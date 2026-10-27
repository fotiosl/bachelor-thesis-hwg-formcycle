# 📌 Offene Aufgaben & Notizen für die nächste Session

> **Erstellt am:** 28.10.2026  
> **Kontext:** Bachelorarbeit Fotios Logaras – HWG Ludwigshafen & Formcycle

---

## 1. Tabelle 3.2 & Tabelle 6.1 mit saniertem 100 %-Formular befüllen
- [ ] **Tabelle 3.2 (`thesis/chapters/03_ist_analyse.tex`):**
  - Spalte 4 ist aktuell als *„HWG-Soll-Standard (Referenz)“* mit Platzhalter-Kriterien vorkonfiguriert.
  *Sobald du das sanierte Formular vorliegen hast:* Die exakten Komponenten/Werte des konkreten sanierten Formulars in die 4. Spalte eintragen (z. B. konkrete Elementanzahl, Seiten, Feldvalidierungen etc.).
- [ ] **Tabelle 6.1 (`thesis/chapters/06_evaluation.tex`):**
  - Prüfen, ob das sanierte Formular zusätzlich als Vorher-Nachher-Zeile in die Evaluation aufgenommen werden soll (z. B. Gegenüberstellung: Alt = 50 Punkte / Orange vs. Saniert = 100 Punkte / Grün), oder ob das alte Master-Formular ersetzt wird.

---

## 2. Systematischer Redundanz-Check (Kapitel 3 vs. Kapitel 4 & weitere)
- [ ] **Kapitel 3 (Ist-Analyse) vs. Kapitel 4 (Konzeption des Standards):**
  - Nochmal systematisch Absatz für Absatz gegenlesen.
  - Prüfen, ob in Kapitel 3 wirklich nur der *Problem Space* (empirische Befunde, Fehlerstatistiken, Nutzerprobleme) steht und in Kapitel 4 rein der *Solution Space* (präskriptive Regelspezifikation, Soll-Werte).
  - Auf etwaige weitere inhaltliche Textdopplungen in anderen Kapiteln prüfen (z. B. Einleitung vs. Theorie vs. Fazit).

---

## 3. Optionale Punkte für die Endphase
- [ ] **Corporate Design / Farbwerte:** Falls am Dashboard (`compliance_dashboard.html`) noch CSS-Farben angepasst werden, Farbhex-Codes und Screenshot (Abbildung 5.2 in `thesis/chapters/05_implementierung.tex`) abstimmen.
- [ ] **Abschluss-Build:** Vor Abgabe oder finalem Druck immer mit `python scripts/build_thesis.py` kompilieren und die Seitenzahlen/Seitenränder im generierten `thesis/main.pdf` kontrollieren.

---

### 💡 Tipp für die Arbeit am Laptop:
Um den aktuellen Stand von diesem Rechner auf deinen Laptop zu übernehmen:
1. Auf diesem Rechner committen und pushen:
   ```bash
   git add .
   git commit -m "chore: text revisions, layout fixes in appendix, and TODO notes"
   git push origin main
   ```
2. Auf dem Laptop vor Arbeitsbeginn im Projektordner:
   ```bash
   git pull origin main
   ```
