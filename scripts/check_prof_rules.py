import lxml.html

with open('docs/kloker_supervision_rules.html', 'r', encoding='utf-8', errors='ignore') as f:
    doc = lxml.html.fromstring(f.read())

print("=== 2.3 Formale Vorgaben ===")
for sec in doc.xpath("//section"):
    txt = sec.text_content()
    if "Formale Vorgaben" in txt:
        print(txt.strip()[:1000])

print("\n=== LaTeX / Template Hinweise ===")
for el in doc.xpath("//p | //li"):
    t = el.text_content().strip()
    if any(k in t.lower() for k in ["latex", "template", "vorlage", "layout", "schrift"]):
        print(f"* {t}")
