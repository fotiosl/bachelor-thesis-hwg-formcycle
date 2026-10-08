# Detaillierter Zeitplan & Meilensteine (Frist: 07.12.2026)

**Projektstart:** 08.10.2026  
**Offizielle Abgabefrist:** 07.12.2026 (Montag)  
**Gesamtdauer:** 8,5 Wochen (60 Kalendertage)  

---

## Übersicht der Phasen & Milestones

| Phase | Zeitraum | Inhalt / Fokus | Konkrete Deliverables / Meilensteine | Betreuungs-Termin |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Setup & Kickoff** | 08.10. – 14.10. | Finales Exposé einreichen, Zotero-Setup, Repository | Exposé-Abgabe, `literature/references.bib` | **Milestone 1:** Exposé-Freigabe |
| **Phase 2: Ist-Analyse & Datenbasis** | 15.10. – 28.10. | Analyse von 3–5 HWG-Formularen, Formcycle-Export | Vorher-Nachher Gegenüberstellung, JSON-Exporte | **Milestone 2:** Abstimmung Methodik & Datenbasis |
| **Phase 3: Standard & Testdaten** | 29.10. – 08.11. | Erstellung Master-Regelwerk & Formalisierung in JSON | **Meilenstein 1:** `rules_registry.json` & synthetische Testformulare | Status-Check |
| **Phase 4: Prototyp & Fragebogen** | 09.11. – 22.11. | Python-Middleware für Formcycle-Extraktion & LLM; Scoring-Logik | **Meilenstein 2:** Funktionsfähiger Code & Evaluationsfragebogen | Zwischen-Check |
| **Phase 5: Evaluation & Nutzertest** | 23.11. – 29.11. | Benchmarks (Fehlalarme, Genauigkeit) & Praxistest mit Personal | Auswertung Benchmark-Daten & Fragebogenergebnisse | **Milestone 3:** Ergebnisse & Schlussfolgerungen |
| **Phase 6: Finalisierung & Abgabe** | 30.11. – 07.12. | Fertigstellung Thesis-Text, Vorabkorrektur, Formatierung (APA 7th) | **Endabgabe Thesis + Software-Artefakt** am **07.12.2026** | Offizielle Abgabe |

---

## Detaillierter Ablauf nach Wochen

### Woche 1 (08.10. – 14.10.2026): Kickoff & Setup
- [x] Exposé mit den Anmerkungen des Betreuers finalisieren.
- [x] Git-Repository initialisieren und Verzeichnisstruktur aufsetzen.
- [x] Kernliteratur als PDF herunterladen und BibTeX-Referenzen anlegen.
- [ ] Exposé bei Prof. Dr. Kloker einreichen.
- [ ] Zotero-Bibliothek einrichten und mit `references.bib` synchronisieren.

### Woche 2 & 3 (15.10. – 28.10.2026): Ist-Analyse & Datenbasis (HWG)
- [ ] Auswahl von 3–5 repräsentativen Formularen der HWG (z. B. Urlaubssemester, Adressänderung, Prüfungsanmeldung).
- [ ] Manueller Export der Formulare aus Formcycle als JSON/HTML in `data/raw_forms/`.
- [ ] Systematisches Heuristik-Audit (Usability-Probleme, Barrierefreiheit nach WCAG 2.1).
- [ ] Erstellung visueller Vorher-Nachher-Gegenüberstellungen (Screenshot-Dokumentation).
- [ ] **Milestone-Meeting 2 mit Betreuer:** Vorstellung der Datenbasis und Audit-Ergebnisse.

### Woche 4 (29.10. – 08.11.2026): Standard-Definition & Testdaten-Erstellung
- [ ] Ausarbeitung des Gestaltungs-Standards (Typografie, Pflichtfelder, Barrierefreiheit, Wording).
- [ ] Übersetzung des Standards in die maschinenlesbare `data/rules/rules_registry.json`.
- [ ] **Dozenten-Meilenstein 1:** Erstellung eines Satzes synthetischer, fehlerhafter Testformulare in `data/test_forms/` (Ground Truth mit definierten Fehlern).

### Woche 5 & 6 (09.11. – 22.11.2026): Prototypische Implementierung (Middleware)
- [ ] Aufsetzen der Python-Middleware in `src/middleware/`.
- [ ] Parser für exportierte Formcycle-JSONs / DOM-Strukturen schreiben.
- [ ] Prompt-Design & Context-Engineering (Übergabe der `rules_registry.json` an das LLM).
- [ ] Implementierung der deterministischen Berechnungslogik für den Compliance-Score (z. B. 0–100 % mit Fehlergewichtung).
- [ ] **Dozenten-Meilenstein 2:** Entwurf des standardisierten Evaluationsfragebogens für die Nutzertestung (Usability, Verständlichkeit, Nutzen).

### Woche 7 (23.11. – 29.11.2026): Benchmarking & Nutzertestung
- [ ] Quantitative Benchmark-Läufe mit den synthetischen Testformularen (Genauigkeit, False Positives, Latenz).
- [ ] Praxistest mit 3–5 Formularautorinnen und -autoren der HWG Ludwigshafen.
- [ ] Erhebung des Feedbacks über den vorbereiteten Fragebogen.
- [ ] Statistische / deskriptive Auswertung der Testergebnisse.
- [ ] **Milestone-Meeting 3 mit Betreuer:** Präsentation der Evaluationsergebnisse.

### Woche 8 & 9 (30.11. – 07.12.2026): Intensive Schreibphase, Vorabkorrektur & Abgabe
- [ ] Verfassen und Zusammenführen aller Kapitel (Einleitung bis Fazit, max. 8.000 Wörter).
- [ ] Verfassen des 2-seitigen **Reflexionsberichts zur KI-Nutzung** (Anhang).
- [ ] **Vorabkorrekturlesen** (Sprache, Rechtschreibung, roter Faden).
- [ ] Formaler Check: Zitationen nach APA 7th, Eidesstattliche Erklärung, Abgabeformat (PDF + Code-Artefakt).
- [ ] **07.12.2026: Offizielle fristgerechte Abgabe der Bachelorarbeit.**
