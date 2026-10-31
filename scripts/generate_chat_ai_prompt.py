import os
import sys
import json
import zipfile
import io
import re
import html


INPUT_CLASSES = {
    "XTextField",
    "XTextArea",
    "XSelect",
    "XCheckbox",
    "XRadio",
    "XDate",
    "XUpload",
    "XFile",
    "XNumber",
}

DEV_NOTE_TOKENS = (
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
    "todo:",
    "fixme:",
)


def decode_text_bytes(raw_bytes: bytes) -> str:
    for enc in ("utf-8", "utf-8-sig", "cp1252", "latin-1"):
        try:
            return raw_bytes.decode(enc)
        except UnicodeDecodeError:
            continue
    return raw_bytes.decode("utf-8", errors="replace")


def clean_visible_text(val) -> str:
    if not val:
        return ""
    s = str(val)
    for _ in range(2):
        s = html.unescape(s)
    s = re.sub(r"<[^>]+>", " ", s)
    return " ".join(s.split())


def extract_long_sentences(items: list, max_words: int = 25, in_header_ids: set = None) -> list:
    long_sents = []
    abbrev_pattern = re.compile(
        r"\b(z\.\s*B\.|bzw\.|inkl\.|ggf\.|ca\.|max\.|mind\.|Nr\.|Art\.|Abs\.|Dr\.|Prof\.|d\.\s*h\.|u\.\s*a\.|etc\.|vgl\.|sog\.|St\.|Str\.)",
        re.IGNORECASE,
    )
    for it in items:
        props = it.get("properties", {}) or {}
        iid = str(props.get("id") or props.get("name") or "")
        if in_header_ids and iid in in_header_ids:
            continue
        ename = str(props.get("name") or "unnamed")
        for field_key in ("rtevalue", "text", "helptext", "help"):
            raw = props.get(field_key)
            if not raw:
                continue
            txt = clean_visible_text(raw)
            if not txt:
                continue
            masked = abbrev_pattern.sub(lambda m: m.group(0).replace(".", "_DOT_"), txt)
            sents = re.split(r"[.!?]+(?:\s+|$)", masked)
            for s in sents:
                s_restored = s.replace("_DOT_", ".").strip()
                words = [w for w in s_restored.split() if any(ch.isalnum() for ch in w)]
                if len(words) > max_words:
                    long_sents.append({
                        "element": ename,
                        "field": field_key,
                        "word_count": len(words),
                        "preview": " ".join(words[:12]) + " ..."
                    })
    return long_sents


def classify_button_role(action_page: str, btn_type: str = "") -> str:
    ap = str(action_page or "").strip()
    ap_low = ap.lower()
    bt_low = str(btn_type or "").strip().lower()
    if ap_low in ("next", "prev", "back", "forward", "xnavbar_next", "xnavbar_prev") or re.match(r"^p\d+(?:_|$)", ap_low):
        return "pagination"
    if ap == "submitNoCheck" or bt_low == "save":
        return "submit_no_check"
    if ap_low == "submit" or bt_low == "submit":
        return "submit"
    return bt_low or "action"


