import os
import zipfile
import json

base_dir = "data/raw_forms"
results = []

def count_elements(el_list):
    count = 0
    types = []
    has_upload = False
    has_table = False
    for el in el_list:
        count += 1
        if isinstance(el, dict):
            t = el.get("type", "unknown")
            types.append(t)
            if "upload" in t.lower() or "file" in t.lower():
                has_upload = True
            if "table" in t.lower() or "grid" in t.lower():
                has_table = True
            for child_key in ["children", "items", "elements"]:
                if child_key in el and isinstance(el[child_key], list):
                    sub_c, sub_t, sub_up, sub_tbl = count_elements(el[child_key])
                    count += sub_c
                    types.extend(sub_t)
                    has_upload = has_upload or sub_up
                    has_table = has_table or sub_tbl
    return count, types, has_upload, has_table

for root, dirs, files in os.walk(base_dir):
    for f in sorted(files):
        if f.endswith(".xfp"):
            fp = os.path.join(root, f)
            rel_dir = os.path.relpath(root, base_dir)
            try:
                with zipfile.ZipFile(fp, "r") as z:
                    fcp_files = [n for n in z.namelist() if n.endswith(".fcp")]
                    if fcp_files:
                        d = json.loads(z.read(fcp_files[0]).decode("utf-8", "ignore"))
                        title = d.get("title", f)
                        desc = d.get("description", "")
                        theme = d.get("formTheme") or d.get("theme", "")
                        errorstyle = d.get("errorstyle", "")
                        pagemax = d.get("pagemax", 1)
                        custom_css_len = len(d.get("css", "") or "")
                        items = d.get("items", [])
                        
                        total_items, all_types, has_upload, has_table = count_elements(items)
                        
                        results.append({
                            "file": f,
                            "category": rel_dir,
                            "title": title,
                            "desc": desc,
                            "pages": pagemax,
                            "item_count": total_items,
                            "theme": theme,
                            "errorstyle": errorstyle,
                            "has_upload": has_upload,
                            "has_table": has_table,
                            "custom_css_bytes": custom_css_len,
                            "unique_types": sorted(list(set(all_types)))
                        })
                    else:
                        results.append({
                            "file": f,
                            "category": rel_dir,
                            "title": "KEINE FCP DATEI",
                            "item_count": 0
                        })
            except Exception as e:
                results.append({
                    "file": f,
                    "category": rel_dir,
                    "title": f"FEHLER: {e}",
                    "item_count": 0
                })

with open("form_inventory.json", "w", encoding="utf-8") as out:
    json.dump(results, out, ensure_ascii=False, indent=2)

print(f"Erfolgreich {len(results)} Formulare analysiert.")
