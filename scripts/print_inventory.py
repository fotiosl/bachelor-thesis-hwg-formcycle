import json

with open("form_inventory.json", encoding="utf-8") as f:
    data = json.load(f)

print(f"{'Ordner':<10} | {'Dateiname':<45} | {'Titel':<35} | {'Elem':<5} | {'Pg':<3} | {'Up':<4} | {'CSS':<7} | {'Theme':<15}")
print("-" * 135)

for item in sorted(data, key=lambda x: (x["category"], -x["item_count"])):
    cat = "prod" if "prod" in item["category"] else ("admin" if "admin" in item["category"] else "test")
    fname = item["file"][:44]
    title = (item.get("title") or "")[:34]
    items = item.get("item_count", 0)
    pages = item.get("pages", 1)
    up = "Ja" if item.get("has_upload") else "-"
    css = f"{item.get('custom_css_bytes', 0)}B"
    theme_val = item.get("theme")
    if isinstance(theme_val, dict):
        theme_str = theme_val.get("name") or theme_val.get("id") or str(theme_val)
    else:
        theme_str = str(theme_val or "kein")
    theme = theme_str[:14]
    print(f"{cat:<10} | {fname:<45} | {title:<35} | {items:<5} | {pages:<3} | {up:<4} | {css:<7} | {theme:<15}")
