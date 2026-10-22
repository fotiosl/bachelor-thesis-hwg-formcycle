# Check professor rules without third-party dependencies
import os
import re

html_path = 'docs/kloker_supervision_rules.html'
if not os.path.exists(html_path):
    print("Datei nicht gefunden:", html_path)
    exit(0)

with open(html_path, 'r', encoding='utf-8', errors='ignore') as f:
    html = f.read()

# Strip tags for clean text search
text = re.sub(r'<[^>]+>', ' ', html)
text = re.sub(r'\s+', ' ', text)

print("=== 2.3 Formale Vorgaben (Auszug) ===")
m = re.search(r'Formale Vorgaben.*?Umfang.*?\.', text)
if m:
    print(m.group(0))

print("\n=== Zitate und Literaturvorgaben (Auszug) ===")
m2 = re.search(r'Zitierweise:.*?Layout:.*?DIN A4', text)
if m2:
    print(m2.group(0))
