# Konzeption eines einheitlichen Formular-Standards für die HWG Ludwigshafen und prototypische Umsetzung einer KI-gestützten Compliance-Prüfung in Formcycle

**Autor:** Fotios Logaras  
**Studiengang:** Wirtschaftsinformatik, Hochschule für Wirtschaft und Gesellschaft Ludwigshafen  
**Erstprüfer:** Prof. Dr. Simon Kloker  
**Bearbeitungszeitraum:** Oktober 2026 – 07. Dezember 2026  
**Abgabetermin:** 07.12.2026  

---

## 1. Problemstellung & Motivation
An der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG) fehlt derzeit ein verbindlicher Gestaltungs- und Strukturstandard für Online-Formulare, um den angestrebten vollständigen Übergang auf das Formular-Management-System Formcycle standardisiert zu vollziehen. Bestehende Papier- und PDF-Vorlagen müssen dabei inhaltlich konsistent und nutzerzentriert in die digitale Formcycle-Struktur überführt werden. Eine Analyse der bereits implementierten Formulare verdeutlicht jedoch deutliche UX-Inkonsistenzen: Komponenten, Benennungskonventionen und die visuelle Benutzerführung variieren regelmäßig. Für die Anwendenden führt dies zu Reibungsverlusten und Verwirrung bei der Dateneingabe, während für die Erstellenden klare Designvorgaben fehlen, was heterogene Insellösungen und technische Workarounds begünstigt. Dieser Mangel an Standardisierung erschwert die langfristige Wartbarkeit erheblich, da nachträgliche Anpassungen unverhältnismäßig viel Einarbeitungszeit erfordern oder im Extremfall eine vollständige Neugestaltung erzwingen.

## 2. Stand der Literatur und Forschungslücke
Die automatisierte Inspektion von Benutzeroberflächen auf Basis von Usability-Heuristiken und Gestaltungsrichtlinien hat durch die Integration von Large Language Models (LLMs) einen tiefgreifenden technologischen Wandel erfahren. Bisherige empirische Untersuchungen belegen jedoch deutliche Grenzen unstrukturierter Ansätze: Werden vortrainierte Modelle lediglich über naive Standard-Prompts mit der heuristischen Evaluation beauftragt, identifizieren sie im Vergleich zu menschlichen Fachleuten nur rund 21 % der tatsächlichen Usability-Probleme und neigen zu Fehlalarmen (Guerino et al., 2025). Ergänzend zeigen Zhong et al. (2025), dass LLMs zwar im Erkennen von Layout-Auffälligkeiten solide Ergebnisse erzielen, jedoch bei domänenspezifischen Komponenten und komplexen Interaktionsabfolgen ohne formalisierten Kontext scheitern. Um eine verlässliche Regelkonformität zu gewährleisten, weisen Cha et al. (2026) nach, dass registry-basierte Context-Engineering-Strategien zur Operationalisierung von Design-Systemen bei LLM-gestützten Schnittstellenprüfungen eine Compliance von über 95 % erzielen können. Hinsichtlich des operativen Feedback-Workflows zwischen Prüfsystem und UX-Designern demonstrieren Duan et al. (2024), dass automatisiertes Usability-Feedback besonders wirksam ist, wenn es direkt in die gewohnte Arbeitsumgebung eingebettet und als handlungsorientierte Optimierungsempfehlung aufbereitet wird. Gleichzeitig offenbaren aktuelle Studien, dass Sprachmodelle bei der Zuweisung objektiver Schweregrade (Severity Ratings) statistisch instabil urteilen, weshalb semantische Erkennung und quantitative Score-Kalkulation sinnvoll entkoppelt werden sollten (Guerino et al., 2025). In der aktuellen Forschung stehen diese Ansätze meist isoliert nebeneinander und beschränken sich vorwiegend auf abstrakte Labor-Mockups. Seither haben sich die Modelle jedoch maßgeblich weiterentwickelt, was eine Forschungslücke hinsichtlich einer praxistauglichen Synthese eröffnet: Es fehlt an einem Ansatz, der eine empirische Ist-Analyse gewachsener Hochschulformulare mit einer formalen Standarddefinition vereint und diesen Standard als registry-gestützte, hybride LLM-Prüfpipeline unmittelbar in ein Enterprise-System wie Formcycle integriert.

