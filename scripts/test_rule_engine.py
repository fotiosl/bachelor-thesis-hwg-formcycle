import json
import zipfile
import os
import re

def load_rules(registry_path="data/rules/rules_registry.json"):
    with open(registry_path, "r", encoding="utf-8") as f:
        return json.load(f)

def extract_workflow_emails_and_states_from_fcexport(proj_data):
    emails = []
    states = []
    def walk_nodes(obj):
        if isinstance(obj, dict):
            if obj.get("type") == "FC_EMAIL":
                cp_str = obj.get("customParameters", "{}")
                try:
                    cp = json.loads(cp_str) if isinstance(cp_str, str) else cp_str
                except Exception:
                    cp = {}
                emails.append({
                    "node_name": obj.get("name", ""),
                    "subject": cp.get("subject", ""),
                    "body": cp.get("body", "")
                })
            elif obj.get("type") in ["FC_CHANGE_STATE", "CUSTOM", "RECEIVED"]:
                st_name = obj.get("name", "")
                if st_name and st_name != "FC_CHANGE_STATE":
                    states.append(st_name)
            for v in obj.values():
                walk_nodes(v)
        elif isinstance(obj, list):
            for item in obj:
                walk_nodes(item)
    walk_nodes(proj_data)
    
    # Deduplicate states preserving order
    dedup_states = []
    for s in states:
        if s not in dedup_states:
            dedup_states.append(s)
    return emails, dedup_states

