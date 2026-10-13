import zipfile, json

forms = {
    'AFörderung Antrag-Sprints für Drittmittelanträge': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp',
    'Antrag auf Förderung Forschungsprojekte_Promotionsvorhaben': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung Forschungsprojekte_Promotionsvorhaben.xfp',
    'Antrag auf Förderung für Durchführung von F&T-Veranstaltungen': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung für Durchführung von F&T-Veranstaltungen.xfp',
    'Auslagenerstattung _20260929': 'data/raw_forms/prod/Auslagenerstattung _20260929.xfp',
    'ZFK Antragsübersicht': 'data/raw_forms/prod/ZFK Antragsübersicht.xfp'
}

for name, path in forms.items():
    print("=" * 70)
    print("NAME:", name)
    with zipfile.ZipFile(path) as z:
        fcp = [n for n in z.namelist() if n.endswith('.fcp')][0]
        d = json.loads(z.read(fcp).decode('utf-8', 'ignore'))
        items = d.get('items', [])
        
        counts = {}
        has_fieldsets = 0
        has_containers = 0
        has_hiddenif = 0
        has_requiredif = 0
        has_viewstatus = 0
        has_viewusergroup = 0
        field_labels = []
        
        for it in items:
            cn = it.get('className')
            counts[cn] = counts.get(cn, 0) + 1
            p = it.get('properties', {})
            if cn == 'XFieldSet': has_fieldsets += 1
            if cn in ['XContainer', 'XContainerInvisible']: has_containers += 1
            if p.get('hiddenif') or p.get('hiddenifvalue'): has_hiddenif += 1
            if p.get('requiredif'): has_requiredif += 1
            if p.get('viewstatus'): has_viewstatus += 1
            if p.get('viewusergroup'): has_viewusergroup += 1
            
            lbl = p.get('label') or p.get('text')
            if lbl and cn in ['XTextField', 'XTextArea', 'XSelect', 'XCheckbox']:
                # strip html tags
                import re
                clean = re.sub('<[^<]+?>', '', lbl).strip()
                if clean:
                    field_labels.append((cn, clean))
                    
        print(f"Breite: {d.get('pagemax')} | Seiten: {d.get('pagemin', 1)}-{d.get('pagemax', 1)} (XPage: {counts.get('XPage', 1)})")
        print(f"Komponenten: {counts}")
        print(f"Semantik: FieldSets={has_fieldsets}, Div-Container={has_containers}")
        print(f"Dynamik: hiddenif={has_hiddenif}, requiredif={has_requiredif}, viewstatus={has_viewstatus}, viewusergroup={has_viewusergroup}")
        print(f"Formular-Felder ({len(field_labels)} Stk):")
        for cn, lb in field_labels[:8]:
            print(f"   [{cn}] {lb}")
        if len(field_labels) > 8:
            print(f"   ... und {len(field_labels)-8} weitere Felder.")