## 3. Forschungsfrage(n), Zielsetzung und Beitrag
Das primäre Ziel der Arbeit besteht darin, einen hochschulweiten Governance-Leitfaden sowie einen funktionsfähigen Software-Prototypen zur automatisierten Compliance-Evaluation in der Formcycle-Infrastruktur zu entwickeln. Hierbei gilt es zu untersuchen, welche Gestaltungsstandards an der HWG bestehen müssen, wie eine maschinenlesbare Komponenten- und Regel-Registry aufgebaut sein muss und wie ein deterministisches Berechnungsmodell einen verlässlichen Compliance-Score ohne stochastische Verzerrungen liefert. Der Nutzen dieser Arbeit liegt darin, ein nachhaltiges Werkzeug zur Einhaltung von Formularstandards, digitaler Barrierefreiheit und Corporate Design an der HWG bereitzustellen. Die zentrale Forschungsfrage lautet daher:

> **Wie lässt sich ein einheitlicher Gestaltungsstandard für HWG-Formulare entwickeln und über KI automatisiert in Formcycle prüfen?**

## 4. Methodisches Vorgehen und Datenbasis
Die Arbeit folgt einem gestaltungsorientierten Ansatz (Design Science Research) und gliedert sich in eine Analyse-, Konzeptions-, Implementierungs- und Evaluationsphase. Zunächst wird eine systematische Bestandsaufnahme durchgeführt: Hierfür werden ausgewählte PDF-, Papier- und Formcycle-Formulare der HWG analysiert, um redundante Felder, Usability-Defizite und Barrierefreiheitsmängel zu identifizieren und in Gegenüberstellungen visuell aufzubereiten. Auf dieser Basis wird ein verbindlicher Leitfaden definiert, der Vorgaben zu Typografie, Abständen, Pflichtfeldlogiken, digitaler Barrierefreiheit (WCAG 2.1) und Benennungskonventionen bündelt. Im nächsten Schritt wird dieses Regelwerk in eine maschinenlesbare JSON-Registry überführt, die als strukturierter Kontextanker für das Context-Engineering dient. Darauf aufbauend wird eine Middleware realisiert, welche die JSON-Struktur des Formulars aus Formcycle extrahiert, zur semantischen Mängelprüfung an ein LLM übergibt und den finalen Compliance-Score über einen deterministischen Algorithmus berechnet. Abschließend wird das System anhand synthetisch erstellter Testformulare in Benchmark-Läufen auf Erkennungsgenauigkeit und Fehlalarme evaluiert. Ein nachgelagerter Praxistest mit formularerstellenden Mitarbeitenden der HWG erfasst die Usability und Nachvollziehbarkeit des Feedbacks über einen standardisierten Fragebogen.

## 5. Zeitplan und vorläufige Gliederung

### Meilensteine und Zeitplan (Frist: 07.12.2026)
* **Woche 1–2 (08.10. – 18.10.2026):** Abschluss der Literaturarbeit; Analyse des HWG-Formularbestands; Konzeption des Master-Regelwerks.
* **Woche 3–4 (19.10. – 01.11.2026):** Formalisierung der JSON-Registry; **Meilenstein 1:** Erstellung der synthetischen, fehlerhaften Testformulare (Ground Truth für Benchmarks).
* **Woche 5–6 (02.11. – 15.11.2026):** Prototypische Umsetzung der Formcycle-Middleware und Prüfpipeline; **Meilenstein 2:** Fertigstellung des Evaluationsfragebogens.
* **Woche 7 (16.11. – 22.11.2026):** Durchführung der Benchmark-Läufe; Praxistests und Fragebogenerhebung mit Mitarbeitenden; Auswertung der Ergebnisse.
* **Woche 8 (23.11. – 29.11.2026):** Intensive Schreibphase; Zusammenführung der Kapitel und Vorbereitung des Rohberichts.
* **Woche 9 (30.11. – 07.12.2026):** **Vorabkorrektur und Feedback-Einarbeitung**; finale Formatierung (APA 7th, Layout); **Abgabe am 07.12.2026**.

### Vorläufige Gliederung
1. **Einleitung und Problemstellung**  
   1.1 Ausgangssituation und Herausforderungen der Formular-Governance an der HWG Ludwigshafen  
   1.2 Zielsetzung, Forschungsfrage und wissenschaftlicher Beitrag  
   1.3 Methodischer Gang der Arbeit (Design Science Research)
