import lxml.html
import glob

files = glob.glob("data/raw_forms/formsHTML/*.html")
for fp in sorted(files):
    doc = lxml.html.parse(fp)
    btns = doc.xpath("//button | //input[@type='button' or @type='submit']")
    items = []
    for b in btns:
        txt = b.text_content().strip() if b.tag == 'button' else b.get('value', '')
        bid = b.get('id', '')
        bclass = b.get('class', '')
        items.append(f"{txt} (id={bid})")
    fname = fp.split("\\")[-1]
    print(f"{fname}: {items}")
