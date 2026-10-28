# MASTER-REVIEW-AUFTRAG FÜR GEMINI (ADVANCED / ARGON / 2.0 FLASH / 1.5 PRO)

## Deine Experten-Rolle:
Du bist ein hochkarätiges wissenschaftliches Begutachtungs- und Gutachter-Gremium für Bachelorarbeiten der Wirtschaftsinformatik an der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG Ludwigshafen). Du agierst in einer Vierfach-Rolle:
1. **Erstprüfer (Prof. Dr. Simon Kloker):** Bewertet Stringenz der Problemstellung, DSR-Methodik (Peffers et al. 2007, Hevner et al. 2004, Gregor & Hevner 2013), Einhaltung von APA 7th, Einhaltung der Betreuungsrichtlinien (siehe Datei 02), Beantwortung der Forschungsfragen (MRQ, FQ1–FQ4) und den Reflexionsbericht nach Westermann (2026).
2. **Software-Architekt & Code-Auditor:** Prüft die 1:1-Kongruenz zwischen den im Text beschriebenen Algorithmen (Kapitel 5) und dem tatsächlichen Python-Quellcode (`04_COMPLIANCE_ENGINE_AST.py`, `05_CONTEXT_ENGINEERING_PROMPT.py`, `07_DASHBOARD_SERVER.py`).
3. **Usability- & Governance-Auditor (DIN EN ISO 9241-110, BITV 2.0 / WCAG 2.1, Art. 13 DSGVO):** Prüft die 22 Governance-Regeln der Registry (`03_REGELKATALOG_REGISTRY_v1.5.0.json`), die Nielsen-Schweregrade und verifiziert die mathematische Richtigkeit der Evaluationsergebnisse (Tabelle 3.2 und Tabelle 6.1).
4. **Wissenschaftlicher Lektor:** Prüft Roter Faden, Typografie, Stil, Vermeidung von Redundanzen und formale Exzellenz.

---

## Dir bereitgestellte Dokumente im Anhang:
* `01_THESIS_MAIN.pdf`: Die fertig kompilierte Bachelorarbeit (47 Seiten, 7 Kapitel, Verzeichnisse, Literaturverzeichnis, Anhang A–B, Eidesstattliche Erklärung).
* `02_BETREUER_VORGABEN_UND_EXPOSE.md`: Die offiziellen Bewertungs- und Richtlinienvorgaben von Prof. Dr. Kloker sowie das genehmigte Exposé.
* `03_REGELKATALOG_REGISTRY_v1.5.0.json`: Die formalisierte maschinenlesbare Governance-Registry mit allen 22 Regeln.
* `04_COMPLIANCE_ENGINE_AST.py`: Der vollständige Python-Quellcode der hybriden Prüf-Engine (`test_rule_engine.py`).
* `05_CONTEXT_ENGINEERING_PROMPT.py`: Der JSON-Payload-Komprimierer und Prompt-Generator (`generate_chat_ai_prompt.py`).
* `06_MULTI_MODEL_BENCHMARKS.json`: Die empirischen Multi-Model-Benchmarkdaten der fünf Open-Weight-Modelle in der GWDG Academic Cloud.
* `07_DASHBOARD_SERVER.py`: Der Python-Server für das Intranet-Compliance-Dashboard (`server.py`).
* `08_TESTFORMULAR_KONFORM_100.json`: Das synthetische Vollkonform-Formular (Ground-Truth Zielscore 100).
* `09_TESTFORMULAR_DEFEKTE_0.json`: Das synthetische Negativ-Formular (Ground-Truth Zielscore 0 mit 19 gezielten Defekten).
*(Optional: `ALL_IN_ONE_AUDIT_DOSSIER.md`, falls als Gesamtdossier beigefügt).*

---

## Deine Aufgaben & Prüfkatalog:

Bitte nutze dein maximales Denk- und Analysepotenzial (Deep Thinking / Extended Thinking / Argon) und führe einen schonungslosen, tiefgehenden Audit durch:

### 1. Mathematische Konsistenz & Evaluationsabgleich (Kapitel 6 vs. Code & Daten)
* Prüfe die Werte in Tabelle 6.1 (S. 34 der Thesis): Stimmen die Scores (100, 0, 17, 6, 100, 50), die Summen aus Bestanden / Verstöße / Empfehlungen / N/A in jeder Zeile exakt mit der Registry (22 Regeln) und der Code-Logik überein?
* Prüfe die Benchmark-Tabelle 6.2 (S. 35): Stimmen die Angaben zu Recall, False Positives und den fünf Modellen (GLM 5.3 Flash, Llama 3.1 8B, Qwen 3.8 27B, Qwen 3 30B, DeepSeek V4 Flash) mit `06_MULTI_MODEL_BENCHMARKS.json` überein?
* Prüfe Tabelle 3.2 (S. 18): Stimmen die Kennzahlen des sanierten Standardformulars (1 Seite, 32 Elemente, 12 Pflichtfelder, 8 E-Mails) mit der Realität überein?

### 2. Code-vs.-Text-Kongruenz (Kapitel 5 vs. Python-Skripte)
* Entspricht die Beschreibung der vier Phasen (Ingestion Zero-Disk via `io.BytesIO`, Stufe 1 AST, Stufe 2 LLM via `/v1/chat/completions`, Fail-Safe `unverified_semantic`, Phase 3 Scoring, Phase 4 Klickpfad) exakt der Code-Implementierung in `04_COMPLIANCE_ENGINE_AST.py`?
* Werden die sechs Presets (`synth_comp`, `synth_noncomp`, `auslagen`, `sprints`, `sprints_standard`, `master`) in Text und Code konsistent geführt?

### 3. DSR-Methodik & Erstprüfer-Kriterien (Prof. Dr. Kloker)
* Wurden die sechs Phasen nach Peffers et al. (2007) und der Level-2-Beitrag nach Gregor & Hevner (2013) wissenschaftlich einwandfrei operationalisiert?
* Ist die Hauptforschungsfrage (MRQ) und sind die vier Teilfragen (FQ1–FQ4) im Fazit (Kapitel 7) vollständig und überzeugend beantwortet?
* Entspricht die Zitation durchgängig APA 7th Edition?
* Entspricht der Reflexionsbericht (Anhang B) exakt den Betreuer-Richtlinien von Prof. Dr. Kloker (Umfang ca. 2 Seiten, strukturierte Reflexion entlang der Leitfragen, Einbettung von Westermann 2026)?

### 4. Roter Faden, Argumentationslogik & Sprache
* Gibt es noch Brüche, logische Sprünge oder Widersprüche zwischen den Kapiteln?
* Gibt es verbliebene Redundanzen zwischen Problem Space (Kapitel 3) und Solution Space (Kapitel 4)?
* Wo siehst du potenzielle Angriffspunkte oder kritische Fragen, die ein Zweitprüfer in der Verteidigung stellen könnte?

---

## Gewünschtes Ausgabeformat:
Gliedere deinen Bericht in:
1. **Management Summary & Gesamturteil (Note/Tendenz)**
2. **Kritische Befunde & Widersprüche (Blocker / Must-Fix)** – falls vorhanden, mit genauer Seiten-/Zeilenangabe.
3. **Subtile Unstimmigkeiten & Konsistenz-Beobachtungen (Should-Fix)**
4. **Feinschliff- und Optimierungsvorschläge für Text, Code und Argumentation**
5. **Erwartbare Fragen und Verteidigungs-Strategie für das Kolloquium**
