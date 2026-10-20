import zipfile
import json
import glob
import os
from collections import defaultdict, Counter

xfp_files = glob.glob('data/raw_forms/**/*.xfp', recursive=True)

form_workflows = []

for p in xfp_files:
    fname = os.path.basename(p)
    folder = os.path.dirname(p).replace('data/raw_forms', '').replace('\\', '/').strip('/')
    try:
        with zipfile.ZipFile(p) as z:
            fce_list = [n for n in z.namelist() if n.endswith('.fcexport') and '/projects/' in n]
            inboxes = []
            states = []
            emails = []
            submit_buttons = []
            print_targets = []
            
            for fce in fce_list:
                d = json.loads(z.read(fce).decode('utf-8', 'ignore'))
                
                # Check project inboxes
                for ib in d.get('project', {}).get('inboxes', []):
                    if isinstance(ib, dict) and 'name' in ib:
                        inboxes.append(ib['name'])
                
                # Check status list
                for st in d.get('project', {}).get('stateList', []):
                    if isinstance(st, dict) and 'name' in st:
                        states.append(st['name'])
                        
                def walk(obj):
                    if isinstance(obj, dict):
                        t = obj.get('type')
                        name = obj.get('name', '')
                        if t == 'FC_MOVE_FORM_RECORD_TO_INBOX':
                            cp = obj.get('customParameters')
                            inboxes.append(name)
                        elif t in ['FC_CHANGE_STATE', 'CUSTOM', 'RECEIVED']:
                            if name: states.append(name)
                        elif t == 'FC_EMAIL':
                            if name: emails.append(name)
                        elif t in ['FC_QUALIFIED_FORM_SUBMIT_BUTTON', 'FC_FORM_SUBMIT_BUTTON']:
                            if name: submit_buttons.append(name)
                        elif t == 'RemotePrintService':
                            if name: print_targets.append(name)
                            
                        for v in obj.values():
                            walk(v)
                    elif isinstance(obj, list):
                        for x in obj:
                            walk(x)
                walk(d)
                
            form_workflows.append({
                'file': fname,
                'folder': folder,
                'inboxes': sorted(list(set(inboxes))),
                'states': sorted(list(set(states))),
                'emails': sorted(list(set(emails))),
                'submit_buttons': sorted(list(set(submit_buttons))),
                'print_targets': sorted(list(set(print_targets)))
            })
    except Exception as e:
        print(f"Error {fname}: {e}")

print(f"Analysierte Formulare: {len(form_workflows)}")

# Print overview of multi-stage workflows
print("\n" + "="*80)
print("MULTI-STAGE WORKFLOWS WITH ROLES / INBOXES / STATES:")
print("="*80)

multi_actor_forms = []
single_actor_forms = []

for fw in form_workflows:
    # Check if there are department keywords in inboxes or states or print targets
    dept_keywords = ['haushalt', 'personal', 'zfk', 'kanzler', 'präsident', 'praesident', 'dekan', 'it', 'justiziariat', 'vorgesetzter', 'fachbereich']
    combined_text = " ".join(fw['inboxes'] + fw['states'] + fw['print_targets'] + fw['emails']).lower()
    matched_depts = [dk for dk in dept_keywords if dk in combined_text]
    
    if len(matched_depts) >= 2 or len(fw['inboxes']) >= 2:
        multi_actor_forms.append((fw, matched_depts))
    else:
        single_actor_forms.append((fw, matched_depts))

print(f"Mehrstufige Formulare (>= 2 Abteilungen / Inboxes): {len(multi_actor_forms)} / {len(form_workflows)}")
print(f"Einstufige / isolierte Formulare: {len(single_actor_forms)} / {len(form_workflows)}")

for fw, depts in multi_actor_forms:
    print(f"\n[{fw['folder']}] {fw['file']}")
    print(f"  Erkannte Stellen/Abteilungen: {', '.join(depts)}")
    if fw['inboxes']:
        print(f"  Postfächer: {fw['inboxes'][:5]}")
    if fw['states']:
        print(f"  Zustände ({len(fw['states'])}): {fw['states'][:6]}")
    if fw['print_targets']:
        print(f"  Prüf-PDFs: {fw['print_targets'][:4]}")
