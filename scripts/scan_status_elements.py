import zipfile, json, os

files = {
    'Drittmittel-Sprints': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp',
    'Forschungsprojekte/Promotionsvorhaben': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung Forschungsprojekte_Promotionsvorhaben.xfp',
    'F&T-Veranstaltungen': 'data/raw_forms/test/unfertige und vielleicht fertige formulare/Antrag auf Förderung für Durchführung von F&T-Veranstaltungen.xfp',
    'Auslagenerstattung': 'data/raw_forms/prod/Auslagenerstattung _20260929.xfp',
    'ZFK Antragsübersicht': 'data/raw_forms/prod/ZFK Antragsübersicht.xfp',
    'ZFK-Fördermittel (prod)': 'data/raw_forms/prod/ZFK-Fördermittel (20260227).xfp'
}

for label, p in files.items():
    print('======================================================================')
    print(f'*** {label} ***')
    print('Path:', p)
    if not os.path.exists(p):
        print('NOT FOUND')
        continue
    with zipfile.ZipFile(p) as z:
        fcp_name = [n for n in z.namelist() if n.endswith('.fcp')][0]
        d = json.loads(z.read(fcp_name).decode('utf-8', 'ignore'))
        
        status_dep_elements = []
        usergroup_dep_elements = []
        has_conditions = []
        all_elements = []
        
        def scan_items(items):
            for it in items:
                if not isinstance(it, dict):
                    continue
                name = it.get('name') or it.get('id') or 'unnamed'
                cname = it.get('className')
                props = it.get('properties', {})
                viewstatus = props.get('viewstatus', [])
                viewusergroup = props.get('viewusergroup', [])
                statusdep = props.get('statusdependent', '')
                events = it.get('events') or {}
                conditions = it.get('conditions') or {}
                
                info = {
                    'name': name,
                    'className': cname,
                    'label': props.get('label') or props.get('text') or it.get('label') or '',
                    'viewstatus': viewstatus,
                    'viewusergroup': viewusergroup,
                    'statusdependent': statusdep,
                    'events': list(events.keys()) if isinstance(events, dict) else events,
                    'conditions': conditions
                }
                all_elements.append(info)
                if viewstatus:
                    status_dep_elements.append(info)
                if viewusergroup:
                    usergroup_dep_elements.append(info)
                if statusdep:
                    status_dep_elements.append(info)
                if conditions:
                    has_conditions.append(info)
                    
                for child_key in ['children', 'items', 'elements']:
                    if child_key in it and isinstance(it[child_key], list):
                        scan_items(it[child_key])
                        
        scan_items(d.get('items', []))
        print(f'Total elements: {len(all_elements)}')
        print(f'Elements with viewstatus: {len(status_dep_elements)}')
        for el in status_dep_elements[:10]:
            print(f"  - [{el['className']}] {el['name']} ('{el['label'][:30]}') -> viewstatus: {el['viewstatus']}, statusdep: {el['statusdependent']}")
        print(f'Elements with viewusergroup: {len(usergroup_dep_elements)}')
        for el in usergroup_dep_elements[:10]:
            print(f"  - [{el['className']}] {el['name']} ('{el['label'][:30]}') -> viewusergroup: {el['viewusergroup']}")
        print(f'Elements with conditions: {len(has_conditions)}')
        for el in has_conditions[:10]:
            print(f"  - [{el['className']}] {el['name']} ('{el['label'][:30]}') -> conditions: {el['conditions']}")
