import zipfile
import json
import glob
import os
from collections import Counter

xfp_files = glob.glob('data/raw_forms/**/*.xfp', recursive=True)
print(f"Total xfp files found: {len(xfp_files)}")

workflows = []

for p in xfp_files:
    fname = os.path.basename(p)
    try:
        with zipfile.ZipFile(p) as z:
            fce_list = [n for n in z.namelist() if n.endswith('.fcexport') and '/projects/' in n]
            all_nodes = []
            for fce in fce_list:
                d = json.loads(z.read(fce).decode('utf-8', 'ignore'))
                def walk(obj):
                    if isinstance(obj, dict):
                        if 'type' in obj and 'name' in obj:
                            all_nodes.append((obj.get('type'), obj.get('name')))
                        for v in obj.values():
                            walk(v)
                    elif isinstance(obj, list):
                        for x in obj:
                            walk(x)
                walk(d)
            if all_nodes:
                workflows.append({
                    'file': fname,
                    'path': p,
                    'nodes': all_nodes
                })
    except Exception as e:
        print(f"Error reading {fname}: {e}")

print(f"\nForms with active workflow nodes: {len(workflows)} / {len(xfp_files)}\n")

all_types = Counter()
for w in workflows:
    print("=" * 60)
    print(f"Form: {w['file']} ({len(w['nodes'])} nodes)")
    for t, n in w['nodes']:
        all_types[t] += 1
        print(f"   [{t:20}] {n}")

print("\n" + "=" * 60)
print("Node type distribution across all workflows:")
for t, c in all_types.most_common():
    print(f"   {t:20}: {c}")
