# 📌 Offene Aufgaben & Notizen für die nächste Session

> **Erstellt am:** 28.10.2026  
> **Kontext:** Bachelorarbeit Fotios Logaras – HWG Ludwigshafen & Formcycle

---

## 1. Tabelle 3.2 & Tabelle 6.1 mit saniertem 100 %-Formular befüllen
- [x] **Tabelle 3.2 (`thesis/chapters/03_ist_analyse.tex`):**
  - Spalte 4 wurde auf die exakten gemessenen Kennzahlen des im Formcycle-v8-Designer sanierten Referenzformulars *„Antrag-Sprints (HWG-Standard)“* umgestellt (1 Seite, 30 Elemente, H1 + 60\,px HWG-Logo mit Alt-Text, XIMA deaktiviert, 2 semantische Fieldsets mit Legenden, 12 Pflichtfelder inkl. globaler Legende, lückenlose Feldvalidierung, Art.-13-DSGVO-Integration, Action-Verb-Buttons und 8/8 E-Mails mit Vorgangs-ID).
- [x] **Tabelle 6.1 (`thesis/chapters/06_evaluation.tex`):**
  - Vollständige Hybrid-Klassifikation (Stufe 1 AST + Stufe 2 Semantik/Hybrid) für alle Zeilen synchronisiert (jede Zeile summiert konsistent exakt zu 22 Regeln):
    - *Synthetisch Konform (`synthetic_compliant_form.xfp`):* 20 Best. / 0 Verst. / 2 N/A (Score 100, Grün)
    - *Synthetisch Fehlerhaft (`synthetic_noncompliant_form.xfp`):* 1 Best. / 19 Verst. / 2 N/A (Score 0, Rot)
    - *Auslagenerstattung (Prod):* 9 Best. / 12 Verst. / 1 Empf. / 0 N/A (Score 17, Rot)
    - *Antrag-Sprints (ZFK, alt):* 7 Best. / 11 Verst. / 4 N/A (Score 6, Rot)
    - *Antrag-Sprints (saniert):* 18 Best. / 0 Verst. / 4 N/A (Score 100, Grün)
    - *Master-Formular (Admin):* 12 Best. / 6 Verst. / 1 Empf. / 3 N/A (Score 50, Orange)
  - **Live-Verifikation:** Neben der GWDG Academic Cloud wurde die semantische Stufe lokal über Ollama mit `qwen3.8:27b` verifiziert (mediane Antwortzeit ca. 10 Sekunden).
- [x] **Pipeline, Presets & Dashboard:**
  - Formular `AFörderung Antrag-Sprints für Drittmittelanträge (HWG-Standard).xfp` in `data/raw_forms/standard/` und `data/test_forms/` abgelegt, in `scripts/test_rule_engine.py`, `scripts/generate_web_dashboard.py` und `web/server.py` als Preset integriert und `web/compliance_dashboard.html` neu generiert.

---

## 2. Systematischer Redundanz-Check & Reflexionsbericht
- [x] **Kapitel 3 (Ist-Analyse) vs. Kapitel 4 (Konzeption des Standards):**
  - Systematisch gegengelesen: Saubere Trennung von Problem Space (Kapitel 3) und Solution Space (Kapitel 4) verifiziert.
- [x] **Reflexionsbericht (Anhang B):**
  - Auf exakt 2 Seiten gestrafft (gemäß Kloker-Betreuungsrichtlinien & Westermann 2026), sodass kein Überlauf mehr auf eine 3. Seite entsteht.
- [x] **Typografie & Build-Optimierung:**
  - `\pdfminorversion=7` integriert (PDF-1.7-Warnung beseitigt).
  - Sämtliche `Overfull \hbox`-Randüberstände im Anhang und Fazit behoben.
  - Tabellenbreite der Eidesstattlichen Erklärung exakt an Satzspiegel angepasst.

---

## 3. Optionale Punkte für die Endphase
- [ ] **Zweitprüfer:** Sobald der Zweitprüfer offiziell bestellt ist, Zeile in `thesis/main.tex` aktivieren.
- [ ] **Corporate Design / Farbwerte:** Falls am Dashboard (`compliance_dashboard.html`) noch CSS-Farben angepasst werden, Farbhex-Codes und Screenshot (Abbildung 5.2 in `thesis/chapters/05_implementierung.tex`) abstimmen.
- [ ] **Abschluss-Build:** Vor Abgabe oder finalem Druck immer mit `python scripts/build_thesis.py` kompilieren und die Seitenzahlen/Seitenränder im generierten `thesis/main.pdf` kontrollieren.

---

### 💡 Tipp für die Arbeit am Laptop:
Um den aktuellen Stand von diesem Rechner auf deinen Laptop zu übernehmen:
1. Auf diesem Rechner committen und pushen:
   ```bash
   git add .
   git commit -m "chore: streamline reflexionsbericht to exactly 2 pages and fix typography"
   git push origin main
   ```
2. Auf dem Laptop vor Arbeitsbeginn im Projektordner:
   ```bash
   git pull origin main
   ```
