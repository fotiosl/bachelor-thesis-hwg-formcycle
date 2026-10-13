import lxml.html

def check(file_name):
    doc = lxml.html.parse(f"data/raw_forms/formsHTML/{file_name}")
    # Check all elements that have page in id or class
    page_els = doc.xpath("//*[contains(@class, 'page') or contains(@id, 'page') or @data-type='page']")
    print(f"=== {file_name} ===")
    print(f"Found {len(page_els)} page candidate elements:")
    for p in page_els[:5]:
        print(f"  Tag: {p.tag} | ID: {p.get('id')} | Class: {p.get('class')} | Style: {p.get('style')}")

check("Personal_Stellenausschreibung_final.html")
check("Auslagenerstattung _20260915.html")
