import os
import lxml.html
import re

html_dir = "data/raw_forms/formsHTML"

def inspect_styling(path):
    with open(path, "r", encoding="utf-8", errors="ignore") as f:
        content = f.read()
    doc = lxml.html.fromstring(content)
    
    # Check form container styles
    form_tags = doc.xpath("//form")
    form_classes = form_tags[0].get("class", "") if form_tags else ""
    form_style = form_tags[0].get("style", "") if form_tags else ""
    
    # Find all inline style attributes that mention width
    width_styles = doc.xpath("//*[@style]/@style")
    widths = [s for s in width_styles if "width" in s.lower() or "max-width" in s.lower()]
    
    # Check for linked stylesheets
    css_links = doc.xpath("//link[@rel='stylesheet']/@href")
    
    # Check for embedded <style> tags
    inline_styles = doc.xpath("//style/text()")
    inline_css_len = sum(len(s) for s in inline_styles)
    
    # Check logo / header image
    images = doc.xpath("//img/@src")
    logos = [img for img in images if "logo" in img.lower() or "hwg" in img.lower() or "header" in img.lower()]
    
    # Check buttons (Next, Submit, Back)
    buttons = doc.xpath("//button | //input[@type='submit' or @type='button']")
    btn_texts = [b.text_content().strip() if b.tag == "button" else b.get("value", "") for b in buttons]
    btn_texts = [t for t in btn_texts if t]
    
    return {
        "form_classes": form_classes,
        "form_style": form_style,
        "widths_sample": widths[:3],
        "css_links_count": len(css_links),
        "inline_css_bytes": inline_css_len,
        "images_count": len(images),
        "logos_found": len(logos),
        "buttons": btn_texts[:6]
    }

for f in sorted(os.listdir(html_dir)):
    if f.endswith(".html"):
        res = inspect_styling(os.path.join(html_dir, f))
        print(f"=== {f} ===")
        print(f"  Form Class: {res['form_classes'][:60]}")
        print(f"  Inline CSS in <style>: {res['inline_css_bytes']} Bytes | Ext CSS Links: {res['css_links_count']}")
        print(f"  Images: {res['images_count']} (Logos: {res['logos_found']})")
        print(f"  Buttons: {res['buttons']}")
        print(f"  Width Styles Sample: {res['widths_sample']}")
