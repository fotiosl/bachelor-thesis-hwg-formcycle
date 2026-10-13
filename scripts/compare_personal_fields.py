import json
import zipfile

def get_fields(xfp_path):
    with zipfile.ZipFile(xfp_path) as z:
        fcp = [n for n in z.namelist() if n.endswith('.fcp')][0]
        d = json.loads(z.read(fcp).decode('utf-8', 'ignore'))
        items = d.get('items', [])
        fields = []
        for it in items:
            props = it.get('properties', {})
            c = it.get('className')
            lbl = props.get('label') or props.get('text') or props.get('heading') or ''
            name = props.get('name', '')
            req = props.get('showrequiredhint', '')
            if c in ['XTextField', 'XSelect', 'XTextArea', 'XFieldSet', 'XCheckbox']:
                fields.append((c, name, lbl[:35], req))
        return fields

print("=== MASTER-FORMULAR (PERSÖNLICHE ANGABEN) ===")
for f in get_fields("data/raw_forms/test/adminformulare/Master-Formular.xfp"):
    print(f"  {f[0]:<12} | {f[1]:<20} | {f[2]:<35} | req={f[3]}")

print("\n=== AUSLAGENERSTATTUNG ===")
for f in get_fields("data/raw_forms/prod/Auslagenerstattung _20260929.xfp")[:15]:
    print(f"  {f[0]:<12} | {f[1]:<20} | {f[2]:<35} | req={f[3]}")

print("\n=== FB1 PRAKTIKUM ===")
for f in get_fields("data/raw_forms/prod/FB1-GiP_Praktikum_final_20251115.xfp")[:15]:
    print(f"  {f[0]:<12} | {f[1]:<20} | {f[2]:<35} | req={f[3]}")
