"""
Zweistufige hybride Compliance-Prüf-Engine für XIMA Formcycle (v8):
- Stufe 1 (Deterministisch, < 20 ms): Formale Struktur-, Layout-, Barrierefreiheits-,
  Validierungs- und Workflow-Prüfung für alle 15 deterministischen Regeln.
- Stufe 2 (Semantisch/Hybrid via OpenAI-kompatibler LLM-REST-API, z. B. GWDG Academic Cloud):
  Semantische Evaluierung der 7 semantischen/hybriden Governance-Regeln anhand des
  kontextoptimierten JSON-Extrakts aus generate_chat_ai_prompt.py.
- Fail-Safe-Transparenz: Ist keine LLM-API angebunden oder tritt ein API-Ausfall auf,
  werden die 7 semantischen Regeln NIEMALS durch starre Heuristiken verfälscht, sondern
  explizit als ungeprüft ('not_applicable' + 'unverified_semantic') ausgewiesen.
"""
import html
import io
import json
import os
import re
import sys
import urllib.error
import urllib.request
import zipfile

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from generate_chat_ai_prompt import (
    INPUT_CLASSES,
    build_prompt_from_payload,
    clean_visible_text,
    decode_text_bytes,
    extract_compact_payload_from_data,
)

SEMANTIC_RULE_IDS = [
    "HWG-STAMM-02",
    "HWG-BTN-01",
    "HWG-BTN-02",
    "HWG-UX-02",
    "HWG-LANG-01",
    "HWG-LANG-02",
    "HWG-FEEDBACK-01",
]

DEFAULT_API_BASE = "https://chat-ai.academiccloud.de/v1"
DEFAULT_LLM_MODEL = "deepseek-v4-flash-0731"


def _load_dotenv_if_present():
    repo_root = os.path.abspath(os.path.join(os.path.dirname(__file__), ".."))
    env_path = os.path.join(repo_root, ".env")
    if not os.path.isfile(env_path):
        return
    try:
        with open(env_path, "r", encoding="utf-8") as f:
            for line in f:
                s = line.strip()
                if not s or s.startswith("#") or "=" not in s:
                    continue
                k, v = s.split("=", 1)
                k = k.strip()
                v = v.strip().strip('"').strip("'")
                if k and k not in os.environ:
                    os.environ[k] = v
    except Exception:
        pass


def load_rules(registry_path="data/rules/rules_registry.json"):
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)


def extract_workflow_emails_and_states_from_fcexport(proj_data):
    emails = []
    states = []

    def walk_nodes(obj):
        if isinstance(obj, dict):
            node_type = obj.get("type")
            if node_type == "FC_EMAIL":
                cp_str = obj.get("customParameters", "{}")
                try:
                    cp = json.loads(cp_str) if isinstance(cp_str, str) else (cp_str or {})
                except Exception:
                    cp = {}
                recipient = (
                    cp.get("to")
                    or cp.get("recipients")
                    or cp.get("recipient")
                    or cp.get("address")
                    or ""
                )
                emails.append({
                    "node_name": str(obj.get("name", "")),
                    "recipient": str(recipient),
                    "subject": str(cp.get("subject", "")),
                    "body": str(cp.get("body", "")),
                })
            elif node_type in ("FC_CHANGE_STATE", "CUSTOM", "RECEIVED"):
                st_name = str(obj.get("name", "")).strip()
                if st_name and st_name != "FC_CHANGE_STATE":
                    states.append(st_name)
            for v in obj.values():
                walk_nodes(v)
        elif isinstance(obj, list):
            for item in obj:
                walk_nodes(item)

    walk_nodes(proj_data)

    dedup_states = []
    for s in states:
        if s not in dedup_states:
            dedup_states.append(s)
    return emails, dedup_states


def _parse_archive_bytes(file_bytes: bytes, filename: str):
    workflow_emails = []
    workflow_states = []
    if filename.lower().endswith(".json"):
        form_data = json.loads(decode_text_bytes(file_bytes))
        workflow_emails = form_data.get("workflow_emails", []) or []
        workflow_states = form_data.get("workflow_states", []) or []
    else:
        with zipfile.ZipFile(io.BytesIO(file_bytes)) as z:
            fcp_candidates = [n for n in z.namelist() if n.endswith(".fcp")]
            if not fcp_candidates:
                raise ValueError(f"Keine .fcp Modelldatei im Formulararchiv '{filename}' gefunden.")
            # Hauptformular bevorzugen (nicht Backup/Subformular, falls mehrere vorhanden)
            fcp_candidates.sort(key=lambda x: (len(x.split("/")), x))
            fcp_name = fcp_candidates[0]
            form_data = json.loads(decode_text_bytes(z.read(fcp_name)))
            fcexports = [
                n for n in z.namelist()
                if n.endswith(".fcexport")
                and ("/projects/" in n or "\\projects\\" in n)
                and "idcheck" not in n
                and "versions" not in n
            ]
            for fce in fcexports:
                proj_data = json.loads(decode_text_bytes(z.read(fce)))
                ems, sts = extract_workflow_emails_and_states_from_fcexport(proj_data)
                workflow_emails.extend(ems)
                for st in sts:
                    if st not in workflow_states:
                        workflow_states.append(st)
    return form_data, workflow_emails, workflow_states


def _has_dirty_label_markup(raw_label: str) -> bool:
    if not raw_label:
        return False
    val = str(raw_label).strip()
    # 1. Doppelt maskierte Entities (z. B. &amp;szlig; oder &amp;nbsp;) oder &nbsp;-Ketten
    if re.search(r"&amp;[a-zA-Z0-9#]+;", val) or "&nbsp;" in val.lower():
        return True
    # 2. Manuelle Zeilenumbrüche, Inline-Spans, verschachtelte Formatierungs-Tags oder Inline-Styles
    if re.search(r"<\s*(?:br|span|div|font|table|tr|td|ul|ol|li|h[1-6])\b", val, re.IGNORECASE):
        return True
    if re.search(r"\bstyle\s*=", val, re.IGNORECASE):
        return True
    if len(re.findall(r"<\s*p\b", val, re.IGNORECASE)) > 1:
        return True
    # 3. Nach einfacher Dekodierung verbleibende spitze Klammern oder Pipe-Trenner im sichtbaren Text
    cleaned = clean_visible_text(val)
    if "|" in cleaned or "<" in cleaned or ">" in cleaned:
        return True
    return False


