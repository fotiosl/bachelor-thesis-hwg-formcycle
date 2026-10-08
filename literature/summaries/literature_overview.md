# Literaturübersicht & Kernargumente der Quellen

Dieser Leitfaden fasst die Kernquellen der Arbeit zusammen, inklusive der zentralen empirischen Befunde, Zitate und der Relevanz für die Argumentation in der Thesis.

---

## 1. Guerino et al. (2025)
* **Titel:** *Can GPT-4o Evaluate Usability Like Human Experts? A Comparative Study on Issue Identification in Heuristic Evaluation*
* **Autoren:** Guilherme Corredato Guerino, Luiz Rodrigues, Bruna Capeleti, Rafael Ferreira Mello, André Freire, Luciana Zaina
* **Konferenz:** INTERACT 2025 (*Human-Computer Interaction*, LNCS Vol. 15286, Springer)
* **Preprint-Link:** [arXiv:2506.16345](https://arxiv.org/abs/2506.16345) | [Lokales PDF](../pdfs/Guerino_2025_GPT4o_Usability_Heuristic_Evaluation.pdf)
* **Kernaussage:**
  * GPT-4o identifizierte bei naiven Prompts auf Screenshots **lediglich 21,2 %** der Usability-Probleme, die menschliche UX-Experten fanden.
  * Das Modell neigt zu Fehlalarmen und hat Schwierigkeiten, die Kritikalität (Severity) objektiv einzustufen.
* **Bedeutung für die Arbeit:**
  * **Begründung für die Forschungslücke:** Beweist empirisch, dass Standard-Prompts ohne formalisierte Domänenrepräsentation für die Praxis unzureichend sind.
  * **Architektur-Begründung:** Begründet, warum das Severity-Scoring nicht vom LLM ausgewürfelt werden darf, sondern deterministisch kalkuliert werden muss.

---

## 2. Zhong, McDonald & Hsieh (2025)
* **Titel:** *Synthetic Heuristic Evaluation: A Comparison between AI- and Human-Powered Usability Evaluation*
* **Autoren:** Ruican Zhong, David W. McDonald, Gary Hsieh (University of Washington)
* **Preprint-Link:** [arXiv:2507.02306](https://arxiv.org/abs/2507.02306) | [Lokales PDF](../pdfs/Zhong_2025_Synthetic_Heuristic_Evaluation.pdf)
* **Kernaussage:**
  * Multimodale LLMs erreichen in der synthetischen Heuristik-Prüfung eine Erkennungsrate von 73–77 % für allgemeine Usability-Mängel und übertreffen einzelne menschliche Tester bei Layout-Fragen.
  * **Grenzen:** Große Schwächen bei domänenspezifischen UI-Komponenten, unklaren Konventionen und mehrstufigen Navigationsabläufen.
* **Bedeutung für die Arbeit:**
  * Zeigt das Potenzial von LLMs für visuelle/strukturelle Prüfungen auf.
  * Begründet die Notwendigkeit einer maschinenlesbaren **Registry**, um dem Modell den fehlenden domänenspezifischen Kontext zu liefern.

---

## 3. Cha et al. (2026)
* **Titel:** *Design System-Compliant User Interface Generation with LLM Agents: A Comparative Study of Context Engineering Strategies*
* **Autoren:** Seungeon Cha, Sunghyun Jo, Jongho Shin, Kyoungwon Seo
* **Konferenz:** CHI EA '26 (*Extended Abstracts of the 2026 CHI Conference on Human Factors in Computing Systems*, ACM)
* **DOI:** [10.1145/3772363.3798616](https://doi.org/10.1145/3772363.3798616)
* **Kernaussage:**
  * Vergleich dreier Context-Engineering-Strategien zur Einhaltung von Design-Systemen: Instruction-based vs. Context-based vs. Registry-based.
  * Die **Registry-basierte Methode** erzielte eine **Compliance von 95,08 %** und übertraf die anderen Ansätze deutlich bei moderatem Token-Overhead.
* **Bedeutung für die Arbeit:**
  * Liefert das methodische Vorbild für die Formalisierung des HWG-Standards als JSON-Registry (`rules_registry.json`).

---

## 4. Duan et al. (2024)
* **Titel:** *Generating Automatic Feedback on UI Mockups with Large Language Models*
* **Autoren:** Peitong Duan, Jeremy Warner, Yang Li, Bjoern Hartmann
* **Konferenz:** CHI '24 (*Proceedings of the 2024 CHI Conference*, ACM)
* **Preprint-Link:** [arXiv:2403.02534](https://arxiv.org/abs/2403.02534) | [Lokales PDF](../pdfs/Duan_2024_Generating_Automatic_Feedback_UI_Mockups.pdf)
* **Kernaussage:**
  * Entwicklung eines LLM-gestützten Figma-Plugins zur automatisierten heuristischen Evaluation.
  * Feedback muss direkt in die gewohnte Arbeitsumgebung der Erstellenden eingebettet sein und als konkrete, iterative Handlungsempfehlung aufbereitet werden.
* **Bedeutung für die Arbeit:**
  * Dient als Vorlage für das autorenzentrierte Feedback-Design im Formcycle-Kontext (z. B. konkrete Korrekturhinweise statt abstrakter Fehlercodes).

---

## 5. Wang & Xhakaj (2025)
* **Titel:** *AIHeurEval: Generating Heuristic Evaluations on Multiple UI Screens with Multimodal Large Language Models*
* **Autoren:** Yuekai Wang, Franceska Xhakaj
* **Konferenz:** HCII 2025 (*Communications in Computer and Information Science*, Vol. 1528, Springer)
* **DOI:** [10.1007/978-3-031-94168-9_22](https://doi.org/10.1007/978-3-031-94168-9_22)
* **Kernaussage:**
  * Heuristische Multi-Screen-Inspektion mit multimodalen LLMs, um die Einschränkung von Single-Screen-Analysen zu überwinden.