def extract_workflow_emails_from_fcexport_obj(proj_data):
    workflow_emails = []

    def walk_nodes(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "FC_EMAIL":
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
                workflow_emails.append({
                    "node_name": str(obj.get("name", "")),
                    "recipient": str(recipient)[:120],
                    "subject": str(cp.get("subject", ""))[:200],
                    "body": clean_visible_text(cp.get("body", ""))[:500],
                })
            for v in obj.values():
                walk_nodes(v)
        elif isinstance(obj, list):
            for item in obj:
                walk_nodes(item)

    walk_nodes(proj_data)
    return workflow_emails


def extract_compact_payload_from_data(form_data: dict, workflow_emails: list, form_name: str) -> dict:
    items = (
        form_data.get("items")
        or (form_data.get("elements") or {}).get("items")
        or []
    )

    id_to_item = {}
    id_to_full_item = {}
    for it in items:
        p = it.get("properties", {}) or {}
        iid = str(p.get("id") or p.get("name") or "")
        if iid:
            id_to_item[iid] = p
            id_to_full_item[iid] = it

    def is_applicant_visible(props: dict) -> bool:
        curr = props
        visited = set()
        for _ in range(8):
            if not curr:
                break
            vs = curr.get("viewstatus")
            if isinstance(vs, list) and len(vs) > 0:
                vs_strs = [str(x).strip() for x in vs]
                if "-1" not in vs_strs:
                    return False
            pid = str(curr.get("parentid") or "")
            if not pid or pid in visited:
                break
            visited.add(pid)
            curr = id_to_item.get(pid)
        return True

    def is_in_header(it: dict) -> bool:
        if it.get("className") == "XHeader":
            return True
        curr = it.get("properties", {}) or {}
        visited = set()
        for _ in range(8):
            pid = str(curr.get("parentid") or "")
            if not pid or pid in visited:
                break
            if pid.lower() == "xi-header-1":
                return True
            visited.add(pid)
            parent_it = id_to_full_item.get(pid)
            if not parent_it:
                break
            if parent_it.get("className") == "XHeader":
                return True
            curr = parent_it.get("properties", {}) or {}
        return False

    compact_elements = []
    buttons_extracted = []
    suspected_dev_notes = []
    in_header_ids = set()
    raw_xpage_count = 0
    input_count = 0
    upload_count = 0

    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {}) or {}
        if c == "XPage":
            raw_xpage_count += 1
        if c in INPUT_CLASSES:
            input_count += 1
        if c in {"XUpload", "XFile", "XUploadButton"}:
            upload_count += 1

        applicant_vis = is_applicant_visible(props)
        in_hdr = is_in_header(it)
        elem_name = str(props.get("name", ""))
        iid = str(props.get("id") or elem_name or "")
        if in_hdr and iid:
            in_header_ids.add(iid)

        # Vorab-Detektion bekannter technischer Entwicklernotizen (Stufe 1 für HWG-UI-01)
        if applicant_vis:
            for tk in ("label", "text", "heading", "rtevalue", "value"):
                tval = str(props.get(tk) or "")
                if not tval:
                    continue
                tval_clean = clean_visible_text(tval)
                tval_low = tval_clean.lower()
                if any(pat in tval_low for pat in DEV_NOTE_TOKENS):
                    suspected_dev_notes.append({
                        "element": elem_name,
                        "snippet": tval_clean[:80],
                    })
                    break

        # Schaltflächen (XButtonList & XButton) strukturiert extrahieren
        if "Button" in c or c == "XButtonList":
            b_list = props.get("buttons", [])
            if isinstance(b_list, list) and b_list:
                for b in b_list:
                    if not isinstance(b, dict):
                        continue
                    val = clean_visible_text(b.get("value") or b.get("text") or b.get("title") or "")
                    act_page = (b.get("action") or {}).get("page", "") if isinstance(b.get("action"), dict) else ""
                    if val:
                        buttons_extracted.append({
                            "element": elem_name,
                            "label": val,
                            "role": classify_button_role(act_page),
                            "action_page": str(act_page),
                            "applicant_visible": applicant_vis,
                        })
            btn_lbl = clean_visible_text(props.get("text") or props.get("label") or props.get("value") or "")
            if btn_lbl:
                buttons_extracted.append({
                    "element": elem_name,
                    "label": btn_lbl,
                    "role": classify_button_role("", str(props.get("type", ""))),
                    "action_page": str(props.get("type", "")),
                    "applicant_visible": applicant_vis,
                })
            btn_items = props.get("items", [])
            if isinstance(btn_items, list):
                for b in btn_items:
                    val = clean_visible_text((b.get("text") or b.get("value") or b.get("title")) if isinstance(b, dict) else str(b))
                    if val:
                        buttons_extracted.append({
                            "element": elem_name,
                            "label": val,
                            "role": "action",
                            "action_page": "",
                            "applicant_visible": applicant_vis,
                        })

        lbl = clean_visible_text(
            props.get("label")
            or props.get("text")
            or props.get("rtevalue")
            or props.get("heading")
            or props.get("legend")
            or ""
        )
        help_txt = clean_visible_text(
            props.get("helptext")
            or props.get("help")
            or props.get("tooltip")
            or props.get("description")
            or ""
        )
        if (lbl or help_txt) and applicant_vis:
            entry = {
                "className": c,
                "name": elem_name,
                "label_or_text": lbl[:240],
                "helptext": help_txt[:240],
            }
            if in_hdr:
                entry["in_header"] = True
            compact_elements.append(entry)

    effective_page_count = max(1, raw_xpage_count)
    applicant_items = [it for it in items if is_applicant_visible(it.get("properties", {}) or {})]
    long_sentences = extract_long_sentences(applicant_items, max_words=25, in_header_ids=in_header_ids)

    return {
        "form_name": form_name,
        "metrics": {
            "page_count": effective_page_count,
            "raw_xpage_count": raw_xpage_count,
            "input_field_count": input_count,
            "upload_field_count": upload_count,
            "ux02_complexity_threshold_reached": bool(effective_page_count >= 3 or input_count >= 25),
            "suspected_dev_notes_count": len(suspected_dev_notes),
            "suspected_dev_notes": suspected_dev_notes,
            "sentences_over_25_words_count": len(long_sentences),
            "sentences_over_25_words": long_sentences[:6],
        },
        "buttons": buttons_extracted,
        "ui_elements": compact_elements,
        "workflow_emails": workflow_emails,
    }


