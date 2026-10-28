"""
Erzeugung eines strukturierten Evaluations-Prompts (inkl. kontextoptimierter JSON-Extraktion
und deterministischer AST-Vorabmetriken) für Stufe 2 der hybriden Compliance-Pipeline
(OpenAI-kompatible REST-API der GWDG Academic Cloud sowie Web-Chat-Evaluation).
"""
import html
import io
import json
import os
import re
import sys
import zipfile


INPUT_CLASSES = {
    "XTextField", "XTextArea", "XSelect", "XCheckbox",
    "XUpload", "XFile", "XRadio", "XDate", "XNumber"
}

ABBREV_PATTERN = re.compile(
    r"\b(?:z\.\s*B\.|u\.\s*a\.|d\.\s*h\.|bzw\.|gem\.|Art\.|Abs\.|Nr\.|max\.|min\.|ca\.|inkl\.|ggf\.|etc\.|Prof\.|Dr\.|bspw\.|vgl\.|sog\.)",
    re.IGNORECASE,
)


def decode_text_bytes(raw_bytes: bytes) -> str:
    try:
        return raw_bytes.decode("utf-8")
    except UnicodeDecodeError:
        return raw_bytes.decode("cp1252", errors="replace")


def clean_visible_text(raw: str) -> str:
    if not raw:
        return ""
    unescaped = html.unescape(str(raw))
    stripped = re.sub(r"<[^>]+>", " ", unescaped)
    return " ".join(stripped.split()).strip()


def extract_long_sentences(items, max_words: int = 25):
    long_sents = []
    for it in items:
        props = it.get("properties", {}) or {}
        elem_name = str(props.get("name") or "unnamed")
        for key in ("text", "rtevalue", "helptext", "help", "tooltip", "description"):
            val = str(props.get(key) or "")
            if not val:
                continue
            txt = clean_visible_text(val)
            # URLs und Platzhalter neutralisieren, Abkürzungspunkte schützen
            txt_no_url = re.sub(r"https?://\S+|www\.\S+", "URL", txt)
            txt_safe = ABBREV_PATTERN.sub(lambda m: m.group(0).replace(".", ""), txt_no_url)
            for sent in re.split(r"[.!?]+", txt_safe):
                words = [w for w in sent.strip().split() if re.search(r"[A-Za-zÄÖÜäöüß0-9]", w)]
                if len(words) > max_words:
                    long_sents.append({
                        "element": elem_name,
                        "property": key,
                        "word_count": len(words),
                        "preview": " ".join(words[:12]) + " ..."
                    })
    return long_sents


def classify_button_role(action_page: str, btn_type: str = "") -> str:
    ap = str(action_page or "").strip()
    ap_low = ap.lower()
    bt_low = str(btn_type or "").strip().lower()
    if ap_low in ("next", "prev", "xnavbar_next", "xnavbar_prev") or re.match(r"^p\d+$", ap_low):
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
    items = form_data.get("items", []) or []

    # Sichtbarkeitskarte (Elemente mit rein internem viewstatus ohne '-1' markieren)
    id_to_item = {}
    for it in items:
        p = it.get("properties", {}) or {}
        iid = str(p.get("id") or p.get("name") or "")
        if iid:
            id_to_item[iid] = p

    def is_applicant_visible(props: dict) -> bool:
        curr = props
        visited = set()
        for _ in range(6):
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

    compact_elements = []
    buttons_extracted = []
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
        elem_name = str(props.get("name", ""))

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
            compact_elements.append({
                "className": c,
                "name": elem_name,
                "label_or_text": lbl[:240],
                "helptext": help_txt[:240],
            })

    effective_page_count = max(1, raw_xpage_count)
    applicant_items = [it for it in items if is_applicant_visible(it.get("properties", {}) or {})]
    long_sentences = extract_long_sentences(applicant_items, max_words=25)

    return {
        "form_name": form_name,
        "metrics": {
            "page_count": effective_page_count,
            "raw_xpage_count": raw_xpage_count,
            "input_field_count": input_count,
            "upload_field_count": upload_count,
            "ux02_complexity_threshold_reached": bool(effective_page_count >= 3 or input_count >= 25),
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
   - HWG-UX-02: Nur wenn metrics.ux02_complexity_threshold_reached == true ist und kein Zwischenspeichern-Mechanismus existiert, setze status = "RECOMMENDATION" (0 Punkte Abzug). Ist ux02_complexity_threshold_reached == false, setze status = "NOT_APPLICABLE".
   - HWG-BTN-02: Nur wenn metrics.page_count > 1 ist, prüfe Schaltflächen mit role == "pagination" auf exakte Benennung ("Weiter" / "Zurück"). Bei einseitigen Formularen (metrics.page_count <= 1) setze status = "NOT_APPLICABLE".
   - HWG-LANG-02: Berücksichtige metrics.sentences_over_25_words; wenn dort keine Sätze > 25 Wörter vorliegen und keine extrem verschachtelten Passivkonstruktionen existieren, setze status = "PASS".
3. HWG-STAMM-02: Für E-Mail-Felder sind "E-Mail-Adresse", "E-Mail" und "Hochschul-E-Mail" zulässig. Persönliche Namensfelder müssen getrennt als "Vorname" und "Nachname" benannt sein ("Name Antragstellende/r", "Name" oder technische Kürzel wie "HWGLU-Email" sind Verstöße).
4. HWG-BTN-01: Prüfe Aktions- und Absendeschaltflächen (role != "pagination") auf das Action-Verb-Muster ([Zielobjekt] + [Vollverb im Infinitiv]). Formulierungen mit klarem Handlungsverb wie "Antrag einreichen" oder "Kritischen Fall einreichen" sind ZULÄSSIG; reine Zustandsbegriffe ohne Verb ("Kritischer Fall") oder kontextlose Ein-Wort-Labels ("senden", "Submit", "OK") sind Verstöße.
5. Halluziniere keine Mängel hinzu, die nicht im Extrakt belegt sind.

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
    target = sys.argv[1] if len(sys.argv) > 1 else "data/test_forms/synthetic_noncompliant_form.json"
    out_prompt = build_prompt(target)
    os.makedirs("data/prompts", exist_ok=True)
    out_file = os.path.join("data/prompts", f"chat_ai_prompt_{os.path.basename(target)}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_prompt)
    print(f"Prompt erfolgreich generiert ({len(out_prompt)} Zeichen): {out_file}")
