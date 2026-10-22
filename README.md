# Bachelorarbeit: Konzeption eines einheitlichen Formular-Standards & KI-gestützte Compliance-Prüfung in Formcycle

[![Status](https://img.shields.io/badge/Status-Review%20%26%20Finalization-success.svg)]()
[![Frist](https://img.shields.io/badge/Abgabe-07.12.2026-critical.svg)]()
[![Institution](https://img.shields.io/badge/Hochschule-HWG%20Ludwigshafen-red.svg)]()

> **Thema:** Konzeption eines einheitlichen Formular-Standards für die HWG Ludwigshafen und prototypische Umsetzung einer KI-gestützten Compliance-Prüfung in Formcycle  
> **Autor:** Fotios Logaras  
> **Erstprüfer:** Prof. Dr. Simon Kloker  
> **Bearbeitungszeit:** 08.10.2026 – **07.12.2026** (8,5 Wochen / 60 Tage)  

---

## 🎯 Zielsetzung & Forschungsfrage

Online-Formulare an der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG) weisen historisch gewachsene UX-Inkonsistenzen bezüglich Komponenten, Benennungen und visueller Benutzerführung auf. 

Diese Arbeit verfolgt ein doppeltes Ziel nach dem **Design Science Research (DSR)** Paradigma:
1. **Konzeption eines verbindlichen Formular- und Governance-Standards** (WCAG 2.1, ISO 9241-110, Corporate Design), formalisiert in einer maschinenlesbaren JSON-Registry (`data/rules/rules_registry.json`).
2. **Entwicklung und Evaluation einer hybriden Prüfpipeline**: Eine Middleware extrahiert Strukturdaten aus Formcycle, nutzt ein LLM zur semantischen Defekterkennung und berechnet über einen deterministischen Algorithmus einen reproduzierbaren Compliance-Score.

> **Zentrale Forschungsfrage:**  
> *Wie lässt sich ein einheitlicher Gestaltungsstandard für HWG-Formulare entwickeln und über KI automatisiert in Formcycle prüfen?*

---

## 📁 Projektstruktur

```text
├── docs/                     # Exposé, Richtlinien, Zeitplan, Modulhandbuch, Ist-Analyse
├── literature/               # BibTeX (references.bib nach APA 7th), Kernliteratur-PDFs & Zusammenfassungen
├── data/
│   ├── raw_forms/            # Exportierte Originalformulare der HWG (.xfp) & gerenderte DOM-Snapshots
│   ├── rules/                # Formalisierte Governance-Regeln (rules_registry.json v1.5.0)
│   ├── test_forms/           # Synthetische Testformulare (Ground Truth Benchmarks)
│   ├── evaluation/           # Empirische Benchmark-Ergebnisse (multi_model_benchmark_results.json)
│   └── prompts/              # Strukturierte Prompts für Open-Source- & Frontier-Modelle
├── scripts/                  # Prüf-Engine (test_rule_engine.py), Build- & Analysewerkzeuge
│   └── archive/              # Archivierte Textgenerierungs- und Optimierungsskripte
├── web/                      # Intranet-Web-Dashboard (compliance_dashboard.html & server.py)
│   └── vendor/               # Lokale Offline-Bibliotheken (JSZip für Air-Gapped Intranet)
├── deploy/                   # Container-Bereitstellung (Dockerfile, docker-compose.yml, nginx.conf)
├── thesis/                   # Vollständige LaTeX-Ausarbeitung (Kapitel 1–7, Anhang, Grafiken)
└── README.md
```

---

## 📚 Wissenschaftliche Kernliteratur

1. **Guerino et al. (2025):** *Can GPT-4o Evaluate Usability Like Human Experts?* (INTERACT 2025 / arXiv:2506.16345) – Belegt, dass unstrukturierte Standard-Prompts nur 21,2 % der Usability-Probleme erfassen und begründet die Notwendigkeit formalisierter Kontextanker.
2. **Cha et al. (2026):** *Design System-Compliant User Interface Generation with LLM Agents* (CHI EA '26) – Demonstriert, dass Registry-basierte Context-Engineering-Strategien über 95 % Design-System-Compliance erzielen.
3. **Duan et al. (2024):** *Generating Automatic Feedback on UI Mockups with Large Language Models* (CHI '24) – Bestätigt den hohen Nutzen von autorenzentriertem, iterativem Feedback direkt in der Entwicklungsumgebung.
4. **Zhong et al. (2025):** *Synthetic Heuristic Evaluation* (arXiv:2507.02306) – Vergleicht synthetische und menschliche Heuristikprüfungen; zeigt Stärken bei Layouts und Schwächen bei isolierten Komponenten.

---

## ⏱️ Zeitplan & Meilensteine bis zum 07.12.2026

* **Phase 1 (Woche 1):** Setup, Literaturorganisation, Exposé-Abgabe.
* **Phase 2 (Woche 2–3):** Ist-Analyse des Formularbestands & Formcycle-Exporte $\rightarrow$ **Milestone 2 mit Betreuer**.
* **Phase 3 (Woche 4):** Standard-Definition & **Meilenstein 1 (Synthetische Testformulare)**.
* **Phase 4 (Woche 5–6):** Middleware-Entwicklung & **Meilenstein 2 (Evaluationsfragebogen)**.
* **Phase 5 (Woche 7):** Benchmarks & Praxistest mit Personal $\rightarrow$ **Milestone 3 mit Betreuer**.
* **Phase 6 (Woche 8–9):** Schreibphase, Vorabkorrektur & **Abgabe am 07.12.2026**.
