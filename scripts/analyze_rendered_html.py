import os
import lxml.html

html_dir = "data/raw_forms/formsHTML"

def analyze_html(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    
    doc = lxml.html.fromstring(content)
    
    title = doc.findtext(".//title") or "Kein Titel"
    
    # Inputs, selects, textareas
    inputs = doc.xpath("//input | //select | //textarea")
    labels = doc.xpath("//label")
    
    # IDs and matching
    input_ids = set(doc.xpath("//input/@id | //select/@id | //textarea/@id"))
    labels_with_for = doc.xpath("//label[@for]")
    matching_for = [l for l in labels_with_for if l.get("for") in input_ids]
    
    # Aria and required
    aria_req = doc.xpath("//*[@aria-required='true' or @required]")
    
    # Fieldsets and legends
    fieldsets = doc.xpath("//fieldset")
    legends = doc.xpath("//fieldset/legend")
    
    # Form pages in Formcycle DOM
    # Usually div with class containing page, or role
    pages = doc.xpath("//*[contains(@class, 'xf-page') or contains(@class, 'page') or contains(@class, 'xm-page')]")
    
    # Error hints
    error_views = doc.xpath("//*[contains(@class, 'error') or contains(@class, 'errormsg')]")
    
    # Asterisks
    asterisks = doc.xpath("//*[contains(text(), '*')]")
    
    return {
        "title": title.strip() if title else "",
        "inputs_total": len(inputs),
        "labels_total": len(labels),
        "labels_with_for": len(labels_with_for),
        "matching_for": len(matching_for),
        "aria_req": len(aria_req),
        "fieldsets": len(fieldsets),
        "legends": len(legends),
        "pages": len(pages),
        "errors": len(error_views),
        "asterisks": len(asterisks),
    }

print(f"{'Datei':<42} | {'Inp':<5} | {'Lbl':<5} | {'For':<5} | {'FSet':<5} | {'Aria':<5} | {'*':<4} | {'Titel'}")
print("-" * 115)

for f in sorted(os.listdir(html_dir)):
    if f.endswith(".html"):
        fp = os.path.join(html_dir, f)
        res = analyze_html(fp)
        print(f"{f[:40]:<42} | {res['inputs_total']:<5} | {res['labels_total']:<5} | {res['matching_for']:<5} | {res['fieldsets']:<5} | {res['aria_req']:<5} | {res['asterisks']:<4} | {res['title'][:35]}")
