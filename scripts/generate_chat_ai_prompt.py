"""
Hilfsskript zur Erzeugung eines strukturierten Evaluations-Prompts (inkl. kompakter JSON-Extraktion)
für Web-Chat-Oberflächen wie die GWDG Academic Cloud Chat AI (ohne API-Zwang).
"""
import json
import zipfile
import os
import sys

def extract_compact_payload(xfp_path):
    workflow_emails = []
    if xfp_path.endswith(".json"):
        with open(xfp_path, "r", encoding="utf-8") as f:
            form_data = json.load(f)
        workflow_emails = form_data.get("workflow_emails", [])
    else:
        with zipfile.ZipFile(xfp_path) as z:
            fcp_name = [n for n in z.namelist() if n.endswith(".fcp")][0]
            form_data = json.loads(z.read(fcp_name).decode("utf-8", "ignore"))
            fcexports = [n for n in z.namelist() if n.endswith(".fcexport") and "/projects/" in n]
            for fce in fcexports:
                proj_data = json.loads(z.read(fce).decode("utf-8", "ignore"))
                def walk_nodes(obj):
                    if isinstance(obj, dict):
                        if obj.get("type") == "FC_EMAIL":
                            cp_str = obj.get("customParameters", "{}")
                            try:
                                cp = json.loads(cp_str) if isinstance(cp_str, str) else cp_str
                            except Exception:
                                cp = {}
                            workflow_emails.append({
                                "node_name": obj.get("name", ""),
                                "subject": cp.get("subject", ""),
                                "body": cp.get("body", "")[:400]
                            })
                        for v in obj.values():
                            walk_nodes(v)
                    elif isinstance(obj, list):
                        for item in obj:
                            walk_nodes(item)
                walk_nodes(proj_data)

    items = form_data.get("items", [])
    compact_elements = []
    page_count = 0
    input_count = 0
    input_classes = {"XTextField", "XTextArea", "XSelect", "XCheckbox", "XUpload", "XFile", "XRadio", "XDate", "XNumber"}

    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {})
        if c == "XPage":
            page_count += 1
        if c in input_classes:
            input_count += 1
        lbl = props.get("label") or props.get("text") or props.get("heading") or props.get("legend") or ""
        help_txt = props.get("help") or props.get("tooltip") or ""
        if lbl or help_txt or c in {"XButton", "XFooter"}:
            compact_elements.append({
                "className": c,
                "name": props.get("name", ""),
                "label_or_text": str(lbl)[:200],
                "help": str(help_txt)[:200]
            })

    return {
        "form_name": os.path.basename(xfp_path),
        "metrics": {
            "page_count": page_count,
            "input_field_count": input_count
        },
        "ui_elements": compact_elements,
        "workflow_emails": workflow_emails
    }

def build_prompt(xfp_path, registry_path="data/rules/rules_registry.json"):
    with open(registry_path, "r", encoding="utf-8") as f:
        reg = json.load(f)
    semantic_rules = [r for r in reg["rules"] if r.get("check_type") == "semantic"]
    payload = extract_compact_payload(xfp_path)

    prompt = f"""Du bist ein wissenschaftlicher Usability- und Compliance-Auditor für digitale Hochschulformulare (XIMA Formcycle) an der HWG Ludwigshafen.
Prüfe das nachfolgende extrahierte Formular-JSON strikt anhand der folgenden {len(semantic_rules)} semantischen Governance-Regeln aus der HWG-Compliance-Registry (v{reg['version']}):

=== SEMANTISCHE PRÜFREGELN ===
{json.dumps(semantic_rules, ensure_ascii=False, indent=2)}

=== ZU PRÜFENDES FORMULAR (KOMPAKTER EXTRAKT) ===
{json.dumps(payload, ensure_ascii=False, indent=2)}

=== AUFGABE ===
Antworte AUSSCHLIESSLICH mit einem validen JSON-Objekt im folgenden Schema:
{{
  "form_name": "{payload['form_name']}",
  "evaluated_rules": [
    {{
      "rule_id": "HWG-...",
      "status": "PASS | VIOLATION | RECOMMENDATION",
      "severity": "critical | major | minor | recommendation",
      "affected_elements": ["Elementname"],
      "finding": "Kurze Begründung des Befunds",
      "remediation_suggestion": "Konkreter Korrekturvorschlag für den Formcycle-Designer"
    }}
  ]
}}
"""
    return prompt

if __name__ == "__main__":
    target = sys.argv[1] if len(sys.argv) > 1 else "data/test_forms/synthetic_noncompliant_form.json"
    out_prompt = build_prompt(target)
    os.makedirs("data/prompts", exist_ok=True)
    out_file = os.path.join("data/prompts", f"chat_ai_prompt_{os.path.basename(target)}.txt")
    with open(out_file, "w", encoding="utf-8") as f:
        f.write(out_prompt)
    print(f"Prompt erfolgreich generiert ({len(out_prompt)} Zeichen): {out_file}")
