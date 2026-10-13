import json
import zipfile
import os

def load_rules(registry_path="data/rules/rules_registry.json"):
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)

def evaluate_form(xfp_path, registry):
    results = {
        "form": os.path.basename(xfp_path),
        "violations": [],
        "passed": [],
        "score": 100
    }
    
    # Unpack .fcp
    with zipfile.ZipFile(xfp_path) as z:
        fcp_name = [n for n in z.namelist() if n.endswith(".fcp")][0]
        form_data = json.loads(z.read(fcp_name).decode("utf-8", "ignore"))
        
    items = form_data.get("items", [])
    
    # Rule CD-01: Layout Width
    # Check maxwidth property in items or form
    widths = set()
    has_image = False
    has_fieldset = False
    missing_required_hints = []
    html_in_labels = []
    dev_notes = []
    button_labels = []
    
    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {})
        
        # Width
        if "maxwidth" in props and props["maxwidth"]:
            widths.add(str(props["maxwidth"]))
            
        # CD-02: Header Image
        if c == "XImage":
            has_image = True
            
        # A11Y-01: Fieldsets
        if c == "XFieldSet":
            has_fieldset = True
            
        # A11Y-02: Required hints
        if props.get("showrequiredhint") == "0" and props.get("required") == "1":
            missing_required_hints.append(props.get("name", "unnamed"))
            
        # A11Y-03: HTML in labels
        for lk in ["label", "text", "heading"]:
            if lk in props and props[lk]:
                val = str(props[lk])
                if "<p>" in val or "&szlig;" in val or "&ouml;" in val or "|" in val:
                    html_in_labels.append((props.get("name"), val[:30]))
                if any(tech in val for tech in ["JavaScript", "Shibboleth", "LDAP-Member", "Postfach-SB"]):
                    dev_notes.append((props.get("name"), val[:40]))
                    
        # Buttons
        if "Button" in c or c == "XButtonList":
            lbl = props.get("label") or props.get("text") or props.get("heading") or ""
            btn_items = props.get("items", [])
            if isinstance(btn_items, list):
                for b in btn_items:
                    if isinstance(b, dict) and "text" in b:
                        button_labels.append(b["text"])
            if lbl:
                button_labels.append(lbl)

    # Evaluate rules against findings
    penalties = registry["scoring"]["severity_penalties"]
    
    # 1. HWG-CD-01
    if "700px" in widths and "850px" not in widths:
        results["violations"].append({
            "rule": "HWG-CD-01",
            "severity": "major",
            "message": "Formular verwendet veraltete 700px-Breite statt dem 850px-Standard."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-CD-01 (Breite 850px eingehalten)")

    # 2. HWG-CD-02
    if not has_image:
        results["violations"].append({
            "rule": "HWG-CD-02",
            "severity": "critical",
            "message": "Kein offizielles HWG-Header-Banner (XImage) im Kopfbereich vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-CD-02 (Header-Logo vorhanden)")

    # 3. HWG-A11Y-01
    if not has_fieldset and len(items) > 20:
        results["violations"].append({
            "rule": "HWG-A11Y-01",
            "severity": "critical",
            "message": "Keine semantischen XFieldSet-Gruppierungen für Formularabschnitte vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-A11Y-01 (Fieldsets vorhanden)")

    # 4. HWG-A11Y-03
    if html_in_labels:
        results["violations"].append({
            "rule": "HWG-A11Y-03",
            "severity": "minor",
            "message": f"HTML-Fragmente oder Entities in {len(html_in_labels)} Label(s) gefunden: {html_in_labels[:2]}"
        })
        results["score"] -= penalties["minor"]

    # 5. HWG-STAMM-03
    if dev_notes:
        results["violations"].append({
            "rule": "HWG-STAMM-03",
            "severity": "critical",
            "message": f"Sichtbare Entwickler-Notizen / Skript-Reste im Frontend: {dev_notes}"
        })
        results["score"] -= penalties["critical"]

    # 6. HWG-BTN-03
    if any("Kritischer Fall" in b for b in button_labels):
        results["violations"].append({
            "rule": "HWG-BTN-03",
            "severity": "critical",
            "message": "Unzulässige Statusbezeichnung 'Kritischer Fall' als Schaltflächen-Label verwendet."
        })
        results["score"] -= penalties["critical"]

    # 7. HWG-BTN-01
    if any(b.strip() == "senden" for b in button_labels):
        results["violations"].append({
            "rule": "HWG-BTN-01",
            "severity": "major",
            "message": "Absende-Button verwendet kleingeschriebenes generisches 'senden' statt 'Antrag einreichen'."
        })
        results["score"] -= penalties["major"]

    results["score"] = max(0, results["score"])
    return results

if __name__ == "__main__":
    reg = load_rules()
    
    test_forms = [
        "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
        "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
        "data/raw_forms/test/adminformulare/Master-Formular.xfp"
    ]
    
    for tf in test_forms:
        res = evaluate_form(tf, reg)
        print(f"\n{'='*20} {res['form']} {'='*20}")
        print(f"Compliance-Score: {res['score']} / 100 Punkte")
        print("Erfolgreich geprüfte Regeln:", len(res['passed']))
        print("Gefundene Verstöße:", len(res['violations']))
        for v in res['violations']:
            print(f"  [X] [{v['severity'].upper()}] {v['rule']}: {v['message']}")
