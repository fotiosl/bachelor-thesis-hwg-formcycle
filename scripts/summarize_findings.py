import json

with open("docs/FORM_INVENTORY_ANALYSIS.json", encoding="utf-8") as f:
    data = json.load(f)

def print_group(name, items):
    print(f"\n{'='*20} {name} ({len(items)} Formulare) {'='*20}")
    for d in items:
        f = d["file"]
        title = d.get("title", "")
        elems = d["total_elements"]
        pages = d["pages"]
        up = "Upload" if d["has_upload"] else "Kein Upload"
        widths = ",".join(d["widths"]) if d["widths"] else "keine"
        theme = d["theme"]
        css = f"{d['custom_css_len']}B CSS" if d["custom_css_len"] else "Kein CSS"
        print(f"* {f}")
        print(f"    Titel: {title} | Elemente: {elems} | Seiten: {pages} | {up} | {css}")
        print(f"    Theme: {theme} | Breiten: {widths}")
        print(f"    Komponenten: {d['classes']}")

print_group("PROD FORMULARE", [x for x in data if "prod" in x["category"]])
print_group("ADMIN / MASTER FORMULARE", [x for x in data if "admin" in x["category"]])
print_group("TEST / ENTWICKLUNGS FORMULARE", [x for x in data if "unfertig" in x["category"]])
