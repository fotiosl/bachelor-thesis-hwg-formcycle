# Detaillierter Zeitplan & Meilensteine (Frist: 07.12.2026)

**Projektstart:** 08.10.2026  
**Offizielle Abgabefrist:** 07.12.2026 (Montag)  
**Gesamtdauer:** 8,5 Wochen (60 Kalendertage)  

---

## Übersicht der Phasen & Milestones

| Phase | Zeitraum | Inhalt / Fokus | Konkrete Deliverables / Meilensteine | Status |
| :--- | :--- | :--- | :--- | :--- |
| **Phase 1: Setup & Kickoff** | 08.10. – 14.10. | Finales Exposé einreichen, Zotero-Setup, Repository | Exposé-Abgabe, `literature/references.bib` | **Erledigt** |
| **Phase 2: Ist-Analyse & Datenbasis** | 15.10. – 28.10. | Analyse von 34 HWG-Formularen, Formcycle-Export | Vorher-Nachher Gegenüberstellung, JSON-Exporte | **Erledigt** |
| **Phase 3: Standard & Testdaten** | 29.10. – 08.11. | Erstellung Master-Regelwerk & Formalisierung in JSON | **Meilenstein 1:** `rules_registry.json` & synthetische Testformulare | **Erledigt** |
| **Phase 4: Prototyp & Pipeline** | 09.11. – 22.11. | Python-Prüfengine für Formcycle-Extraktion & LLM; Scoring-Logik, Dashboard | **Meilenstein 2:** Funktionsfähiger Code, Pipeline & Web-Dashboard | **Erledigt** |
| **Phase 5: Evaluation & Benchmarking**| 23.11. – 29.11. | Benchmarks (synthetisch & real) & Multi-Model-Vergleich (Academic Cloud) | Auswertung Benchmark-Daten, Latenz- & Treffermetriken | **Erledigt** |
| **Phase 6: Finalisierung & Abgabe** | 30.11. – 07.12. | Fertigstellung Thesis-Text, Vorabkorrektur, Formatierung (APA 7th) | **Endabgabe Thesis + Software-Artefakt** am **07.12.2026** | **In Prüfung** |

---

## Detaillierter Ablauf nach Wochen

### Woche 1 (08.10. – 14.10.2026): Kickoff & Setup
- [x] Exposé mit den Anmerkungen des Betreuers finalisieren.
- [x] Git-Repository initialisieren und Verzeichnisstruktur aufsetzen.
- [x] Kernliteratur als PDF herunterladen und BibTeX-Referenzen anlegen.
- [x] Exposé bei Prof. Dr. Kloker einreichen.
- [x] Zotero-Bibliothek einrichten und mit `references.bib` synchronisieren.

### Woche 2 & 3 (15.10. – 28.10.2026): Ist-Analyse & Datenbasis (HWG)
- [x] Erhebung des gesamten Formularbestands der HWG (34 Formulare, 34 Workflow-Modelle in 53 .fcexport-Dateien).
- [x] Export der Formulare aus Formcycle als JSON/HTML in `data/raw_forms/`.
- [x] Systematisches Heuristik-Audit (Usability-Probleme, Barrierefreiheit nach WCAG 2.1).
- [x] Erstellung visueller Vorher-Nachher-Gegenüberstellungen (Screenshot-Dokumentation in `thesis/figures/`).
- [x] **Milestone-Meeting 2 mit Betreuer:** Vorstellung der Datenbasis und Audit-Ergebnisse.

### Woche 4 (29.10. – 08.11.2026): Standard-Definition & Testdaten-Erstellung
- [x] Ausarbeitung des Gestaltungs-Standards (Typografie, Pflichtfelder, Barrierefreiheit, Wording).
- [x] Übersetzung des Standards in die maschinenlesbare `data/rules/rules_registry.json` (v1.5.0, 22 Regeln).
- [x] **Dozenten-Meilenstein 1:** Erstellung der synthetischen Testformulare in `data/test_forms/` (Ground Truth mit 19 definierten Defekten).

### Woche 5 & 6 (09.11. – 22.11.2026): Prototypische Implementierung (Pipeline & Dashboard)
- [x] Aufsetzen der modularen Python-Middleware in `scripts/test_rule_engine.py` und `web/server.py`.
- [x] AST-Traversierung und Merkmalsextraktion für Formcycle-Archive (`.xfp`, `.fcp`, `.fcexport`).
- [x] Prompt-Design & Context-Engineering für Open-Source- und Frontier-Modelle (`data/prompts/`).
- [x] Implementierung der deterministischen Berechnungslogik für den Compliance-Score (0–100 Punkte).
- [x] **Meilenstein 2:** Entwicklung des interaktiven Intranet-Web-Dashboards (`web/compliance_dashboard.html`).

### Woche 7 (23.11. – 29.11.2026): Benchmarking & Modell-Evaluation
- [x] Quantitative Benchmark-Läufe mit den synthetischen Testformularen (Genauigkeit, False Positives, Latenz).
- [x] Empirischer Multi-Model-Vergleich mit 5 Modellen über die universitäre Academic Cloud (GWDG).
- [x] Auswertung realer Anträge (Auslagenerstattung, Drittmittel-Sprints, Master-Formular).
- [x] **Milestone-Meeting 3 mit Betreuer:** Präsentation der Evaluationsergebnisse.

### Woche 8 & 9 (30.11. – 07.12.2026): Intensive Schreibphase, Vorabkorrektur & Abgabe
- [x] Verfassen und Zusammenführen aller Kapitel (Kapitel 1–7, ca. 4.400 Wörter, Limit 8.000 Wörter eingehalten).
- [x] Verfassen des 2-seitigen **Reflexionsberichts zur KI-Nutzung** (Anhang B).
- [x] Dokumentation der Prompt-Spezifikation (Anhang A) und Eidesstattliche Erklärung (Anhang C).
- [ ] **Vorabkorrekturlesen** (Sprache, Rechtschreibung, roter Faden).
- [ ] Formaler Check: Zitationen nach APA 7th, Eidesstattliche Erklärung, Abgabeformat (PDF + Code-Artefakt).
- [ ] **07.12.2026: Offizielle fristgerechte Abgabe der Bachelorarbeit.**
