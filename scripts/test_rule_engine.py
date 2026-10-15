import json
import zipfile
import os
import re

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
    
    # Load JSON directly or unpack from .xfp
    if xfp_path.endswith(".json"):
        with open(xfp_path, "r", encoding="utf-8") as f:
            form_data = json.load(f)
    else:
        with zipfile.ZipFile(xfp_path) as z:
            fcp_name = [n for n in z.namelist() if n.endswith(".fcp")][0]
            form_data = json.loads(z.read(fcp_name).decode("utf-8", "ignore"))
        
    items = form_data.get("items", [])
    form_props = form_data.get("properties", {})
    
    widths = set()
    if "maxwidth" in form_props and form_props["maxwidth"]:
        widths.add(str(form_props["maxwidth"]))
    has_image = False
    has_fieldset = False
    missing_required_hints = []
    html_in_labels = []
    dev_notes = []
    button_labels = []
    
    # New dimensions tracking
    has_personal_data = False
    has_dsgvo_notice = False
    upload_elements = []
    structured_fields_unvalidated = []
    compact_fields_unconstrained = []
    jargon_without_help = []
    has_process_feedback = False
    
    jargon_catalog = [
        "gstb", "kostenstelle", "vergabevermerk", "remonstration", 
        "promotionsausschuss", "exmatrikulation", "shibboleth", 
        "kap", "mittelbewirtschafter"
    ]
    
    all_texts_combined = ""

    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {})
        name = str(props.get("name", "")).lower()
        lbl = str(props.get("label", "") or props.get("text", "") or props.get("heading", ""))
        lbl_lower = lbl.lower()
        help_text = str(props.get("help", "") or props.get("tooltip", "") or props.get("description", "")).lower()
        
        all_texts_combined += f" {lbl} {help_text} "
        
        # 1. Width
        if "maxwidth" in props and props["maxwidth"]:
            widths.add(str(props["maxwidth"]))
            
        # 2. CD-02: Header Image
        if c == "XImage":
            has_image = True
            
        # 3. A11Y-01: Fieldsets
        if c == "XFieldSet":
            has_fieldset = True
            
        # 4. A11Y-02: Required hints
        if props.get("showrequiredhint") == "0" and props.get("required") == "1":
            missing_required_hints.append(props.get("name", "unnamed"))
            
        # 5. A11Y-03: HTML in labels & Dev Notes
        for lk in ["label", "text", "heading"]:
            if lk in props and props[lk]:
                val = str(props[lk])
                if "<p>" in val or "&szlig;" in val or "&ouml;" in val or "|" in val:
                    html_in_labels.append((props.get("name"), val[:30]))
                if any(tech in val for tech in ["JavaScript", "Shibboleth", "LDAP-Member", "Postfach-SB"]):
                    dev_notes.append((props.get("name"), val[:40]))
                    
        # 6. Buttons
        if "Button" in c or c == "XButtonList":
            btn_lbl = props.get("label") or props.get("text") or props.get("heading") or ""
            btn_items = props.get("items", [])
            if isinstance(btn_items, list):
                for b in btn_items:
                    if isinstance(b, dict) and "text" in b:
                        button_labels.append(b["text"])
            if btn_lbl:
                button_labels.append(btn_lbl)
                
        # 7. Personal Data & DSGVO detection
        if any(term in name or term in lbl_lower for term in ["vorname", "nachname", "name", "email", "e-mail", "matrikel", "geburtsdatum", "iban", "anschrift"]):
            has_personal_data = True
            
        if any(term in lbl_lower or term in help_text for term in ["datenschutz", "dsgvo", "datenverarbeitung", "datenschutzerklärung", "hwg-lu.de"]):
            has_dsgvo_notice = True

        # 8. Upload specification
        if c in ["XUpload", "XFile", "XUploadButton"] or "upload" in name:
            has_formats = any(fmt in lbl_lower or fmt in help_text for fmt in ["pdf", "jpg", "png", "zip", "format", "dateiformat"])
            has_size = any(sz in lbl_lower or sz in help_text for sz in ["mb", "kb", "maximal", "größe", "dateigröße"])
            if not (has_formats and has_size):
                upload_elements.append({
                    "name": props.get("name", "upload"),
                    "has_formats": has_formats,
                    "has_size": has_size
                })

        # 9. Structured fields validation (IBAN, PLZ, Datum)
        if any(term in name or term in lbl_lower for term in ["iban", "plz", "postleitzahl", "telefon", "geburtsdatum"]):
            val_rule = props.get("validation", {})
            has_regex = bool(props.get("pattern") or (isinstance(val_rule, dict) and val_rule.get("regex")) or (isinstance(val_rule, dict) and val_rule.get("type")))
            if not has_regex:
                structured_fields_unvalidated.append(props.get("name", lbl[:15]))

        # 10. Compact fields width UX (e.g. PLZ, Hausnummer)
        if any(term in name or term in lbl_lower for term in ["plz", "postleitzahl", "hausnummer", "hnr"]):
            col_width = props.get("colwidth") or props.get("width")
            if col_width in ["100%", "12", None] and "maxwidth" not in props:
                compact_fields_unconstrained.append(props.get("name", lbl[:15]))

        # 11. Jargon without help
        for jg in jargon_catalog:
            if jg in lbl_lower:
                if not help_text or len(help_text.strip()) < 5:
                    jargon_without_help.append((jg, props.get("name", lbl[:15])))

    # 12. Process / Feedback transparency
    if any(term in all_texts_combined.lower() for term in ["bearbeitungsdauer", "bearbeitungszeit", "folgeschritte", "prüfungsphase", "nach dem absenden", "weiterer ablauf"]):
        has_process_feedback = True

    # Scoring calculation
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
    else:
        results["passed"].append("HWG-A11Y-03 (Saubere Labels)")

    # 5. HWG-UI-01: Keine Entwickler-Notizen
    if dev_notes:
        results["violations"].append({
            "rule": "HWG-UI-01",
            "severity": "critical",
            "message": f"Sichtbare Entwickler-Notizen / Skript-Reste im Frontend: {dev_notes}"
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-UI-01 (Keine Entwickler-Notizen)")

    # 6. HWG-STAMM-02: Standardisierte Stammdaten-Bezeichnungen
    non_canonical_master_labels = []
    for it in items:
        props = it.get("properties", {})
        lbl = str(props.get("label", "") or "").strip()
        name = str(props.get("name", "")).lower()
        if "email" in name or "mail" in name:
            if lbl and lbl not in ["E-Mail-Adresse", "E-Mail", "Hochschul-E-Mail"]:
                non_canonical_master_labels.append((lbl, "Erwartet: E-Mail-Adresse oder Hochschul-E-Mail"))
        if "nachname" in name or ("name" in name and "vorname" not in name and "antrag" not in name):
            if "antragstellende" in lbl.lower() or lbl == "Name":
                non_canonical_master_labels.append((lbl, "Erwartet: Nachname"))

    if non_canonical_master_labels:
        results["violations"].append({
            "rule": "HWG-STAMM-02",
            "severity": "minor",
            "message": f"Nicht-standardisierte Stammdaten-Bezeichnungen gefunden: {non_canonical_master_labels[:2]}"
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-STAMM-02 (Kanonische Stammdaten-Labels)")

    # 7. HWG-BTN-01: Aktionsorientierte Schaltflächen-Semantik (Action-Verb-Pattern)
    invalid_buttons = []
    for b in button_labels:
        b_clean = b.strip()
        b_lower = b_clean.lower()
        # Bare state or generic minimal label
        if b_clean in ["Kritischer Fall", "Status", "Genehmigung", "Fehler"]:
            invalid_buttons.append((b_clean, "Reine Status-/Zustandsbezeichnung ohne Handlungsverb"))
        elif b_lower in ["senden", "submit", "ok", "abschicken"]:
            invalid_buttons.append((b_clean, "Generisches Minimal-Label ohne Zielobjekt"))

    if invalid_buttons:
        results["violations"].append({
            "rule": "HWG-BTN-01",
            "severity": "major",
            "message": f"Schaltflächen verletzen das Action-Verb-Muster: {invalid_buttons}"
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-BTN-01 (Aktionsorientierte Schaltflächen)")

    # 8. HWG-DSGVO-01
    if has_personal_data and not has_dsgvo_notice:
        results["violations"].append({
            "rule": "HWG-DSGVO-01",
            "severity": "critical",
            "message": "Personenbezogene Daten werden erhoben, aber es fehlt ein Datenschutz-Hinweis / DSGVO-Link."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-DSGVO-01 (Datenschutz-Hinweis vorhanden oder keine Personendaten)")

    # 9. HWG-UPLOAD-01
    if upload_elements:
        results["violations"].append({
            "rule": "HWG-UPLOAD-01",
            "severity": "major",
            "message": f"{len(upload_elements)} Dateiupload-Element(e) ohne transparente Angabe von Dateiformat und/oder Maximalgröße."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-UPLOAD-01 (Uploads spezifiziert oder keine Uploads)")

    # 10. HWG-VAL-01
    if structured_fields_unvalidated:
        results["violations"].append({
            "rule": "HWG-VAL-01",
            "severity": "major",
            "message": f"Strukturierte Felder ohne Validierungsregel gefunden: {structured_fields_unvalidated[:3]}"
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-VAL-01 (Strukturierte Felder validiert)")

    # 11. HWG-UX-01
    if compact_fields_unconstrained:
        results["violations"].append({
            "rule": "HWG-UX-01",
            "severity": "minor",
            "message": f"Kompakte Felder (PLZ/Hausnummer) ohne Breitenbegrenzung über volle Breite gestreckt: {compact_fields_unconstrained[:2]}"
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-UX-01 (Affordanzgerechte Feldbreiten)")

    # 12. HWG-LANG-01
    if jargon_without_help:
        results["violations"].append({
            "rule": "HWG-LANG-01",
            "severity": "major",
            "message": f"Hochschul-Jargon ohne erläuternden Hilfetext gefunden: {[f'{j[0]} in {j[1]}' for j in jargon_without_help[:2]]}"
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-LANG-01 (Verständlicher Wortschatz)")

    # 13. HWG-FEEDBACK-01
    if not has_process_feedback:
        results["violations"].append({
            "rule": "HWG-FEEDBACK-01",
            "severity": "minor",
            "message": "Keine transparenten Informationen über Bearbeitungszeit oder nachgelagerte Folgeschritte hinterlegt."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-FEEDBACK-01 (Prozesstransparenz vorhanden)")

    results["score"] = max(0, results["score"])
    return results

if __name__ == "__main__":
    reg = load_rules()
    
    test_forms = [
        "data/test_forms/synthetic_compliant_form.json",
        "data/test_forms/synthetic_noncompliant_form.json",
        "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
        "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
        "data/raw_forms/test/adminformulare/Master-Formular.xfp"
    ]
    
    print(f"=== COMPLIANCE REGISTRY EVALUATION (Registry Version {reg['version']}) ===")
    print(f"Gesamtanzahl definierter Regeln: {len(reg['rules'])}\n")
    
    for tf in test_forms:
        res = evaluate_form(tf, reg)
        print(f"\n{'='*25} {res['form']} {'='*25}")
        print(f"Compliance-Score: {res['score']} / 100 Punkte")
        print(f"Bestandene Prüfungen: {len(res['passed'])}")
        print(f"Gefundene Verstöße:   {len(res['violations'])}")
        for v in res['violations']:
            print(f"  [X] [{v['severity'].upper():8}] {v['rule']}: {v['message']}")