def evaluate_form(xfp_path, registry):
    results = {
        "form": os.path.basename(xfp_path),
        "violations": [],
        "recommendations": [],
        "passed": [],
        "not_applicable": {},
        "score": 100
    }
    
    workflow_emails = []
    workflow_states = []
    # Load JSON directly or unpack from .xfp
    if xfp_path.endswith(".json"):
        with open(xfp_path, "r", encoding="utf-8") as f:
            form_data = json.load(f)
        workflow_emails = form_data.get("workflow_emails", [])
        workflow_states = form_data.get("workflow_states", [])
    else:
        with zipfile.ZipFile(xfp_path) as z:
            fcp_candidates = [n for n in z.namelist() if n.endswith(".fcp")]
            if not fcp_candidates:
                raise ValueError(f"Keine .fcp Modelldatei im Formulararchiv '{os.path.basename(xfp_path)}' gefunden.")
            fcp_name = fcp_candidates[0]
            form_data = json.loads(z.read(fcp_name).decode("utf-8", "ignore"))
            fcexports = [n for n in z.namelist() if n.endswith(".fcexport") and ("/projects/" in n or "\\projects\\" in n) and "idcheck" not in n and "versions" not in n]
            for fce in fcexports:
                proj_data = json.loads(z.read(fce).decode("utf-8", "ignore"))
                ems, sts = extract_workflow_emails_and_states_from_fcexport(proj_data)
                workflow_emails.extend(ems)
                workflow_states.extend(sts)
        
    items = form_data.get("items", [])
    form_props = form_data.get("properties", {})
    
    widths = set()
    if "maxwidth" in form_props and form_props["maxwidth"]:
        widths.add(str(form_props["maxwidth"]))
    has_image = False
    image_props = {}
    has_header_title_h1 = False
    header_title_details = None
    has_fieldset = False
    footer_shows_logo = False
    
    # Required fields (HWG-A11Y-02)
    required_fields_total = 0
    missing_required_hints = []
    manual_asterisks_in_labels = []
    
    # HTML in labels & Dev Notes (HWG-A11Y-03, HWG-UI-01)
    html_in_labels = []
    dev_notes = []
    
    # Buttons (HWG-BTN-01, HWG-BTN-02, HWG-UX-02)
    button_labels = []
    nav_button_labels = []
    has_save_button = False
    
    # Complexity tracking (HWG-UX-02)
    page_count = 0
    input_field_count = 0
    input_classes = {
        "XTextField", "XTextArea", "XSelect", "XCheckbox", 
        "XUpload", "XFile", "XRadio", "XDate", "XNumber"
    }
    
    # Master data sequence tracking (HWG-STAMM-01)
    personal_fields_sequence = []
    
    # Dimensions tracking
    has_personal_data = False
    has_dsgvo_notice = False
    upload_elements = []
    has_upload_elements = False
    structured_fields_unvalidated = []
    compact_fields_unconstrained = []
    has_compact_fields = False
    jargon_without_help = []
    long_sentences = []
    
    jargon_catalog = [
        "gstb", "kostenstelle", "vergabevermerk", "remonstration", 
        "promotionsausschuss", "exmatrikulation", "shibboleth", "ldap",
        "kap", "mittelbewirtschafter", "mittelgeber", "verausgabt", 
        "verausgabung", "zfk", "haushaltsstelle", "bewilligungszeitraum", 
        "titelgruppe", "drittmittel"
    ]

    for it in items:
        c = it.get("className", "")
        props = it.get("properties", {})
        name = str(props.get("name", "")).lower()
        lbl = str(props.get("label", "") or props.get("text", "") or props.get("heading", ""))
        lbl_clean = re.sub(r"<[^>]+>", " ", lbl).strip()
        lbl_lower = lbl_clean.lower()
        help_text = str(props.get("help", "") or props.get("tooltip", "") or props.get("description", "")).lower()
        
        if c == "XPage":
            page_count += 1
        if c in input_classes:
            input_field_count += 1
            
        # 1. Width
        if "maxwidth" in props and props["maxwidth"]:
            widths.add(str(props["maxwidth"]))
            
        # 2. CD-02: Header Image
        if c == "XImage":
            has_image = True
            image_props = props

        # 2c. CD-04: Header Title (H1)
        parent_id = str(props.get("parentid", "")).lower()
        rte = str(props.get("rtevalue", "") or "")
        heading = str(props.get("heading", "") or "")
        label = str(props.get("label", "") or "")
        text = str(props.get("text", "") or "")
        lvl = str(props.get("headinglevel", "") or "")
        is_header = "header" in parent_id or c == "XHeader" or "header" in name
        all_heading_text = f"{rte} {heading} {label} {text}"
        
        if is_header or "header" in name or "titel" in name or "title" in name:
            if "<h1" in all_heading_text.lower() or lvl == "1":
                has_header_title_h1 = True
            elif "<h2" in all_heading_text.lower() or "<h3" in all_heading_text.lower() or "antrag" in all_heading_text.lower() or "title" in name or "titel" in name:
                if not has_header_title_h1:
                    header_title_details = "h2_or_text"
            
        # 2b. CD-03: Footer XIMA Logo
        if c == "XFooter":
            if str(props.get("showlogo", "0")) == "1":
                footer_shows_logo = True
            
        # 3. A11Y-01: Fieldsets
        if c == "XFieldSet":
            has_fieldset = True
            
        # 4. A11Y-02: Required fields
        if c in input_classes:
            is_req = str(props.get("required", "0")) == "1"
            show_hint = str(props.get("showrequiredhint", "1"))
            if is_req:
                required_fields_total += 1
                if show_hint == "0":
                    missing_required_hints.append(props.get("name", "unnamed"))
            elif "*" in lbl_clean:
                manual_asterisks_in_labels.append(props.get("name", "unnamed"))
            
        # 5. A11Y-03: HTML in labels & Dev Notes
        for lk in ["label", "text", "heading"]:
            if lk in props and props[lk]:
                val = str(props[lk])
                clean_val = " ".join(val.split())
                if re.search(r"<[^>]+>", val) or re.search(r"&[a-zA-Z0-9#]+;", val) or "|" in val:
                    html_in_labels.append((props.get("name", "unnamed"), clean_val[:35]))
                if any(tech in val for tech in ["JavaScript", "Shibboleth", "LDAP-Member", "Postfach-SB"]):
                    dev_notes.append((props.get("name", "unnamed"), clean_val[:40]))
                    
        # 6. Buttons
        if "Button" in c or c == "XButtonList":
            # XButtonList buttons property
            b_list = props.get("buttons", [])
            if isinstance(b_list, list) and b_list:
                for b in b_list:
                    val = b.get("value") or b.get("text") or b.get("title") or ""
                    if val:
                        button_labels.append((props.get("name", "btn"), val))
                        if b.get("action", {}).get("page") in ["next", "prev"] or "weiter" in val.lower() or "zurück" in val.lower() or "zurueck" in val.lower():
                            nav_button_labels.append(val)
            # Standalone button properties
            btn_lbl = props.get("text") or props.get("label") or props.get("value") or ""
            if btn_lbl:
                button_labels.append((props.get("name", "btn"), btn_lbl))
                if "weiter" in btn_lbl.lower() or "zurück" in btn_lbl.lower() or "zurueck" in btn_lbl.lower():
                    nav_button_labels.append(btn_lbl)
            btn_items = props.get("items", [])
            if isinstance(btn_items, list):
                for b in btn_items:
                    if isinstance(b, dict):
                        val = b.get("text") or b.get("value") or b.get("title") or ""
                        if val:
                            button_labels.append((props.get("name", "btn"), val))
                    elif isinstance(b, str) and b:
                        button_labels.append((props.get("name", "btn"), b))
                        
            for _, bl in button_labels:
                if any(s in bl.lower() for s in ["zwischenspeichern", "speichern", "fortsetzen"]):
                    has_save_button = True
                if str(props.get("type", "")).lower() == "save":
                    has_save_button = True

        # Master Data Sequence (HWG-STAMM-01)
        if c in input_classes:
            elem_name = props.get("name", "unnamed")
            # Only classify personal identity fields
            if any(term in name or term in lbl_lower for term in ["anrede", "salutation"]):
                personal_fields_sequence.append(("anrede", elem_name, lbl_clean or "Anrede", 1))
            elif "vorname" in name or "vorname" in lbl_lower:
                personal_fields_sequence.append(("vorname", elem_name, lbl_clean or "Vorname", 2))
            elif "nachname" in name or "nachname" in lbl_lower or ("name" in name and not any(t in name for t in ["vorname", "antrag", "bank", "kredit", "projekt", "programm", "foerder", "titel", "datei"])):
                personal_fields_sequence.append(("nachname", elem_name, lbl_clean or "Nachname", 3))
            elif lbl_clean.lower() == "name" or "name antragstellende" in lbl_lower or "name antragsteller" in lbl_lower:
                personal_fields_sequence.append(("nachname", elem_name, lbl_clean or "Nachname", 3))
            elif any(term in name or term in lbl_lower for term in ["email", "e-mail", "mail"]):
                personal_fields_sequence.append(("email", elem_name, lbl_clean or "E-Mail-Adresse", 4))
            elif any(term in name or term in lbl_lower for term in ["telefon", "telefonnummer", "phone", "mobil"]):
                personal_fields_sequence.append(("telefon", elem_name, lbl_clean or "Telefonnummer", 5))

        # 7. Personal Data & DSGVO detection
        if any(term in name or term in lbl_lower for term in ["vorname", "nachname", "name", "email", "e-mail", "matrikel", "geburtsdatum", "iban", "anschrift"]):
            has_personal_data = True
            
        raw_dsgvo_ctx = f"{lbl_lower} {help_text} {str(props.get('rtevalue', '')).lower()} {str(props.get('html', '')).lower()}"
        if any(term in raw_dsgvo_ctx for term in ["datenschutz", "dsgvo", "datenverarbeitung", "datenschutzerklärung", "hwg-lu.de"]):
            has_dsgvo_notice = True
        if c == "XFooter" and str(props.get("privacyPolicyShow", "0")) == "1":
            has_dsgvo_notice = True

        # 8. Upload specification
        if c in ["XUpload", "XFile", "XUploadButton"] or "upload" in name:
            has_upload_elements = True
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
            has_compact_fields = True
            col_width = props.get("colwidth") or props.get("width")
            if col_width in ["100%", "12", None] and "maxwidth" not in props:
                compact_fields_unconstrained.append(props.get("name", lbl[:15]))

        # 11. Jargon without help
        for jg in jargon_catalog:
            matched = bool(re.search(rf"\b{re.escape(jg)}\b", lbl_lower)) if len(jg) <= 4 else (jg in lbl_lower)
            if matched:
                if not help_text or len(help_text.strip()) < 5:
                    jargon_without_help.append((jg, props.get("name", lbl[:15])))

        # 12. Sentence length (HWG-LANG-02)
        for k in ["text", "help", "tooltip", "description", "rtevalue"]:
            val = str(props.get(k) or "")
            if val:
                clean_t = re.sub(r"<[^>]+>", " ", val)
                for sent in re.split(r"[.!?]+", clean_t):
                    words = [w for w in sent.strip().split() if len(w) > 1]
                    if len(words) > 25:
                        long_sentences.append((props.get("name", "unnamed"), len(words), " ".join(words[:8]) + "..."))

    # Process / Feedback transparency via Workflow E-Mails (HWG-FEEDBACK-01)
    has_workflow_feedback = False
    for em in workflow_emails:
        em_text = f"{em.get('subject', '')} {em.get('body', '')}".lower()
        if any(term in em_text for term in [
            "vielen dank", "eingegangen", "geprüft", "prüfung", "entscheidung", 
            "folgeschritte", "bearbeit", "rückmeldung", "vorgangsnummer", "project_alias"
        ]):
            has_workflow_feedback = True
            break

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

    # 2. HWG-CD-02 (Header-Logo mit 60px Höhe und rechtsbündig)
    if not has_image:
        results["violations"].append({
            "rule": "HWG-CD-02",
            "severity": "critical",
            "message": "Kein offizielles HWG-Header-Banner (XImage) im Kopfbereich vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        img_h = str(image_props.get("imageheight") or image_props.get("height") or "").strip().lower()
        img_align = str(image_props.get("textalign") or image_props.get("align") or "").strip().lower()
        is_height_60 = img_h in ["60", "60px"]
        is_right_aligned = img_align in ["right", "2"]
        
        if not is_height_60 or not is_right_aligned:
            issues = []
            if not is_height_60:
                issues.append(f"Höhe (in px) ist '{img_h or 'undefiniert'}' statt 60px")
            if not is_right_aligned:
                issues.append(f"Ausrichtung ist '{img_align or 'links'}' statt rechtsbündig")
            results["violations"].append({
                "rule": "HWG-CD-02",
                "severity": "major",
                "message": f"HWG-Header-Logo weicht von den Formatvorgaben ab: {', '.join(issues)}."
            })
            results["score"] -= penalties["major"]
        else:
            results["passed"].append("HWG-CD-02 (Header-Logo mit 60px Höhe, rechtsbündig vorhanden)")

    # 2b. HWG-CD-03 (XIMA Footer Logo)
    if footer_shows_logo:
        results["violations"].append({
            "rule": "HWG-CD-03",
            "severity": "major",
            "message": "Im Footer (XFooter) ist 'Logo anzeigen' (showlogo='1') aktiviert ('Powered by XIMA Formcycle')."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-CD-03 (XIMA-Logo im Footer deaktiviert)")

    # 2c. HWG-CD-04 (Formulartitel im Header als H1)
    if has_header_title_h1:
        results["passed"].append("HWG-CD-04 (Formulartitel im Header als H1 vorhanden)")
    else:
        if header_title_details == "h2_or_text":
            msg = "Formulartitel im Header ist nicht als Überschrift erster Ordnung (H1) ausgezeichnet (gefunden: H2 oder Fließtext statt <h1>)."
        else:
            msg = "Kein Formulartitel im Kopfbereich (Header) vorhanden. Der Antragstitel muss im Header als H1 deklariert werden."
        results["violations"].append({
            "rule": "HWG-CD-04",
            "severity": "major",
            "message": msg
        })
        results["score"] -= penalties["major"]

    # 3. HWG-A11Y-01 (Fieldsets)
    if has_fieldset:
        results["passed"].append("HWG-A11Y-01 (Fieldsets vorhanden: Semantische Gruppenbildung erfüllt)")
    elif len(items) > 20:
        results["violations"].append({
            "rule": "HWG-A11Y-01",
            "severity": "critical",
            "message": "Keine semantischen XFieldSet-Gruppierungen für Formularabschnitte vorhanden."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-A11Y-01 (Kompaktformular <= 20 Elemente: Keine Abschnittsbildung per Fieldset erforderlich)")

    # 4. HWG-A11Y-02 (Pflichtfeld-Deklaration mit Sternchen & aria-required)
    if missing_required_hints or manual_asterisks_in_labels:
        issues = []
        if missing_required_hints:
            issues.append(f"Optischer Hinweis deaktiviert (showrequiredhint='0') in {missing_required_hints}")
        if manual_asterisks_in_labels:
            issues.append(f"Manuelles Sternchen (*) im Label ohne native Pflichtfeldfunktion in {manual_asterisks_in_labels}")
        results["violations"].append({
            "rule": "HWG-A11Y-02",
            "severity": "major",
            "message": f"Pflichtfeld-Deklaration verletzt: {'; '.join(issues)}."
        })
        results["score"] -= penalties["major"]
    elif required_fields_total > 0:
        results["passed"].append(f"HWG-A11Y-02 (Pflichtfeld-Deklaration: {required_fields_total} Pflichtfelder mit optischem Hinweis und barrierefreiem aria-required deklariert)")
    else:
        results["not_applicable"]["HWG-A11Y-02"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Pflichtfelder im Formular deklariert."

    # 5. HWG-A11Y-03 (HTML in Labels)
    if html_in_labels:
        affected_fields = [h[0] for h in html_in_labels]
        names_preview = ", ".join(affected_fields[:6]) + (f" und {len(affected_fields)-6} weitere" if len(affected_fields) > 6 else "")
        results["violations"].append({
            "rule": "HWG-A11Y-03",
            "severity": "minor",
            "message": f"HTML-Fragmente oder Entities in {len(html_in_labels)} Label(s) gefunden: [{names_preview}]."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-A11Y-03 (Saubere Labels ohne HTML-Fragmente und Entities)")

    # 6. HWG-STAMM-01 (Einheitliche Abfolge persönlicher Stammdaten)
    if len(personal_fields_sequence) >= 2:
        out_of_order = []
        for i in range(len(personal_fields_sequence) - 1):
            curr = personal_fields_sequence[i]
            nxt = personal_fields_sequence[i+1]
            if nxt[0] == "anrede" and curr[0] in ["email", "telefon"]:
                continue
            if curr[3] > nxt[3]: # e.g. Nachname (3) before Vorname (2)
                out_of_order.append(f"'{curr[2]}' ({curr[0]}) vor '{nxt[2]}' ({nxt[0]})")
        if out_of_order:
            results["violations"].append({
                "rule": "HWG-STAMM-01",
                "severity": "major",
                "message": f"Inkonsistente Abfolge persönlicher Stammdaten: {', '.join(out_of_order)}. Erwartete Reihenfolge: Anrede -> Vorname -> Nachname -> E-Mail-Adresse -> Telefonnummer."
            })
            results["score"] -= penalties["major"]
        else:
            results["passed"].append("HWG-STAMM-01 (Kanonische Stammdaten-Abfolge eingehalten)")
    else:
        results["not_applicable"]["HWG-STAMM-01"] = (
            "Kriterium auf diesen Formularkontext nicht anwendbar: Keine oder weniger als 2 persönliche Stammdatenfelder vorhanden. "
            "Hinweis: Achten Sie bei der Erhebung von Stammdaten stets auf die kanonische Abfolge: Anrede -> Vorname -> Nachname -> E-Mail-Adresse -> Telefonnummer."
        )

    # 7. HWG-STAMM-02: Standardisierte Stammdaten-Bezeichnungen
    non_canonical_master_labels = []
    for it in items:
        props = it.get("properties", {})
        raw_lbl = str(props.get("label", "") or "").strip()
        lbl = re.sub(r"<[^>]+>", "", raw_lbl).strip()
        name = str(props.get("name", "")).lower()
        if "email" in name or "mail" in name:
            if lbl and lbl not in ["E-Mail-Adresse", "E-Mail", "Hochschul-E-Mail"]:
                non_canonical_master_labels.append((lbl, "Erwartet: E-Mail-Adresse oder Hochschul-E-Mail"))
        if "nachname" in name or ("name" in name and "vorname" not in name and "antrag" not in name and "bank" not in name and "kredit" not in name and "projekt" not in name and "programm" not in name and "foerder" not in name):
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

    # 8. HWG-UI-01: Keine Entwickler-Notizen
    if dev_notes:
        results["violations"].append({
            "rule": "HWG-UI-01",
            "severity": "critical",
            "message": f"Sichtbare Entwickler-Notizen / Skript-Reste im Frontend: {dev_notes}"
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-UI-01 (Keine Entwickler-Notizen)")

    # 9. HWG-BTN-01: Aktionsorientierte Schaltflächen-Semantik (Action-Verb-Pattern)
    invalid_buttons = []
    for btn_source, b in button_labels:
        b_clean = b.strip()
        b_lower = b_clean.lower()
        if b_clean in ["Kritischer Fall", "Status", "Genehmigung", "Fehler", "Rückmeldung", "Abgelehnt", "Angenommen"]:
            invalid_buttons.append((b_clean, "Reine Status-/Zustandsbezeichnung ohne Handlungsverb"))
        elif b_lower in ["senden", "submit", "ok", "abschicken"]:
            invalid_buttons.append((b_clean, "Generisches Minimal-Label ohne Zielobjekt"))

    if invalid_buttons:
        # Deduplicate invalid buttons
        dedup_btn = list(dict.fromkeys([f"'{ib[0]}' ({ib[1]})" for ib in invalid_buttons]))
        results["violations"].append({
            "rule": "HWG-BTN-01",
            "severity": "major",
            "message": f"Schaltflächen verletzen das Action-Verb-Muster: {', '.join(dedup_btn)}"
        })
        results["score"] -= penalties["major"]
    elif button_labels:
        results["passed"].append("HWG-BTN-01 (Aktionsorientierte Schaltflächen: Action-Verb-Muster erfüllt)")
    else:
        results["not_applicable"]["HWG-BTN-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Aktionsschaltflächen im Formular vorhanden."

    # 10. HWG-BTN-02: Einheitliche Navigations-Schaltflächen (Mehrseitige Formulare)
    if page_count > 1:
        invalid_nav = []
        for nb in nav_button_labels:
            nb_lower = nb.strip().lower()
            if nb_lower not in ["weiter", "zurück", "zurueck"]:
                invalid_nav.append(nb)
        if invalid_nav:
            results["violations"].append({
                "rule": "HWG-BTN-02",
                "severity": "minor",
                "message": f"Nicht-standardisierte Navigations-Schaltflächen in mehrseitigem Formular gefunden: {invalid_nav}. Erwartet: 'Weiter' und 'Zurück'."
            })
            results["score"] -= penalties["minor"]
        else:
            results["passed"].append("HWG-BTN-02 (Einheitliche Navigations-Schaltflächen 'Weiter'/'Zurück' vorhanden)")
    else:
        results["not_applicable"]["HWG-BTN-02"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Einseitiges Formular ohne Seitenwechsel (keine Pagination erforderlich)."

    # 11. HWG-DSGVO-01
    if has_personal_data and not has_dsgvo_notice:
        results["violations"].append({
            "rule": "HWG-DSGVO-01",
            "severity": "critical",
            "message": "Personenbezogene Daten werden erhoben, aber es fehlt ein Datenschutz-Hinweis / DSGVO-Link."
        })
        results["score"] -= penalties["critical"]
    else:
        results["passed"].append("HWG-DSGVO-01 (Datenschutz-Hinweis vorhanden oder keine Personendaten)")

    # 12. HWG-UPLOAD-01
    if not has_upload_elements:
        results["not_applicable"]["HWG-UPLOAD-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Dateiupload-Elemente im Formular vorhanden."
    elif upload_elements:
        results["violations"].append({
            "rule": "HWG-UPLOAD-01",
            "severity": "major",
            "message": f"{len(upload_elements)} Dateiupload-Element(e) ohne transparente Angabe von Dateiformat und/oder Maximalgröße."
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-UPLOAD-01 (Dateiuploads mit Formaten und Maximalgröße spezifiziert)")

    # 13. HWG-VAL-01
    if structured_fields_unvalidated:
        results["violations"].append({
            "rule": "HWG-VAL-01",
            "severity": "major",
            "message": f"Strukturierte Felder ohne Validierungsregel gefunden: {structured_fields_unvalidated[:3]}"
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-VAL-01 (Strukturierte Felder validiert)")

    # 14. HWG-UX-01
    if not has_compact_fields:
        results["not_applicable"]["HWG-UX-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine typischen Kompaktfelder (wie PLZ oder Hausnummer) vorhanden."
    elif compact_fields_unconstrained:
        results["violations"].append({
            "rule": "HWG-UX-01",
            "severity": "minor",
            "message": f"Kompakte Felder (PLZ/Hausnummer) ohne Breitenbegrenzung über volle Breite gestreckt: {compact_fields_unconstrained[:2]}"
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-UX-01 (Affordanzgerechte Feldbreiten für Kompaktfelder eingehalten)")

    # 15. HWG-UX-02: Empfehlung für Zwischenspeichern-Funktion (0 Punkte Abzug!)
    if (page_count >= 3 or input_field_count >= 25) and not has_save_button:
        results["recommendations"].append({
            "rule": "HWG-UX-02",
            "severity": "recommendation",
            "message": (
                f"Formularumfang ({page_count} Seiten, {input_field_count} Eingabefelder) überschreitet den "
                "Komplexitätsschwellenwert. Empfehlung (0 Pkt. Abzug): Einen 'Zwischenspeichern'-Button ergänzen, "
                "der das Formular speichert und einen Fortsetzungs-Link per E-Mail an die Nutzenden versendet."
            )
        })
        results["score"] -= penalties.get("recommendation", 0)
    elif has_save_button:
        results["passed"].append("HWG-UX-02 (Zwischenspeichern-Funktion für komplexe Formulare vorhanden)")
    else:
        results["not_applicable"]["HWG-UX-02"] = (
            f"Kriterium auf diesen Formularkontext nicht anwendbar: Formularumfang ({page_count} Seiten, "
            f"{input_field_count} Eingabefelder) erfordert keine Zwischenspeicherung."
        )

    # 16. HWG-LANG-01
    if jargon_without_help:
        dedup_jargon = list(dict.fromkeys([f"'{j[0]}' in {j[1]}" for j in jargon_without_help]))
        results["violations"].append({
            "rule": "HWG-LANG-01",
            "severity": "major",
            "message": f"Hochschul- und Verwaltungs-Jargon ohne erläuternden Hilfetext gefunden: {', '.join(dedup_jargon[:3])}"
        })
        results["score"] -= penalties["major"]
    else:
        results["passed"].append("HWG-LANG-01 (Verständlicher Wortschatz: Kein unerklärter Jargon)")

    # 17. HWG-LANG-02 (Prägnante Formulierung / Vermeidung von Schachtelsätzen)
    if long_sentences:
        results["violations"].append({
            "rule": "HWG-LANG-02",
            "severity": "minor",
            "message": f"Überlange Schachtelsätze (> 25 Wörter) gefunden: {long_sentences[:2]}."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-LANG-02 (Prägnante Formulierungen: Alle Sätze unter 25 Wörtern)")

    # 18. HWG-FEEDBACK-01 (Workflow E-Mail Check)
    if not has_workflow_feedback:
        results["violations"].append({
            "rule": "HWG-FEEDBACK-01",
            "severity": "minor",
            "message": "Keine Eingangsbestätigungs-E-Mail mit Prozess-/Bearbeitungsinformationen in den Workflow-E-Mail-Knoten (FC_EMAIL) gefunden."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append(f"HWG-FEEDBACK-01 (Workflow-E-Mail-Transparenz in {len(workflow_emails)} FC_EMAIL-Knoten bestätigt)")

    # 19. HWG-WF-01 (Workflow-Governance: Strukturierte Status-Knoten und Lebenszyklus)
    if not workflow_states:
        results["violations"].append({
            "rule": "HWG-WF-01",
            "severity": "minor",
            "message": "Keine expliziten Status-Knoten (FC_CHANGE_STATE) im Workflow hinterlegt. Kanonischer Lebenszyklus erforderlich."
        })
        results["score"] -= penalties["minor"]
    else:
        canonical_states = {"eingegangen", "in prüfung", "in bearbeitung", "nachforderung ausstehend", "genehmigt", "abgelehnt", "archiviert", "abgeschlossen"}
        non_canonical_states = [s for s in workflow_states if s.lower() not in canonical_states]
        if non_canonical_states:
            results["violations"].append({
                "rule": "HWG-WF-01",
                "severity": "minor",
                "message": f"Nicht-standardisierte Ad-hoc-Statusnamen im Workflow gefunden: {non_canonical_states}. Erwartet: kanonische Zustände ('Eingegangen', 'In Prüfung', 'Genehmigt', 'Abgelehnt')."
            })
            results["score"] -= penalties["minor"]
        else:
            results["passed"].append(f"HWG-WF-01 (Kanonischer Workflow-Lebenszyklus eingehalten: {', '.join(workflow_states)})")

    # 20. HWG-WF-02 (Vorgangsnummern-Referenz in automatisierter Kommunikation)
    has_project_alias = False
    for em in workflow_emails:
        subj = str(em.get("subject", "")).lower()
        body = str(em.get("body", "")).lower()
        if "%$project_alias%" in subj or "%$project_alias%" in body or "vorgangsnummer" in subj or "vorgang" in subj:
            has_project_alias = True
            break

    if not has_project_alias:
        results["violations"].append({
            "rule": "HWG-WF-02",
            "severity": "minor",
            "message": "Fehlende Vorgangsnummer ([%$PROJECT_ALIAS%]) in Workflow-E-Mail-Betreffzeilen."
        })
        results["score"] -= penalties["minor"]
    else:
        results["passed"].append("HWG-WF-02 (Vorgangsnummern-Referenz in Workflow-E-Mail vorhanden)")

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
        print(f"Nicht zutreffend:     {len(res['not_applicable'])}")
        for v in res['violations']:
            print(f"  [X] [{v['severity'].upper():8}] {v['rule']}: {v['message']}")
        for na_k, na_v in res['not_applicable'].items():
            print(f"  [-] [N/A     ] {na_k}: {na_v}")
        if res["recommendations"]:
            print(f"Unverbindliche Empfehlungen ({len(res['recommendations'])}, 0 Punkte Abzug):")
            for r in res["recommendations"]:
                print(f"  [i] [{r['severity'].upper():14}] {r['rule']}: {r['message']}")