def extract_compact_payload(xfp_path: str) -> dict:
    workflow_emails = []
    if xfp_path.lower().endswith(".json"):
        with open(xfp_path, "r", encoding="utf-8") as f:
            form_data = json.load(f)
        for em in form_data.get("workflow_emails", []) or []:
            workflow_emails.append({
                "node_name": str(em.get("node_name", "")),
                "recipient": str(em.get("recipient", "")),
                "subject": str(em.get("subject", ""))[:200],
                "body": clean_visible_text(em.get("body", ""))[:500],
            })
    else:
        with open(xfp_path, "rb") as f:
            raw = f.read()
        with zipfile.ZipFile(io.BytesIO(raw)) as z:
            fcp_name = [n for n in z.namelist() if n.endswith(".fcp")][0]
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
                workflow_emails.extend(extract_workflow_emails_from_fcexport_obj(proj_data))

    return extract_compact_payload_from_data(form_data, workflow_emails, os.path.basename(xfp_path))


def build_prompt_from_payload(payload: dict, registry: dict) -> str:
    semantic_rules = [
        r for r in registry["rules"]
        if r.get("evaluation_type") in ("semantic", "hybrid")
    ]
    rule_ids = [r["id"] for r in semantic_rules]

    prompt = f"""Du bist ein wissenschaftlicher Usability-, Barrierefreiheits- und Governance-Auditor für digitale Hochschulformulare (XIMA Formcycle) an der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG Ludwigshafen).
Prüfe den nachfolgenden komprimierten Formular- und Workflow-Extrakt strikt anhand der folgenden {len(semantic_rules)} semantischen und hybriden Governance-Regeln aus der HWG-Compliance-Registry (v{registry['version']}):

=== SEMANTISCHE & HYBRIDE PRÜFREGELN ({', '.join(rule_ids)}) ===
{json.dumps(semantic_rules, ensure_ascii=False, indent=2)}

=== ZU PRÜFENDES FORMULAR (KOMPAKTER AST-EXTRAKT INKL. VORABMETRIKEN) ===
{json.dumps(payload, ensure_ascii=False, indent=2)}

=== PRÜFINSTRUKTIONEN & NEGATIVE CONSTRAINTS ===
1. Bewerte JEDE der {len(semantic_rules)} Regeln ({', '.join(rule_ids)}) genau einmal im Array "evaluated_rules".
2. Nutze für hybride Regeln zwingend die deterministischen Vorabmetriken unter "metrics":
   - HWG-UI-01: Prüfe alle sichtbaren Elemente unter "ui_elements" sowie "metrics.suspected_dev_notes" semantisch darauf, ob interne Entwickler-Notizen, technische Implementierungshinweise (z. B. zu JavaScript, Shibboleth, LDAP, Sichtbarkeit/hide), Baustellenvermerke oder redaktionelle Arbeitskommentare im Frontend stehen. Liegen solche vor, setze status = "VIOLATION".
   - HWG-UX-02: Nur wenn metrics.ux02_complexity_threshold_reached == true ist und kein Zwischenspeichern-Mechanismus existiert, setze status = "RECOMMENDATION" (0 Punkte Abzug). Ist ux02_complexity_threshold_reached == false, setze status = "NOT_APPLICABLE".
   - HWG-LANG-02: Berücksichtige metrics.sentences_over_25_words; wenn dort keine Sätze > 25 Wörter vorliegen und keine extrem verschachtelten Passivkonstruktionen existieren, setze status = "PASS".
3. HWG-STAMM-02: Für E-Mail-Felder sind "E-Mail-Adresse", "E-Mail" und "Hochschul-E-Mail" zulässig. Persönliche Namensfelder müssen getrennt als "Vorname" und "Nachname" benannt sein ("Name Antragstellende/r", "Name" für Personen oder technische Kürzel wie "HWGLU-Email" sind Verstöße; Sachbezeichnungen wie "Benennung des Förderprogramms" sind hingegen zulässig).
4. HWG-BTN-01: Prüfe ausschließlich für Antragstellende sichtbare Aktions- und Absendeschaltflächen (applicant_visible == true und role != "pagination") auf das Action-Verb-Muster ([Zielobjekt] + [Vollverb im Infinitiv]). Formulierungen mit klarem Handlungsverb wie "Antrag einreichen" oder "Kritischen Fall einreichen" sind ZULÄSSIG; reine Zustandsbegriffe ohne Verb ("Kritischer Fall") oder kontextlose Ein-Wort-Labels ("senden", "Submit", "OK") sind Verstöße.
5. HWG-LANG-01: Ignoriere den offiziellen Formulartitel im Kopfbereich (Elemente mit in_header == true), da Überschriften im Header keinen Hilfetext besitzen müssen. Prüfe alle übrigen Formularfelder und Hinweistexte auf unerklärte Verwaltungs-/Hochschulfachbegriffe oder Abkürzungen ohne zugehörigen Hilfetext (helptext).
6. Halluziniere keine Mängel hinzu, die nicht im Extrakt belegt sind.

=== VERBINDLICHES JSON-AUSGABEFORMAT ===
Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt (ohne Markdown-Codeblöcke):
{{
  "form_name": "{payload['form_name']}",
  "evaluated_rules": [
    {{
      "rule_id": "HWG-...",
      "status": "PASS | VIOLATION | RECOMMENDATION | NOT_APPLICABLE",
      "severity": "critical | major | minor | recommendation",
      "affected_elements": ["Elementname"],
      "finding": "Prägnante sachliche Begründung des Befunds",
      "remediation_suggestion": "Konkreter Korrekturvorschlag für den XIMA Formcycle Designer"
    }}
  ]
}}
"""
    return prompt


def build_prompt(xfp_path: str, registry_path: str = "data/rules/rules_registry.json") -> str:
    with open(registry_path, "r", encoding="utf-8") as f:
        reg = json.load(f)
    payload = extract_compact_payload(xfp_path)
    return build_prompt_from_payload(payload, reg)


if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/test_forms/synthetic_noncompliant_form.xfp"
    if not os.path.exists(target) and target.endswith(".xfp"):
        target = target[:-4] + ".json"
    out_prompt = build_prompt(target)
    os.makedirs("data/prompts", exist_ok=True)
    out_file = os.path.join("data/prompts", f"chat_ai_prompt_{os.path.basename(target)}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_prompt)
    print(f"Prompt erfolgreich generiert ({len(out_prompt)} Zeichen): {out_file}")
