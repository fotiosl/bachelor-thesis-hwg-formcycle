import zipfile, json

def inspect_conditional_properties(path, label):
    print("=" * 60)
    print(f"FORM: {label} ({path})")
    with zipfile.ZipFile(path) as z:
        fcp = [n for n in z.namelist() if n.endswith('.fcp')][0]
        d = json.loads(z.read(fcp).decode('utf-8', 'ignore'))
        items = d.get('items', [])
        
        dynamic_rules = []
        for it in items:
            p = it.get('properties', {})
            cname = it.get('className')
            label_text = p.get('label') or p.get('text') or ''
            # clean html
            label_text = label_text.replace('\n', ' ').strip()
            
            interesting = {}
            for k in ['hiddenifvalue', 'visibleif', 'hiddenif', 'readonlyifcomp', 'requiredif', 'viewstatus', 'viewusergroup', 'statusdependent', 'actionif']:
                val = p.get(k)
                if val:
                    interesting[k] = val
                    
            if interesting:
                dynamic_rules.append({
                    'class': cname,
                    'label': label_text[:50],
                    'rules': interesting
                })
                
        print(f"Total elements: {len(items)}, Elements with dynamic/conditional rules: {len(dynamic_rules)}")
        for r in dynamic_rules[:15]:
            print(f"  [{r['class']}] '{r['label']}'")
            for rk, rv in r['rules'].items():
                print(f"     -> {rk}: {rv}")

forms = [
    ('data/raw_forms/prod/Auslagenerstattung _20260929.xfp', 'Auslagenerstattung'),
    ('data/raw_forms/prod/ZFK Antragsübersicht.xfp', 'ZFK Antragsübersicht')
]

for p, l in forms:
    inspect_conditional_properties(p, l)
