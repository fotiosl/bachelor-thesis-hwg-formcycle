import zipfile, json

def inspect_form_details(path, name):
    print("==================================================")
    print(f"DETAILS FOR: {name} ({path})")
    with zipfile.ZipFile(path) as z:
        fcp_name = [n for n in z.namelist() if n.endswith('.fcp')][0]
        d = json.loads(z.read(fcp_name).decode('utf-8', 'ignore'))
        
        pages = []
        for it in d.get('items', []):
            if it.get('className') == 'XPage':
                page_title = it.get('properties', {}).get('title') or it.get('name')
                # Count elements inside page
                elem_types = {}
                def c_elem(item_list):
                    for sub in item_list:
                        t = sub.get('className', 'unknown')
                        elem_types[t] = elem_types.get(t, 0) + 1
                        for k in ['children', 'items', 'elements']:
                            if k in sub and isinstance(sub[k], list):
                                c_elem(sub[k])
                c_elem(it.get('children', []) or it.get('items', []))
                pages.append((page_title, elem_types))
        
        print(f"Total Pages in items: {len(pages)}")
        for idx, (p_title, p_types) in enumerate(pages):
            print(f"  Page {idx+1}: '{p_title}' -> {p_types}")

inspect_form_details('data/raw_forms/prod/ZFK Antragsübersicht.xfp', 'ZFK Antragsübersicht')
inspect_form_details('data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp', 'Drittmittel-Sprints')
inspect_form_details('data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung Forschungsprojekte_Promotionsvorhaben.xfp', 'Forschungsprojekte/Promotionsvorhaben')
inspect_form_details('data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung für Durchführung von F&T-Veranstaltungen.xfp', 'F&T-Veranstaltungen')
inspect_form_details('data/raw_forms/prod/Auslagenerstattung _20260929.xfp', 'Auslagenerstattung')