def _is_width_compact(props: dict, row_counts: dict) -> bool:
    cw = str(props.get("computedwidth") or "").strip()
    if cw.endswith("%"):
        try:
            if float(cw[:-1]) < 100.0:
                return True
        except ValueError:
            pass
    row_id = str(props.get("rowid") or "").strip()
    if row_id and row_counts.get(row_id, 0) >= 2:
        return True
    if props.get("maxwidth"):
        mw = str(props.get("maxwidth")).strip().lower()
        if mw != "100%":
            return True
    col_w = props.get("colwidth") or props.get("width")
    if col_w is not None and str(col_w).strip() not in ("", "100%", "12"):
        return True
    css_all = f"{props.get('cssclasses', '')} {props.get('cssclasseswrapper', '')}".lower()
    if any(cls in css_all for cls in ("col-", "w-25", "w-33", "w-50", "compact")):
        return True
    return False


def evaluate_stage1_ast(form_data: dict, workflow_emails: list, workflow_states: list, filename: str, registry: dict) -> dict:
    """
    Prüft ausschließlich die 15 deterministischen Governance-Regeln (Stufe 1).
    """
    results = {
        "form": filename,
        "violations": [],
        "recommendations": [],
        "passed": [],
        "not_applicable": {},
        "unverified_semantic": [],
        "llm_evaluation": {
            "evaluated": False,
            "status": "pending",
            "model": None,
            "api_base": None,
            "reason": "",
            "unverified_rules": [],
        },
        "score": 100,
    }

    items = form_data.get("items", []) or []
    form_props = form_data.get("properties") or {}
    penalties = registry["scoring"]["severity_penalties"]

    # Index für Hierarchie- & Sichtbarkeitsauflösung (flaches items-Array mit parentid-Referenzen)
    id_to_item = {}
    for it in items:
        p = it.get("properties", {}) or {}
        iid = str(p.get("id") or p.get("name") or "")
        if iid:
            id_to_item[iid] = it

    def get_ancestors(props: dict):
        chain = []
        pid = str(props.get("parentid") or "")
        visited = set()
        for _ in range(8):
            if not pid or pid in visited or pid not in id_to_item:
                break
            visited.add(pid)
            parent_it = id_to_item[pid]
            chain.append(parent_it)
            pid = str((parent_it.get("properties") or {}).get("parentid") or "")
        return chain

    def is_in_header(it: dict) -> bool:
        c = it.get("className", "")
        props = it.get("properties", {}) or {}
        if c == "XHeader":
            return True
        pid = str(props.get("parentid") or "").lower()
        if "header" in pid:
            return True
        return any(anc.get("className") == "XHeader" for anc in get_ancestors(props))

    def is_applicant_visible(props: dict) -> bool:
        vs = props.get("viewstatus")
        if isinstance(vs, list) and len(vs) > 0 and "-1" not in [str(x).strip() for x in vs]:
            return False
        for anc in get_ancestors(props):
            anc_vs = (anc.get("properties") or {}).get("viewstatus")
            if isinstance(anc_vs, list) and len(anc_vs) > 0 and "-1" not in [str(x).strip() for x in anc_vs]:
                return False
        return True

    def get_section_key(props: dict) -> str:
        for anc in get_ancestors(props):
            if anc.get("className") in ("XFieldSet", "XContainer", "XContainerInvisible", "XPage"):
                ap = anc.get("properties") or {}
                return str(ap.get("id") or ap.get("name") or "root")
        return str(props.get("parentid") or "root")

    # Zeilenbelegung (rowid) für HWG-UX-01 zählen
    row_counts = {}
    for it in items:
        props = it.get("properties", {}) or {}
        if not is_applicant_visible(props):
            continue
        rid = str(props.get("rowid") or "").strip()
        if rid:
            row_counts[rid] = row_counts.get(rid, 0) + 1

    # Container-Breiten (HWG-CD-01)
    container_widths = []
    if isinstance(form_props, dict) and form_props.get("maxwidth"):
        container_widths.append(("form_properties", str(form_props.get("maxwidth")).strip().lower()))

    header_images = []
    header_h1_count = 0
    header_has_non_h1_title = False
    footer_shows_logo = False
    header_or_footer_shows_req_hint = False
    footer_shows_privacy = False

    fieldsets_all = []
    fieldsets_missing_legend = []
    unsemantic_section_containers = []
    container_input_children = {}

    required_fields_total = 0
    manual_asterisks_in_labels = []
    dirty_labels = []
    dev_notes = []

    section_personal_sequences = {}
    has_personal_data = False
    has_text_dsgvo_with_link = False

    has_upload_elements = False
    deficient_uploads = []
    structured_fields_unvalidated = []
    has_compact_fields = False
    compact_fields_unconstrained = []

    applicant_input_count = 0

    non_person_keywords = [
        "vorname", "antrag", "bank", "kredit", "projekt", "programm",
        "foerder", "förder", "titel", "datei", "forschung", "vorhaben", "institut",
        "organisation", "unternehmen", "thema", "kurs", "modul", "fach",
        "abteilung", "studiengang", "dokument", "bezeichnung", "stelle",
        "einrichtung", "arbeit", "abschlussarbeit", "hochschule", "firma",
        "suche", "praxispartner", "betreuer"
    ]

    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {}) or {}
        elem_name = str(props.get("name") or "unnamed")
        name_low = elem_name.lower()
        app_vis = is_applicant_visible(props)

        raw_lbl = str(props.get("label") or props.get("text") or props.get("heading") or "")
        lbl_clean = clean_visible_text(raw_lbl)
        lbl_lower = lbl_clean.lower()
        help_raw = str(props.get("helptext") or props.get("help") or props.get("tooltip") or props.get("description") or "")
        help_clean = clean_visible_text(help_raw).lower()

        # 1. HWG-CD-01: Breiten auf XHeader, XPage, XFooter
        if c in ("XHeader", "XPage", "XFooter"):
            mw = str(props.get("maxwidth") or "").strip().lower()
            if mw:
                container_widths.append((elem_name, mw))

        # 2. HWG-CD-02 & HWG-CD-04: Header-Prüfung
        if is_in_header(it):
            if c == "XImage":
                header_images.append(props)
            rte_h = str(props.get("rtevalue") or "")
            hdg_h = str(props.get("heading") or "")
            lbl_h = str(props.get("label") or "")
            txt_h = str(props.get("text") or "")
            lvl_h = str(props.get("headinglevel") or "").strip()
            combined_h = f"{rte_h} {hdg_h} {lbl_h} {txt_h}"
            h1_matches = len(re.findall(r"<\s*h1\b", combined_h, re.IGNORECASE))
            if h1_matches > 0:
                header_h1_count += h1_matches
            elif lvl_h == "1" and clean_visible_text(combined_h):
                header_h1_count += 1
            elif re.search(r"<\s*h[2-6]\b", combined_h, re.IGNORECASE) or (
                c in ("XSpan", "XHeading", "XText") and len(clean_visible_text(combined_h)) >= 5
            ):
                header_has_non_h1_title = True

        # 3. HWG-CD-03, HWG-A11Y-02 (Container-Flag), HWG-DSGVO-01 (Footer-Flag)
        if c in ("XHeader", "XFooter"):
            if str(props.get("showrequiredhint", "0")).strip().lower() in ("1", "true"):
                header_or_footer_shows_req_hint = True
        if c == "XFooter":
            if str(props.get("showlogo", "0")).strip().lower() in ("1", "true"):
                footer_shows_logo = True
            if str(props.get("privacyPolicyShow", "0")).strip().lower() in ("1", "true"):
                footer_shows_privacy = True

        # 4. HWG-A11Y-01: Fieldsets & Legenden vs. unsemantische Container
        if c == "XFieldSet" and app_vis:
            fieldsets_all.append(elem_name)
            leg_txt = clean_visible_text(props.get("legend") or props.get("label") or props.get("heading") or "")
            if not leg_txt:
                fieldsets_missing_legend.append(elem_name)

        if c in INPUT_CLASSES and app_vis:
            applicant_input_count += 1
            # Prüfe, ob das Eingabefeld in einem Top-Level-XContainer (ohne umschließendes XFieldSet) liegt
            ancs = get_ancestors(props)
            in_fieldset = any(a.get("className") == "XFieldSet" for a in ancs)
            if not in_fieldset:
                for a in ancs:
                    if a.get("className") in ("XContainer", "XContainerInvisible") and not is_in_header(a):
                        cname = str((a.get("properties") or {}).get("name") or "container")
                        container_input_children[cname] = container_input_children.get(cname, 0) + 1

        # 5. HWG-A11Y-02: Pflichtfelder & manuelle Sternchen
        if c in INPUT_CLASSES and app_vis:
            is_req = str(props.get("required", "0")).strip().lower() in ("1", "true") or bool(str(props.get("requiredif") or "").strip())
            if is_req:
                required_fields_total += 1
            elif re.search(r"(?:\*\s*$|\(\*\)|\s\*(?:\s|$))", lbl_clean):
                manual_asterisks_in_labels.append(elem_name)

        # 6. HWG-A11Y-03: Unsaubere HTML-Fragmente in Feld-/Fieldset-Beschriftungen
        if (c in INPUT_CLASSES or c == "XFieldSet") and app_vis:
            raw_field_lbl = str(props.get("label") or "")
            if raw_field_lbl and _has_dirty_label_markup(raw_field_lbl):
                dirty_labels.append((elem_name, " ".join(raw_field_lbl.split())[:45]))

        # 7. HWG-UI-01: Sichtbare Entwickler-Notizen (inkl. XSpan.rtevalue!)
        if app_vis:
            for tk in ("label", "text", "heading", "rtevalue", "value"):
                tval = str(props.get(tk) or "")
                if not tval:
                    continue
                tval_clean = clean_visible_text(tval)
                tval_low = tval_clean.lower()
                if any(
                    pat in tval_low
                    for pat in (
                        "javascript",
                        "shibboleth",
                        "shibboleh",
                        "ldap-member",
                        "forms-admin",
                        "postfach-sb",
                        "display:none",
                        "display: none",
                        "ausgeblendet (hide)",
                        "saml-hslu",
                    )
                ):
                    dev_notes.append((elem_name, tval_clean[:65]))
                    break

        # 8. HWG-STAMM-01: Stammdaten-Sequenz pro Sektion (ohne XTextArea und ohne interne Bearbeiterfelder)
        if c in INPUT_CLASSES and c != "XTextArea" and app_vis:
            sec_key = get_section_key(props)
            seq = section_personal_sequences.setdefault(sec_key, [])
            has_nachname_in_sec = any(f[0] == "nachname" for f in seq)

            # Explizite Personen-Nachnamensmuster VOR non_person_keywords prüfen (Fix für 'Name Antragstellende/r')
            is_explicit_person_lastname = (
                "nachname" in name_low
                or "nachname" in lbl_lower
                or lbl_lower in ("name", "familienname")
                or any(
                    p in lbl_lower
                    for p in ("name antragstellende", "name antragsteller", "name der antragstellenden")
                )
            ) and "vorname" not in name_low and "vorname" not in lbl_lower and "suche" not in name_low and "suche" not in lbl_lower

            is_non_person = any(k in name_low or k in lbl_lower for k in non_person_keywords)

            if any(t in name_low or t in lbl_lower for t in ("anrede", "salutation")) and len(lbl_clean) <= 30:
                seq.append(("anrede", elem_name, lbl_clean or "Anrede", 1))
            elif ("vorname" in name_low or "vorname" in lbl_lower) and "suche" not in name_low:
                seq.append(("vorname", elem_name, lbl_clean or "Vorname", 2))
            elif is_explicit_person_lastname or (
                not is_non_person and not has_nachname_in_sec and "name" in name_low
            ):
                seq.append(("nachname", elem_name, lbl_clean or "Nachname", 3))
            elif any(t in name_low or t in lbl_lower for t in ("email", "e-mail", "mail")) and c == "XTextField":
                seq.append(("email", elem_name, lbl_clean or "E-Mail-Adresse", 4))
            elif any(t in name_low or t in lbl_lower for t in ("telefon", "telefonnummer", "phone", "mobilfunk")) and c == "XTextField":
                seq.append(("telefon", elem_name, lbl_clean or "Telefonnummer", 5))

        # 9. HWG-DSGVO-01: Personendaten & Datenschutzhinweis mit Link
        if c in INPUT_CLASSES and any(
            t in name_low or t in lbl_lower
            for t in ("vorname", "nachname", "email", "e-mail", "matrikel", "geburtsdatum", "iban", "anschrift", "telefon")
        ):
            has_personal_data = True

        raw_html_ctx = f"{raw_lbl} {help_raw} {props.get('rtevalue', '')} {props.get('html', '')}".lower()
        has_priv_term = any(
            t in raw_html_ctx
            for t in ("datenschutz", "dsgvo", "art. 13", "artikel 13", "datenverarbeitung")
        )
        has_priv_link = any(
            lnk in raw_html_ctx
            for lnk in ("href=", "https://", "http://", "www.hwg-lu.de/datenschutz", "hwg-lu.de/datenschutz")
        )
        if has_priv_term and has_priv_link:
            has_text_dsgvo_with_link = True

        # 10. HWG-UPLOAD-01: Technische & sichtbare Upload-Spezifikation
        if (c in ("XUpload", "XFile", "XUploadButton") or "upload" in name_low) and app_vis:
            has_upload_elements = True
            vis_ctx = f"{lbl_lower} {help_clean}"
            has_vis_formats = any(
                fmt in vis_ctx for fmt in ("pdf", "jpg", "jpeg", "png", "docx", "xlsx", "zip", "dateiformat")
            )
            has_vis_size = any(
                sz in vis_ctx for sz in ("mb", "kb", "maximal", "max.", "dateigröße", "dateigroesse")
            )
            fext = str(props.get("fileextension") or "").strip().lower()
            try:
                msize = int(str(props.get("maxfilesize") or "0").strip() or "0")
            except ValueError:
                msize = 0
            has_tech_limits = bool(fext) and msize > 0

            # Widerspruchsprüfung (z. B. Label verspricht docx/xlsx, fileextension erlaubt nur pdf/jpg)
            contradiction = False
            if fext:
                for promised_ext in ("docx", "xlsx", "zip"):
                    if promised_ext in vis_ctx and promised_ext[:3] not in fext:
                        contradiction = True

            if not (has_vis_formats and has_vis_size and has_tech_limits) or contradiction:
                reasons = []
                if not has_tech_limits:
                    reasons.append("technische Dateiendung/Maximalgröße fehlt")
                if not has_vis_formats:
                    reasons.append("Formate im Hilfetext/Label fehlen")
                if not has_vis_size:
                    reasons.append("Größenlimit im Hilfetext/Label fehlt")
                if contradiction:
                    reasons.append("Widerspruch zwischen Textangabe und fileextension")
                deficient_uploads.append(f"{elem_name} ({', '.join(reasons)})")

        # 11. HWG-VAL-01: Strukturierte Eingabefelder (PLZ, IBAN, Telefon, Datum, Matrikelnummer)
        if c in ("XTextField", "XDate", "XNumber") and app_vis:
            dt = str(props.get("datatype") or "").strip()
            vrule = str(props.get("vrule") or props.get("pattern") or "").strip()
            val_dict = props.get("validation") if isinstance(props.get("validation"), dict) else {}
            has_custom_regex = (dt == "regexp" and bool(vrule)) or bool(props.get("pattern")) or bool(val_dict.get("regex"))

            is_plz = bool(re.search(r"\b(?:plz|postleitzahl)\b", lbl_lower)) or "plz" in name_low or "postleitzahl" in name_low
            is_iban = bool(re.search(r"\biban\b", lbl_lower)) or "iban" in name_low
            is_phone = any(t in name_low or t in lbl_lower for t in ("telefon", "mobilfunk", "handynummer"))
            is_date = c == "XDate" or any(t in name_low or t in lbl_lower for t in ("geburtsdatum",)) or bool(re.search(r"\bdatum\b", lbl_lower))
            is_matrikel = "matrikel" in name_low or "matrikel" in lbl_lower

            if is_plz:
                if not (dt == "plzDE" or has_custom_regex):
                    structured_fields_unvalidated.append(f"{elem_name} (PLZ: Typ '{dt or 'text'}')")
            elif is_iban:
                if not (has_custom_regex or val_dict.get("type") == "iban"):
                    structured_fields_unvalidated.append(f"{elem_name} (IBAN: leeres/fehlendes Regex-Muster)")
            elif is_phone:
                # Erlaubt sowohl Formcycle-Preset 'phone' als auch eigenen Regex (empfohlen für '+'-Vorwahlen!)
                if not (dt == "phone" or has_custom_regex):
                    structured_fields_unvalidated.append(f"{elem_name} (Telefon: unvalidierter Freitext)")
            elif is_date:
                if not (c == "XDate" or dt in ("dateDE", "dateISO", "date", "datetime") or has_custom_regex):
                    structured_fields_unvalidated.append(f"{elem_name} (Datum: Typ '{dt or 'text'}')")
            elif is_matrikel:
                if not has_custom_regex:
                    structured_fields_unvalidated.append(f"{elem_name} (Matrikelnummer: Typ '{dt or 'text'}' ohne 6–7-stelligen Regex)")

        # 12. HWG-UX-01: Kompakte Feldbreiten (PLZ, Hausnummer)
        if c == "XTextField" and app_vis:
            is_compact = (
                bool(re.search(r"\b(?:plz|postleitzahl|hausnummer|hausnr|hnr)\b", lbl_lower))
                or any(k in name_low for k in ("plz", "postleitzahl", "hausnummer", "hnr"))
            )
            if is_compact:
                has_compact_fields = True
                if not _is_width_compact(props, row_counts):
                    compact_fields_unconstrained.append(elem_name)

    for cname, cnt in container_input_children.items():
        if cnt >= 3:
            unsemantic_section_containers.append(f"{cname} ({cnt} Felder)")

    # --- Regelauswertung Stufe 1 (15 deterministische Regeln) ---

    # 1. HWG-CD-01
    distinct_widths = {w for _, w in container_widths if w}
    if not distinct_widths or distinct_widths != {"850px"}:
        bad_w = sorted(w for w in distinct_widths if w != "850px") or ["undefiniert"]
        results["violations"].append({
            "rule": "HWG-CD-01",
            "severity": "major",
            "message": f"Layout-Container weichen vom 850px-Standard ab (gefunden: {', '.join(bad_w)})."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-CD-01 (Layout-Breite durchgängig 850px)")

    # 2. HWG-CD-02
    if not header_images:
        results["violations"].append({
            "rule": "HWG-CD-02",
            "severity": "critical",
            "message": "Kein offizielles HWG-Header-Banner (XImage) innerhalb des Header-Containers (XHeader) vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        img_p = header_images[0]
        img_h = str(img_p.get("imageheight") or img_p.get("height") or "").strip().lower()
        img_align = str(img_p.get("textalign") or img_p.get("align") or "").strip().lower()
        img_alt = clean_visible_text(img_p.get("alt") or img_p.get("alttext") or "")
        img_alt_low = img_alt.lower()

        is_h60 = img_h in ("60", "60px")
        is_right = img_align in ("right", "2")
        has_valid_alt = bool(img_alt) and (
            "hochschule für wirtschaft und gesellschaft" in img_alt_low
            or "hochschule fuer wirtschaft und gesellschaft" in img_alt_low
            or "hwg ludwigshafen" in img_alt_low
        )
        if not (is_h60 and is_right and has_valid_alt):
            issues = []
            if not is_h60:
                issues.append(f"Höhe ist '{img_h or 'undefiniert'}' statt 60px")
            if not is_right:
                issues.append(f"Ausrichtung ist '{img_align or 'links'}' statt rechtsbündig")
            if not has_valid_alt:
                issues.append("barrierefreier Alternativtext (alt) fehlt oder unvollständig")
            results["violations"].append({
                "rule": "HWG-CD-02",
                "severity": "major",
                "message": f"HWG-Header-Logo weicht von den Vorgaben ab: {', '.join(issues)}."
            })
            results["score"] -= penalties["major"]
        else:
            results["passed"].append("HWG-CD-02 (Header-Logo 60px, rechtsbündig, mit korrektem Alt-Text)")

    # 3. HWG-CD-03
    if footer_shows_logo:
        results["violations"].append({
            "rule": "HWG-CD-03",
            "severity": "major",
            "message": "Im Footer (XFooter) ist 'Logo anzeigen' (showlogo='1') aktiviert ('Powered by XIMA Formcycle')."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-CD-03 (XIMA-Herstellerlogo im Footer deaktiviert)")

    # 4. HWG-CD-04
    if header_h1_count == 1:
        results["passed"].append("HWG-CD-04 (Formulartitel im Header eindeutig als H1 ausgezeichnet)")
    else:
        if header_h1_count > 1:
            msg = f"Mehrere H1-Überschriften ({header_h1_count}) im Header gefunden; zulässig ist genau eine H1-Hauptüberschrift."
        elif header_has_non_h1_title:
            msg = "Formulartitel im Header (XHeader) ist nicht als Überschrift erster Ordnung (<h1>) ausgezeichnet (nur H2/Fließtext gefunden)."
        else:
            msg = "Kein Formulartitel als <h1> innerhalb des Kopfbereichs (XHeader) vorhanden."
        results["violations"].append({
            "rule": "HWG-CD-04",
            "severity": "major",
            "message": msg
        })
        results["score"] -= penalties["major"]

    # 5. HWG-A11Y-01
    if applicant_input_count < 4 and not fieldsets_all:
        results["not_applicable"]["HWG-A11Y-01"] = "Kleinstformular (< 4 Eingabefelder): Keine Abschnittsgruppierung erforderlich."
    elif not fieldsets_all:
        results["violations"].append({
            "rule": "HWG-A11Y-01",
            "severity": "critical",
            "message": f"Keine semantischen XFieldSet-Gruppierungen für {applicant_input_count} Eingabefelder vorhanden."
        })
        results["score"] -= penalties["critical"]
    elif fieldsets_missing_legend or unsemantic_section_containers:
        issues = []
        if fieldsets_missing_legend:
            issues.append(f"XFieldSet ohne Legende (<legend>): {', '.join(fieldsets_missing_legend[:4])}")
        if unsemantic_section_containers:
            issues.append(f"Unsemantische XContainer statt Fieldset genutzt: {', '.join(unsemantic_section_containers[:3])}")
        results["violations"].append({
            "rule": "HWG-A11Y-01",
            "severity": "critical",
            "message": f"Semantische Abschnittsgruppierung unvollständig: {'; '.join(issues)}."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append(f"HWG-A11Y-01 ({len(fieldsets_all)} XFieldSet-Gruppen mit Legenden vorhanden)")

    # 6. HWG-A11Y-02
    a11y02_issues = []
    if required_fields_total > 0 and not header_or_footer_shows_req_hint:
        a11y02_issues.append("Pflichtfeldlegende (showrequiredhint='1') weder in Kopfzeile (XHeader) noch Fußzeile (XFooter) aktiviert")
    if manual_asterisks_in_labels:
        a11y02_issues.append(f"Manuelles Sternchen (*) im Label ohne native Pflichtfeldfunktion (required='1') in {manual_asterisks_in_labels[:4]}")

    if a11y02_issues:
        results["violations"].append({
            "rule": "HWG-A11Y-02",
            "severity": "major",
            "message": f"Pflichtfeld-Deklaration fehlerhaft: {'; '.join(a11y02_issues)}."
        })
        results["score"] -= penalties["major"]
    elif required_fields_total > 0:
        results["passed"].append(f"HWG-A11Y-02 ({required_fields_total} Pflichtfelder programmatisch inkl. globaler Legende deklariert)")
    else:
        results["not_applicable"]["HWG-A11Y-02"] = "Keine Pflichtfelder im Formular deklariert."

    # 7. HWG-A11Y-03
    if dirty_labels:
        affected = [d[0] for d in dirty_labels]
        preview = ", ".join(affected[:6]) + (f" und {len(affected) - 6} weitere" if len(affected) > 6 else "")
        results["violations"].append({
            "rule": "HWG-A11Y-03",
            "severity": "minor",
            "message": f"HTML-Störfragmente (<br>, <span>, &nbsp;, doppelte Entities oder '|') in {len(dirty_labels)} Label(s): [{preview}]."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-A11Y-03 (Saubere Label-Syntax ohne störende HTML-Fragmente)")

    # 8. HWG-STAMM-01
    total_personal_fields = sum(len(v) for v in section_personal_sequences.values())
    out_of_order = []
    for sec_key, seq in section_personal_sequences.items():
        if len(seq) < 2:
            continue
        for i in range(len(seq) - 1):
            curr, nxt = seq[i], seq[i + 1]
            if curr[3] > nxt[3]:
                out_of_order.append(f"'{curr[2]}' ({curr[1]}) vor '{nxt[2]}' ({nxt[1]})")

    if any(len(v) >= 2 for v in section_personal_sequences.values()):
        if out_of_order:
            results["violations"].append({
                "rule": "HWG-STAMM-01",
                "severity": "major",
                "message": f"Inkonsistente Stammdaten-Abfolge: {', '.join(out_of_order[:3])}. Erwartet: Anrede -> Vorname -> Nachname -> E-Mail-Adresse -> Telefonnummer."
            })
            results["score"] -= penalties["major"]
        else:
            results["passed"].append("HWG-STAMM-01 (Kanonische Stammdaten-Abfolge in allen Sektionen eingehalten)")
    else:
        results["not_applicable"]["HWG-STAMM-01"] = (
            f"Keine zusammenhängende Stammdaten-Sektion mit >= 2 Personenfeldern vorhanden (gefunden: {total_personal_fields})."
        )

    # 9. HWG-UI-01
    if dev_notes:
        preview_dn = "; ".join(f"{n}: '{txt}'" for n, txt in dev_notes[:3])
        results["violations"].append({
            "rule": "HWG-UI-01",
            "severity": "critical",
            "message": f"Sichtbare Entwickler-Notizen / technische Hinweise im Frontend: {preview_dn}."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-UI-01 (Keine sichtbaren Entwickler-Notizen im Frontend)")

    # 10. HWG-DSGVO-01
    has_dsgvo_notice = footer_shows_privacy or has_text_dsgvo_with_link
    if not has_personal_data:
        results["not_applicable"]["HWG-DSGVO-01"] = "Formular erhebt keine personenbezogenen Daten."
    elif not has_dsgvo_notice:
        results["violations"].append({
            "rule": "HWG-DSGVO-01",
            "severity": "critical",
            "message": "Personenbezogene Daten werden erhoben, aber weder Footer-Datenschutzerklärung (privacyPolicyShow='1') noch verlinkter Art.-13-DSGVO-Hinweis vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-DSGVO-01 (DSGVO-Datenschutzhinweis mit Verlinkung / Footer-Option vorhanden)")

    # 11. HWG-UPLOAD-01
    if not has_upload_elements:
        results["not_applicable"]["HWG-UPLOAD-01"] = "Keine Dateiupload-Elemente im Formular vorhanden."
    elif deficient_uploads:
        results["violations"].append({
            "rule": "HWG-UPLOAD-01",
            "severity": "major",
            "message": f"{len(deficient_uploads)} Upload-Element(e) unvollständig oder widersprüchlich spezifiziert: {', '.join(deficient_uploads[:3])}."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-UPLOAD-01 (Alle Dateiuploads technisch und im Hilfetext konsistent spezifiziert)")

    # 12. HWG-VAL-01
    if structured_fields_unvalidated:
        results["violations"].append({
            "rule": "HWG-VAL-01",
            "severity": "major",
            "message": f"Strukturierte Eingabefelder ohne gültigen Validator / Regex gefunden: {', '.join(structured_fields_unvalidated[:4])}."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-VAL-01 (Alle strukturierten Eingabefelder formal validiert)")

    # 13. HWG-UX-01
    if not has_compact_fields:
        results["not_applicable"]["HWG-UX-01"] = "Keine typischen Kompaktfelder (PLZ, Hausnummer) im Formular vorhanden."
    elif compact_fields_unconstrained:
        results["violations"].append({
            "rule": "HWG-UX-01",
            "severity": "minor",
            "message": f"Kompakte Felder über volle 100%-Zeilenbreite gestreckt: {', '.join(compact_fields_unconstrained[:3])}."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-UX-01 (Affordanzgerechte kompakte Feldbreiten eingehalten)")

    # 14. HWG-WF-01
    if not workflow_states:
        results["violations"].append({
            "rule": "HWG-WF-01",
            "severity": "minor",
            "message": "Keine expliziten Status-Knoten (FC_CHANGE_STATE) im Workflow hinterlegt."
        })
        results["score"] -= penalties["minor"]
    else:
        canonical_roots = [
            "eingegangen", "in prüfung", "in bearbeitung",
            "nachforderung", "genehmigt", "abgelehnt", "archiviert", "abgeschlossen"
        ]
        non_canonical_states = [
            s for s in workflow_states
            if not any(root in s.lower().strip() for root in canonical_roots)
        ]
        if non_canonical_states:
            results["violations"].append({
                "rule": "HWG-WF-01",
                "severity": "minor",
                "message": f"Nicht-standardisierte Ad-hoc-Workflow-Status gefunden ({len(non_canonical_states)}): {non_canonical_states}."
            })
            results["score"] -= penalties["minor"]
        else:
            results["passed"].append(f"HWG-WF-01 (Kanonischer Workflow-Lebenszyklus eingehalten: {', '.join(workflow_states)})")

    # 15. HWG-WF-02
    alias_tokens = ("%$project_alias%", "%$record_id%", "%$vorgang", "[%$id%]")
    emails_with_alias = [
        em for em in workflow_emails
        if any(tok in f"{em.get('subject', '')} {em.get('body', '')}".lower() for tok in alias_tokens)
    ]
    if not workflow_emails or not emails_with_alias:
        results["violations"].append({
            "rule": "HWG-WF-02",
            "severity": "minor",
            "message": "Fehlender dynamischer Vorgangsplatzhalter ([%$PROJECT_ALIAS%]) in den automatisierten Workflow-E-Mails (FC_EMAIL)."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append(f"HWG-WF-02 (Dynamische Vorgangsreferenz in {len(emails_with_alias)}/{len(workflow_emails)} Workflow-E-Mails vorhanden)")

    results["score"] = max(0, results["score"])
    return results


def _mark_semantic_unverified(results: dict, registry: dict, status: str, reason: str, api_base: str, model: str, rule_ids=None):
    target_ids = rule_ids if rule_ids is not None else SEMANTIC_RULE_IDS
    rule_lookup = {r["id"]: r for r in registry["rules"]}
    for rid in target_ids:
        rtype = (rule_lookup.get(rid) or {}).get("evaluation_type", "semantic")
        label = "Semantische KI-Regel" if rtype == "semantic" else "Hybride AST/KI-Regel"
        if rid not in results["unverified_semantic"]:
            results["unverified_semantic"].append(rid)
        results["not_applicable"][rid] = (
            f"KI-Prüfung ausstehend ({label}): Diese Regel wurde NICHT durch ein Sprachmodell (LLM) begutachtet. "
            f"Grund: {reason}"
        )
    results["llm_evaluation"] = {
        "evaluated": False,
        "status": status,
        "api_base": api_base,
        "model": model,
        "reason": reason,
        "unverified_rules": list(results["unverified_semantic"]),
    }


def _extract_json_from_llm_text(raw_text: str) -> dict:
    # Entferne optionale <think>...</think> Reasoning-Blöcke (z. B. Qwen 3 / DeepSeek)
    cleaned = re.sub(r"<think>.*?</think>", "", raw_text, flags=re.DOTALL | re.IGNORECASE).strip()
    fence_match = re.search(r"```(?:json)?\s*(\{.*\})\s*```", cleaned, flags=re.DOTALL | re.IGNORECASE)
    if fence_match:
        cleaned = fence_match.group(1).strip()
    else:
        start = cleaned.find("{")
        end = cleaned.rfind("}")
        if start != -1 and end != -1 and end > start:
            cleaned = cleaned[start : end + 1]
    return json.loads(cleaned)


def merge_llm_evaluation_payload(results: dict, llm_obj: dict, registry: dict, model_name: str, api_base: str) -> dict:
    """
    Fusioniert die strukturierte JSON-Antwort eines LLMs für die 7 semantischen/hybriden Regeln
    deterministisch mit den Stufe-1-AST-Ergebnissen gemäß Gleichung (4.2).
    """
    penalties = registry["scoring"]["severity_penalties"]
    rule_lookup = {r["id"]: r for r in registry["rules"]}
    evaluated_entries = llm_obj.get("evaluated_rules") or []
    seen_semantic = set()

    for entry in evaluated_entries:
        if not isinstance(entry, dict):
            continue
        rid = str(entry.get("rule_id") or entry.get("rule") or "").strip()
        if rid not in SEMANTIC_RULE_IDS or rid in seen_semantic:
            continue
        seen_semantic.add(rid)
        results["not_applicable"].pop(rid, None)
        if rid in results["unverified_semantic"]:
            results["unverified_semantic"].remove(rid)

        reg_rule = rule_lookup[rid]
        canonical_sev = reg_rule["severity"]
        status = str(entry.get("status") or "").strip().upper()
        finding = str(entry.get("finding") or entry.get("message") or "").strip()
        rem_sugg = str(entry.get("remediation_suggestion") or "").strip()
        affected = entry.get("affected_elements") or []
        aff_str = f" (Betroffen: {', '.join(str(a) for a in affected[:4])})" if affected else ""
        full_msg = f"[KI-Befund · {model_name}] {finding}{aff_str}" + (f" — Vorschlag: {rem_sugg}" if rem_sugg else "")

        if status == "VIOLATION":
            if canonical_sev == "recommendation":
                results["recommendations"].append({
                    "rule": rid,
                    "rule_id": rid,
                    "severity": "recommendation",
                    "message": full_msg,
                })
            else:
                results["violations"].append({
                    "rule": rid,
                    "rule_id": rid,
                    "severity": canonical_sev,
                    "message": full_msg,
                })
                results["score"] -= penalties.get(canonical_sev, 0)
        elif status == "RECOMMENDATION":
            results["recommendations"].append({
                "rule": rid,
                "rule_id": rid,
                "severity": "recommendation",
                "message": full_msg,
            })
        elif status in ("NOT_APPLICABLE", "N/A", "NA"):
            results["not_applicable"][rid] = f"[KI-Prüfung · {model_name}] {finding or 'Auf diesen Formularkontext nicht anwendbar.'}"
        elif status == "PASS":
            results["passed"].append(f"{rid} ({finding or 'Semantische KI-Prüfung bestanden'})")
        else:
            results["unverified_semantic"].append(rid)
            results["not_applicable"][rid] = f"KI-Prüfung unvollständig: Unbekannter Status '{status}' vom Modell '{model_name}'."

    missing = [rid for rid in SEMANTIC_RULE_IDS if rid not in seen_semantic]
    for rid in missing:
        if rid not in results["unverified_semantic"]:
            results["unverified_semantic"].append(rid)
        results["not_applicable"][rid] = (
            f"KI-Prüfung unvollständig: Modell '{model_name}' lieferte keine Bewertung für {rid}."
        )

    results["score"] = max(0, results["score"])
    results["llm_evaluation"] = {
        "evaluated": len(missing) == 0,
        "status": "ok" if not missing else "partial",
        "api_base": api_base,
        "model": model_name,
        "reason": f"Semantische Prüfung über Modell '{model_name}' abgeschlossen."
        if not missing
        else f"Modell '{model_name}' hat {len(seen_semantic)}/7 semantische Regeln bewertet (fehlend: {', '.join(missing)}).",
        "unverified_rules": list(results["unverified_semantic"]),
    }
    return results


def evaluate_stage2_llm(results: dict, form_data: dict, workflow_emails: list, filename: str, registry: dict, llm_config: dict = None) -> dict:
    _load_dotenv_if_present()
    cfg = llm_config or {}
    api_key = (
        cfg.get("api_key")
        or os.environ.get("LLM_API_KEY")
        or os.environ.get("GWDG_API_KEY")
        or os.environ.get("OPENAI_API_KEY")
        or ""
    ).strip()
    api_base = (
        cfg.get("api_base")
        or os.environ.get("LLM_API_BASE")
        or os.environ.get("GWDG_API_BASE")
        or DEFAULT_API_BASE
    ).strip().rstrip("/")
    model = (
        cfg.get("model")
        or os.environ.get("LLM_MODEL")
        or os.environ.get("GWDG_MODEL")
        or DEFAULT_LLM_MODEL
    ).strip()
    timeout_sec = int(cfg.get("timeout") or os.environ.get("LLM_TIMEOUT") or 45)
    allow_no_key = str(os.environ.get("LLM_ALLOW_NO_KEY", "0")).strip() == "1"

    if not api_key and not allow_no_key:
        _mark_semantic_unverified(
            results,
            registry,
            status="unconfigured",
            reason="Keine LLM-API angebunden (kein API-Key in LLM_API_KEY / GWDG_API_KEY oder Dashboard-Konfiguration hinterlegt).",
            api_base=api_base,
            model=model,
        )
        return results

    payload = extract_compact_payload_from_data(form_data, workflow_emails, filename)
    prompt = build_prompt_from_payload(payload, registry)

    endpoint = api_base if api_base.endswith("/chat/completions") else f"{api_base}/chat/completions"
    req_body = json.dumps({
        "model": model,
        "temperature": 0.0,
        "messages": [
            {
                "role": "system",
                "content": "Du bist ein präziser wissenschaftlicher Usability- und Governance-Auditor. Antworte ausschließlich mit validem JSON gemäß Schema."
            },
            {
                "role": "user",
                "content": prompt
            }
        ]
    }).encode("utf-8")

    headers = {
        "Content-Type": "application/json",
        "Accept": "application/json",
        "User-Agent": "HWG-Formcycle-Compliance-Checker/1.5.0",
    }
    if api_key:
        headers["Authorization"] = f"Bearer {api_key}"

    req = urllib.request.Request(endpoint, data=req_body, headers=headers, method="POST")
    try:
        with urllib.request.urlopen(req, timeout=timeout_sec) as resp:
            resp_raw = resp.read().decode("utf-8", errors="replace")
        resp_json = json.loads(resp_raw)
        content = (
            ((resp_json.get("choices") or [{}])[0].get("message") or {}).get("content")
            or ""
        )
        if not content:
            raise ValueError("Leere Modellantwort im Feld choices[0].message.content.")
        llm_obj = _extract_json_from_llm_text(content)
        return merge_llm_evaluation_payload(results, llm_obj, registry, model_name=model, api_base=api_base)
    except urllib.error.HTTPError as he:
        err_detail = ""
        try:
            err_detail = he.read().decode("utf-8", errors="replace")[:160]
        except Exception:
            pass
        _mark_semantic_unverified(
            results,
            registry,
            status="error",
            reason=f"LLM-API HTTP-Fehler {he.code} ({he.reason}) bei '{endpoint}'. {err_detail}".strip(),
            api_base=api_base,
            model=model,
        )
        return results
    except Exception as exc:
        _mark_semantic_unverified(
            results,
            registry,
            status="error",
            reason=f"LLM-API nicht erreichbar oder Antwort ungültig ({type(exc).__name__}: {exc}).",
            api_base=api_base,
            model=model,
        )
        return results


def _finalize_rule_ids(results: dict) -> dict:
    for v in results["violations"]:
        r_id = v.get("rule") or v.get("rule_id")
        v["rule"] = r_id
        v["rule_id"] = r_id
    for r in results["recommendations"]:
        r_id = r.get("rule") or r.get("rule_id")
        r["rule"] = r_id
        r["rule_id"] = r_id
    results["score"] = max(0, results["score"])
    return results


def evaluate_form_bytes(file_bytes: bytes, filename: str, registry: dict, llm_config: dict = None) -> dict:
    """
    Reine In-Memory-Auswertung (Zero-Disk-Footprint) eines .xfp-Archivs oder Formular-JSONs.
    """
    form_data, workflow_emails, workflow_states = _parse_archive_bytes(file_bytes, filename)
    results = evaluate_stage1_ast(form_data, workflow_emails, workflow_states, filename, registry)
    results = evaluate_stage2_llm(results, form_data, workflow_emails, filename, registry, llm_config=llm_config)
    return _finalize_rule_ids(results)


def evaluate_form(xfp_path: str, registry: dict, llm_config: dict = None) -> dict:
    with open(xfp_path, "rb") as f:
        raw_bytes = f.read()
    return evaluate_form_bytes(raw_bytes, os.path.basename(xfp_path), registry, llm_config=llm_config)


if __name__ == "__main__":
    reg = load_rules()
    test_forms = [
        "data/test_forms/synthetic_compliant_form.json",
        "data/test_forms/synthetic_noncompliant_form.json",
        "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
        "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
        "data/raw_forms/test/adminformulare/Master-Formular.xfp",
    ]

    print(f"=== HWG COMPLIANCE PIPELINE EVALUATION (Registry v{reg['version']}) ===")
    print(f"Gesamtanzahl Governance-Regeln: {len(reg['rules'])} (15 deterministisch [Stufe 1] + 7 semantisch/hybrid [Stufe 2])")

    for tf in test_forms:
        res = evaluate_form(tf, reg)
        llm_info = res.get("llm_evaluation", {})
        print(f"\n{'=' * 22} {res['form']} {'=' * 22}")
        if llm_info.get("evaluated"):
            print(f"[KI-Stufe 2 AKTIV] Modell: {llm_info.get('model')} ({llm_info.get('api_base')})")
        else:
            print(f"[!] WARNUNG – KI-STUFENPRÜFUNG INAKTIV ({llm_info.get('status', 'unavailable').upper()}):")
            print(f"    {llm_info.get('reason')}")
            print(f"    -> {len(res.get('unverified_semantic', []))} semantische Regeln wurden NICHT durch eine KI geprüft!")
        print(f"Compliance-Score:     {res['score']} / 100 Punkte")
        print(f"Bestanden:            {len(res['passed'])}")
        print(f"Verstöße:             {len(res['violations'])}")
        print(f"Empfehlungen (0 P.):  {len(res['recommendations'])}")
        print(f"Nicht zutreffend:     {len(res['not_applicable'])} (davon {len(res.get('unverified_semantic', []))} KI-ungeprüft)")
        for v in res["violations"]:
            print(f"  [X] [{v['severity'].upper():8}] {v['rule']}: {v['message']}")
        for r in res["recommendations"]:
            print(f"  [i] [RECOMM. ] {r['rule']}: {r['message']}")
        for na_k, na_v in res["not_applicable"].items():
            tag = "KEINE KI" if na_k in res.get("unverified_semantic", []) else "N/A     "
            print(f"  [-] [{tag}] {na_k}: {na_v}")
