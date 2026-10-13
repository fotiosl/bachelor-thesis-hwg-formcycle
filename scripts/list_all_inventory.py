import json

with open('docs/FORM_INVENTORY_ANALYSIS.json', encoding='utf-8') as f:
    data = json.load(f)

print(f"Total forms: {len(data)}")
for i, d in enumerate(data):
    cat = d.get("category", "")
    fname = d.get("file", "")
    title = d.get("title", "")
    elem = d.get("total_elements", 0)
    pages = d.get("pages", 1)
    widths = d.get("widths", [])
    upload = d.get("has_upload", False)
    css = d.get("custom_css_bytes", 0)
    print(f"{i+1:2d}. [{cat[:25]:<25}] {fname[:40]:<40} | {elem:3d} el | {pages} p | {str(widths):<10} | Up:{str(upload):<5} | CSS:{css}")