2. **Theoretischer Hintergrund und Stand der Technik**  
   2.1 Formular-Usability und digitale Barrierefreiheit (ISO 9241-110, WCAG 2.1)  
   2.2 Heuristische Evaluation und LLM-gestützte Schnittstelleninspektion  
   2.3 Registry-basierte Context-Engineering-Strategien für Design-Systeme  
   2.4 Hybride Bewertungsarchitekturen: Deterministische Regelsysteme versus probabilistisches Scoring
3. **Empirische Ist-Analyse des HWG-Formularbestands**  
   3.1 Erhebungsmethodik und Auswahl des Formular-Korpus  
   3.2 Heuristik-Audit und Identifikation von Problemfeldern (visueller Vorher-Nachher-Vergleich)  
   3.3 Ableitung der Kernanforderungen für einen einheitlichen Standard
4. **Konzeption des Formular-Standards und der Prüf-Registry**  
   4.1 Gestaltungsrichtlinien für Struktur, Barrierefreiheit und Corporate Design  
   4.2 Formalisierung als maschinenlesbare Komponenten- und Regel-Registry (JSON)
5. **Prototypische Implementierung der Compliance-Prüfpipeline**  
   5.1 Systemarchitektur, Datenextraktion aus Formcycle und Schnittstellendesign  
   5.2 Prompt-Design und Context-Engineering für das LLM-Prüfmodul  
   5.3 Deterministische Berechnung des Compliance-Scores und Feedback-Visualisierung
6. **Empirische Evaluation und Diskussion**  
   6.1 Quantitative Benchmark-Tests anhand synthetischer Testformulare  
   6.2 Qualitative Nutzertestung mit Formularautorinnen und -autoren  
   6.3 Diskussion, Systemgrenzen und Validitätsbedrohungen
7. **Fazit und Ausblick**  
   7.1 Zusammenfassung der Ergebnisse  
   7.2 Handlungsempfehlungen für die Hochschulpraxis  
   7.3 Zukünftige Forschungsansätze

## 6. Verwertungsstrategie
Zu den zentralen Adressaten der Bachelorarbeit zählen die Hochschulleitung, das Qualitätsmanagement sowie die Formcycle-Administration der HWG Ludwigshafen. Durch die Standardisierung wird ein konsistenter, barrierefreier Außenauftritt sichergestellt und der IT-Support nachhaltig entlastet, da fehleranfällige Insellösungen entfallen. Der entwickelte Leitfaden soll im Intranet als verbindliches Referenzwerk bereitgestellt werden und insbesondere bei der Einarbeitung neuer Mitarbeitender als verlässliche Orientierung dienen. Das softwarebasierte Prüfwerkzeug liefert direkt umsetzbare Optimierungsempfehlungen bei der Formularerstellung und wird durch eine verständliche Kurzanleitung für das Verwaltungspersonal ergänzt, um eine reibungslose Anwendung in der Praxis zu gewährleisten.

## 7. Literaturverzeichnis (APA 7th Edition)

Cha, S., Jo, S., Shin, J., & Seo, K. (2026). Design System-Compliant User Interface Generation with LLM Agents: A Comparative Study of Context Engineering Strategies. In *Extended Abstracts of the 2026 CHI Conference on Human Factors in Computing Systems* (CHI EA '26). Association for Computing Machinery. https://doi.org/10.1145/3772363.3798616

Duan, P., Warner, J., Li, Y., & Hartmann, B. (2024). Generating Automatic Feedback on UI Mockups with Large Language Models. In *Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems* (CHI '24), Article 872, 1–20. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642782

Guerino, G. C., Rodrigues, L., Capeleti, B., Mello, R. F., Freire, A., & Zaina, L. (2025). Can GPT-4o Evaluate Usability Like Human Experts? A Comparative Study on Issue Identification in Heuristic Evaluation. In *Human-Computer Interaction – INTERACT 2025* (Lecture Notes in Computer Science, Vol. 15286, pp. 381–402). Springer. https://arxiv.org/abs/2506.16345

Zhong, R., McDonald, D. W., & Hsieh, G. (2025). *Synthetic Heuristic Evaluation: A Comparison between AI- and Human-Powered Usability Evaluation*. arXiv preprint. https://doi.org/10.48550/arXiv.2507.02306
