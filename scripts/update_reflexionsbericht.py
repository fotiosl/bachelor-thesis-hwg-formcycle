import os

report_content = r"""\chapter{Reflexionsbericht zur Nutzung von KI-Tools}
\label{chap:reflexionsbericht}

Gemäß den Betreuungsrichtlinien von Prof. Dr. Simon Kloker sowie der Handreichung zur guten wissenschaftlichen Praxis im Umgang mit generativer künstlicher Intelligenz an Hochschulen (\textcite{westermann2026ki}) dokumentiert und reflektiert dieser zweiseitige Bericht den Einsatz von KI-Werkzeugen im Verlauf der vorliegenden Bachelorarbeit. Der Einsatz generativer KI erfolgte theoriegeleitet, reflektiert und unter ständiger Wahrung der wissenschaftlichen Eigenständigkeit und Urheberschaft des Autors.

\section*{1. Auswahl der KI-Tools und methodisches Vorgehen}
Die Auswahl der eingesetzten Werkzeuge wurde anhand klar definierter Anforderungskriterien getroffen. Da die Arbeit eine komplexe Verknüpfung aus JSON-Datenstrukturen, hierarchischen AST-Bäumen der Formcycle-Plattform und linguistischer Microcopy-Analyse umfasst, waren ein großes Kontextfenster, hohe logische Code-Verständnisfähigkeit sowie eine geringe Halluzinationsneigung bei strikten Schemata ausschlaggebend. Primär wurde das multimodale Frontier-Modell \textit{Google Gemini} in einer agentischen Entwicklungsumgebung eingesetzt. Ergänzend wurden zur Evaluation der Modell-Agnostik im Sinne der Datensouveränität quelloffene Open-Source-Modelle (\textit{Meta Llama-3.1-8B}, \textit{Qwen-3.8-27B}, \textit{Qwen-3-30B-A3B}, \textit{GLM-5.3-Flash} und \textit{DeepSeek-V4-Flash}) über die universitäre Infrastruktur der \textit{Academic Cloud} (GWDG) evaluiert. Werkzeuge ohne nachvollziehbare Inferenzspuren oder mit proprietärem Vendor-Lock-in wurden für die Analysepipeline verworfen.

\section*{2. Häufigkeit, Nutzen und ungeeignete Werkzeuge}
KI-Werkzeuge kamen im Rahmen iterativer Arbeitsschritte in unterschiedlicher Intensität zum Einsatz:
\begin{itemize}
    \item \textbf{Sehr hoher Nutzen:} Bei der Entwicklung der Python-Middleware erwies sich die KI als herausragender Pair-Programming-Partner. Die Konstruktion komplexer Algorithmen zur AST-Traversierung, die Handhabung verschachtelter ZIP-Archive und die Konvertierung von Formular-Metadaten in standardisierte JSON-Schemas konnten durch Prompt-Iterationen erheblich beschleunigt werden.
    \item \textbf{Mittlerer Nutzen:} Beim Formulieren des wissenschaftlichen Textes half die KI als linguistischer Resonanzboden zur Schärfung von Argumentationssträngen und zur Elimination von Füllwörtern.
    \item \textbf{Ungeeignete Werkzeuge:} Reine generative Textassistenten ohne Code-Verbindung erwiesen sich für die fachliche Regelfindung als ungeeignet. Frühe Versuche, Standard-Prompts direkt unbereinigte Formular-Dumps analysieren zu lassen, scheiterten an Aufmerksamkeitsverlust (\textit{Lost in the Middle}) und oberflächlichen Halluzinationen. Erst durch strukturiertes Context-Engineering und die Reduktion irrelevanter Layout-Tokens um >90\,\% konnte verlässliche Inferenz erzielt werden.
\end{itemize}

\section*{3. Anwendungsbereiche und aufgetretene Herausforderungen}
Besonders unterstützend wirkte der KI-Einsatz bei der formalen Definition der 21 Governance-Regeln der Registry v1.5.0 sowie bei der Konzeption des interaktiven HTML5/CSS-Web-Dashboards. Eine signifikante Herausforderung trat bei der Synthese von Literaturquellen auf: Unüberwachte Sprachmodelle neigen dazu, plausible, aber gänzlich fiktive bibliografische Angaben (\textit{Phantom-Zitate}) zu erfinden. Sämtliche in der Arbeit verwendeten Quellen mussten daher manuell gegen wissenschaftliche Datenbanken (ACM Digital Library, IEEE Xplore, SpringerLink) verifiziert werden. Eine weitere Herausforderung bestand in der korrekten Interpretation negativer Constraints: Kleinere Modelle (wie Llama-3.1-8B) neigten bei Satzlängenprüfungen zu Zählfehlern, wohingegen größere Modelle ab 27B Parametern komplexe Heuristiken präzise meisterten.

\section*{4. Validierung der KI-generierten Inhalte}
Alle durch KI-Interaktion entstandenen Artefakte – sei es Programmcode, Tabellenstrukturen oder Formulierungsvorschläge – wurden nach dem Vier-Augen-Prinzip einer rigorosen menschlichen Qualitätskontrolle unterzogen:
\begin{itemize}
    \item \textbf{Code-Validierung:} Jedes Python-Skript wurde durch automatisierte Unit-Tests und Regressionstests an realen Formcycle-Exports (\texttt{.xfp}) auf Ausfallsicherheit, Typkorrektheit und Laufzeit (<20\,ms) geprüft.
    \item \textbf{Empirische Ground-Truth-Prüfung:} Die KI-gestützt erstellten Referenzformulare wurden manuell auf DOM-Ebene durchleuchtet, um sicherzustellen, dass die 15 injizierten Fehler exakt den Spezifikationen der Registry entsprechen.
    \item \textbf{Fachliche Normprüfung:} Gesetzliche und ergonomische Vorgaben (BITV 2.0, DIN EN ISO 9241-110, Art. 13 DSGVO) wurden originär an den Primärtexten gespiegelt.
\end{itemize}

\section*{5. Erforderliche Kompetenzen für die effektive Nutzung}
Der gewinnbringende Einsatz generativer KI setzt ein hohes Maß an fachlicher Domänen- und Methodenkompetenz voraus (\textcite{recker2013scientific}). Ohne fundiertes Verständnis der Web-Accessibility (WCAG-Erfolgskriterien), der Software-Ergonomie nach Nielsen und der internen JSON-Objektmodelle von Formcycle wäre es unmöglich gewesen, zielführende System-Prompts zu konstruieren oder fehlerhafte Ausgaben zu entlarven. Darüber hinaus war fortgeschrittenes \textit{Context-Engineering} erforderlich, um Typ-Injektionen, Few-Shot-Exemplare und strikte JSON-Schemas so zu orchestrieren, dass Open-Source-Modelle deterministisch reagieren.

\section*{6. Auswirkungen auf den Schreib- und Forschungsprozess}
Die Nutzung von KI transformierte den traditionellen Schreibprozess von einer sequenziellen Texterstellung hin zu einer dialogischen, iterativen Wissenskonstruktion. Durch das rasche Prototyping von Code und Testfällen verlagerte sich der zeitliche Schwerpunkt der Bachelorarbeit weg von zeitraubenden mechanischen Routineaufgaben (wie dem manuellen Durchsuchen von 49 Formulardateien) hin zu konzeptioneller Tiefe, methodischer Reflexion und empirischer Validierung. Als hinderlich erwies sich zu Beginn die Gefahr einer kognitiven Verzerrung (\textit{Automation Bias}), der durch bewusstes Hinterfragen jedes KI-Vorschlags aktiv entgegengewirkt werden musste.

\section*{7. Schlussfolgerungen für zukünftige wissenschaftliche Arbeiten}
Generative KI stellt ein mächtiges epistemisches Werkzeug dar, das die Effizienz und Qualität gestaltungsorientierter Forschungsarbeiten maßgeblich steigern kann. Für zukünftige wissenschaftliche Projekte lässt sich schlussfolgern, dass KI niemals als unkritischer Texterzeuger, sondern stets als fokussiertes Analyse- und Reflexionsinstrument eingesetzt werden sollte. Die strikte methodische Entkopplung von deterministischer Vorverarbeitung und semantischer Modell-Inferenz, wie sie in dieser Arbeit entwickelt wurde, bietet eine belastbare Blaupause für den dauerhaften, datensouveränen Einsatz an Hochschulen.
"""

with open("thesis/appendix/reflexionsbericht.tex", "w", encoding="utf-8") as f:
    f.write(report_content.strip() + "\n")

print("Reflexionsbericht erfolgreich auf ca. 2 Seiten ausgebaut!")
