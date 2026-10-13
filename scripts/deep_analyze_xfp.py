import os
import zipfile
import json

base_dir = "data/raw_forms"
reports = []

for root, dirs, files in os.walk(base_dir):
    for f in sorted(files):
        if f.endswith(".xfp"):
            fp = os.path.join(root, f)
            rel_dir = os.path.relpath(root, base_dir)
            try:
                with zipfile.ZipFile(fp) as z:
                    fcp_name = [n for n in z.namelist() if n.endswith(".fcp")][0]
                    d = json.loads(z.read(fcp_name).decode("utf-8", "ignore"))
                    
                    title = d.get("title", f)
                    desc = d.get("description", "")
                    theme = d.get("formTheme") or d.get("theme", "")
                    if isinstance(theme, dict):
                        theme_name = theme.get("name") or theme.get("id") or "Custom/Dict"
                    else:
                        theme_name = str(theme or "None")
                    
                    errorstyle = d.get("errorstyle", "")
                    custom_css = d.get("css", "") or ""
                    items = d.get("items", [])
                    
                    # Component counts
                    classes = {}
                    field_widths = set()
                    req_hints = set()
                    labels = []
                    has_upload = False
                    pages = 0
                    
                    for it in items:
                        c = it.get("className", "Unknown")
                        classes[c] = classes.get(c, 0) + 1
                        if c == "XPage":
                            pages += 1
                        if c == "XUpload":
                            has_upload = True
                        props = it.get("properties", {})
                        if "maxwidth" in props and props["maxwidth"] is not None:
                            field_widths.add(str(props["maxwidth"]))
                        if "showrequiredhint" in props and props["showrequiredhint"] is not None:
                            req_hints.add(str(props["showrequiredhint"]))
                        # Check labels
                        for lkey in ["label", "text", "heading"]:
                            if lkey in props and props[lkey]:
                                labels.append(str(props[lkey])[:40])
                                
                    reports.append({
                        "file": f,
                        "rel_path": os.path.join(rel_dir, f),
                        "category": rel_dir,
                        "title": title,
                        "desc": desc,
                        "total_elements": len(items),
                        "pages": max(pages, 1),
                        "classes": classes,
                        "has_upload": has_upload,
                        "theme": theme_name,
                        "errorstyle": errorstyle,
                        "custom_css_len": len(custom_css),
                        "widths": sorted(list(field_widths)),
                        "required_hints": sorted(list(req_hints)),
                        "sample_labels": labels[:5]
                    })
            except Exception as e:
                reports.append({
                    "file": f,
                    "rel_path": os.path.join(rel_dir, f),
                    "category": rel_dir,
                    "title": f"ERROR: {e}",
                    "total_elements": 0,
                    "pages": 0,
                    "classes": {},
                    "has_upload": False,
                    "theme": "Error",
                    "errorstyle": "",
                    "custom_css_len": 0,
                    "widths": [],
                    "required_hints": [],
                    "sample_labels": []
                })

with open("docs/FORM_INVENTORY_ANALYSIS.json", "w", encoding="utf-8") as out:
    json.dump(reports, out, ensure_ascii=False, indent=2)

print(f"Exported detailed inventory of {len(reports)} forms.")
