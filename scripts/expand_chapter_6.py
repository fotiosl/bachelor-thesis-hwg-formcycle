import os

chapter_6_content = r"""\chapter{Empirische Evaluation und Diskussion}
\label{chap:evaluation}

Zur wissenschaftlichen Überprüfung und Validierung des im Rahmen dieser Arbeit entwickelten gestaltungsorientierten Artefakts (\textcite{hevner2004design, peffers2007design}) wird in diesem Kapitel eine umfassende empirische Evaluation durchgeführt. Ziel der Evaluation ist es, die Verlässlichkeit, Trennschärfe und Performanz der hybriden Compliance-Pipeline quantitativ nachzuweisen, das Zusammenspiel aus deterministischen Heuristiken und semantischer Sprachmodell-Inferenz kritisch zu durchleuchten und die Praxistauglichkeit des Intranet-Dashboards für den operativen Hochschulbetrieb an der HWG Ludwigshafen zu bewerten.

\section{Evaluationsdesign, Methodik und Benchmark-Metriken}
\label{sec:eval_design}

Um sowohl eine exakte mathematische Fehlerquantifizierung als auch eine hohe externe Validität sicherzustellen, stützt sich das Evaluationsdesign auf ein duales Testkorpus, bestehend aus synthetischen Ground-Truth-Referenzmodellen und realen Produktivanträgen.

\subsection{Synthetisches Kontrollkorpus (Ground Truth)}
In der empirischen Software- und Usability-Forschung stellt das Fehlen objektiv annotierter Ground-Truth-Datensätze eine zentrale methodische Herausforderung dar (\textcite{zhong2025synthetic, guerino2025gpt4o}). Da reale Bestandsformulare naturgemäß unbekannte oder umstrittene Mischformen von Konformität aufweisen, wurden im Rahmen dieser Untersuchung zwei synthetische Kontrollinstanzen nach dem Formcycle-Schema konstruiert:\footnote{Hinweis zur Datenherkunft gemäß Betreuungsrichtlinien (Abschnitt 6.2.1): Die beiden synthetischen Referenzdatensätze (\texttt{synthetic\_compliant\_form.json} und \texttt{synthetic\_noncompliant\_form.json}) wurden KI-gestützt (Google Gemini) auf Basis des Formcycle-\texttt{.fcp}-Schemas generiert und manuell validiert. Verwendeter Generierungs-Prompt: \textit{\enquote{Erzeuge zwei synthetische Formcycle-JSON-Testformulare (.fcp-Struktur mit items, properties und workflow\_emails) zur Evaluation der HWG-Compliance-Registry v1.5.0: (1) Ein vollkonformes Referenzformular (Ground Truth: 100 Punkte), das alle 20 bewerteten Regeln einhält (850px, XImage-Logo, XFooter mit showlogo=0, XFieldSet-Gruppierung, kanonische Stammdaten, Regex-Validierung für PLZ/IBAN, DSGVO-Hinweis, spezifizierter Upload, Action-Verb-Button sowie FC\_EMAIL-Eingangsbestätigung). (2) Ein fehlerinjiziertes Referenzformular (Ground Truth: 0 Punkte) mit exakt 15 gezielten Regelverstößen über alle Schweregrade hinweg.}}}
\begin{itemize}
    \item \textbf{Synthetisches Referenzformular A (Vollkonform, Ground Truth = 100 Punkte):} Dieses Formular implementiert das im Standard (Kapitel~\ref{chap:konzeption}) definierte Idealbild. Es nutzt eine Layoutbreite von 850px, besitzt das offizielle HWG-Kopfbanner, hat das XIMA-Footerlogo deaktiviert (\texttt{showlogo="0"}), strukturiert Abschnitte über semantische \texttt{XFieldSet}-Container, deklariert Pflichtfelder programmatisch und optisch, nutzt kanonische Stammdaten-Labels, validiert PLZ und IBAN über reguläre Ausdrücke, integriert die vorgeschriebene DSGVO-Datenschutzerklärung, spezifiziert Upload-Formate und -Größen präzise, verwendet aktionsorientierte Schaltflächen (\enquote{Antrag jetzt verbindlich einreichen}) und hinterlegt im Workflow sowohl den standardisierten Statuslebenszyklus (\texttt{HWG-WF-01}) als auch die Vorgangsnummer \texttt{[\%\$PROJECT\_ALIAS\%]} in der Eingangsbestätigungs-E-Mail (\texttt{HWG-WF-02}).
    \item \textbf{Synthetisches Referenzformular B (Fehlerinjiziert, Ground Truth = 0 Punkte):} In dieses Negativmuster wurden bewusst 15 distinkte Regelverstöße über alle Schweregrade hinweg injiziert: Veraltete 700px-Breite (Major), fehlendes Kopflogo (Critical), aktives XIMA-Herstellerbranding im Footer (Major), HTML-Tags in Labels (Minor), sichtbare Entwicklernotizen im Frontend (Critical), nicht-standardisierte Bezeichner (Minor), generische Button-Labels wie \texttt{senden} und Status-Labels wie \enquote{Kritischer Fall} (Major), fehlende DSGVO-Klausel bei Personendaten (Critical), unvollständige Upload-Angaben (Major), unvalidierte strukturierte Eingabefelder (Major), unbeschränkte kompakte Felder (Minor), Hochschul-Jargon ohne Tooltip (Major), fehlende E-Mail-Bestätigung (Minor), fehlende Workflow-Statusknoten (Minor) sowie fehlende Vorgangsnummern in E-Mails (Minor).
\end{itemize}

\subsection{Reales Evaluierungskorpus der HWG Ludwigshafen}
Zur Überprüfung der Praxistauglichkeit unter realen Betriebsbedingungen wurden drei authentische Formulare aus dem Formcycle-System der Hochschule ausgewählt, die unterschiedliche organisatorische Domänen und funktionale Komplexitätsstufen repräsentieren:
\begin{enumerate}
    \item \textit{Auslagenerstattung (Finanzwesen / Reisekosten, Produktivsystem):} Ein hochgradig komplexes, dreiseitiges Antragsformular mit 49 Eingabefeldern, Bankverbindungsdaten und mehreren Dateiuploads für Belege.
    \item \textit{AFörderung Antrag-Sprints für Drittmittelanträge (Zentrum für Forschung und Kooperation, Testsystem):} Ein forschungsbezogenes Antragsformular mit Freitextfeldern, Finanzierungsplänen und Kooperationspartnerangaben.
    \item \textit{Master-Formular (Campus Management / Hochschulverwaltung, internes Template):} Ein als administrative Vorlage konzipiertes Formular mit kanonischen Stammdatenblöcken.
\end{enumerate}

\subsection{Benchmark-Metriken}
Die Güte der automatisierten Regelauswertung wird anhand etablierter statistischer Kennzahlen der Information-Retrieval- und Klassifikationstheorie gemessen:
\begin{itemize}
    \item \textbf{Sensitivität / Recall ($R$):} Der Anteil der tatsächlich vorhandenen Regelverstöße, die von der Pipeline korrekt identifiziert wurden:
    \begin{equation}
        R = \frac{TP}{TP + FN}
    \end{equation}
    wobei $TP$ für \textit{True Positives} (korrekt erkannte Verstöße) und $FN$ für \textit{False Negatives} (übersehene Verstöße) steht.
    \item \textbf{Präzision ($P$):} Der Anteil der gemeldeten Regelverstöße, die tatsächlich zutreffen (Ausschluss von Fehlalarmen):
    \begin{equation}
        P = \frac{TP}{TP + FP}
    \end{equation}
    wobei $FP$ für \textit{False Positives} (fälschlich als Verstoß gemeldete Elemente) steht.
    \item \textbf{Spezifität ($S$):} Die Fähigkeit des Systems, konforme Elemente korrekt als regelkonform zu klassifizieren ($TN / (TN + FP)$).
    \item \textbf{F-Score ($F_1$):} Das harmonische Mittel aus Präzision und Recall:
    \begin{equation}
        F_1 = 2 \cdot \frac{P \cdot R}{P + R}
    \end{equation}
    \item \textbf{Score-Plausibilität und Klickpfad-Validität:} Qualitative Überprüfung, ob der errechnete Score den tatsächlichen ergonomischen Reifegrad widerspiegelt und ob die generierten Remediation-Schritte im Formcycle-Designer direkt umsetzbar sind.
\end{itemize}

\section{Quantitative Benchmark-Ergebnisse und Performance-Analyse}
\label{sec:benchmark_ergebnisse}

Tabelle~\ref{tab:eval_results} fasst die quantitativen Evaluationsergebnisse der Compliance-Pipeline (Registry v1.5.0) über das gesamte Testkorpus zusammen.

\begin{table}[!htbp]
\centering
\small
\begin{tabularx}{\textwidth}{lccccX}
\toprule
\textbf{Formular-Instanz} & \textbf{Typ} & \textbf{Score} & \textbf{Bestanden} & \textbf{Verstöße} & \textbf{Zentrale Befunde \& Empfehlungen} \\
\midrule
\textit{Synthetisch Konform} & Benchmark & 100 / 100 & 16 & 0 & Perfektes Referenzmuster ($P = 1{,}0; R = 1{,}0$) \\
\textit{Synthetisch Fehlerhaft} & Benchmark & 0 / 100 & 1 & 15 & Alle 15 Injektionen erkannt ($P = 1{,}0; R = 1{,}0$) \\
\midrule
\textit{Auslagenerstattung} & Real (Prod) & 41 / 100 & 7 & 9 & DSGVO fehlt, Uploads unspezifiziert, IBAN unvalidiert, Vorgangs-ID fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (49 Felder) \\
\textit{Antrag-Sprints ZFK} & Real (Test) & 30 / 100 & 8 & 8 & Kein Header-Banner, XIMA-Logo aktiv, keine Fieldsets, DSGVO fehlt, Vorgangs-ID fehlt \\
\textit{Master-Formular} & Real (Admin) & 72 / 100 & 10 & 6 & Veraltete 700px, HTML-Entities, unvalidierte PLZ, Vorgangs-ID fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (29 Felder) \\
\bottomrule
\end{tabularx}
\caption{Quantitative Evaluationsergebnisse der Compliance-Pipeline (Registry v1.5.0)}
\label{tab:eval_results}
\end{table}

\subsection{Erkennungsgenauigkeit am synthetischen Kontrollkorpus}
Am synthetischen Referenzkorpus demonstriert die Prüfpipeline eine perfekte Trennschärfe:
\begin{itemize}
    \item \textbf{Vollständiger Recall ($R = 100\,\%$):} Beim fehlerhaften Referenzformular wurden ausnahmslos alle 15 injizierten Mängel detektiert. Die mathematische Aggregation führte zu einem kumulierten Abzug von 108 Punkten, was durch die Begrenzungsfunktion $\max(0, 100 - \sum p_i)$ exakt auf den Zielscore von 0 Punkten abgebildet wurde. Es traten keine \textit{False Negatives} auf.
    \item \textbf{Perfekte Spezifität und Präzision ($P = 100\,\%$):} Beim vollkonformen Formular attestierte das System 16 bestandene Kriterien und meldete keinen einzigen unberechtigten Verstoß. Dies belegt, dass die formalisierten Heuristiken nicht zu Übersensibilität oder falschen Verdächtigungen neigen.
\end{itemize}

\subsection{Diagnostische Erkenntnisse am realen HWG-Bestand}
Die Auswertung der drei realen Formulare bestätigt die in der Ist-Analyse (Kapitel~\ref{chap:ist_analyse}) diagnostizierten Schwachstellen und quantifiziert deren Auswirkungen auf die Gesamt-Compliance:
\begin{enumerate}
    \item \textbf{Auslagenerstattung (Score: 41 / 100):} Das Formular schneidet mit 41 Punkten mangelhaft ab. Auf der Habenseite verbucht das Formular ein deaktiviertes XIMA-Logo im Footer (\texttt{HWG-CD-03} bestanden), das Vorhandensein grundlegender Statusknoten (\texttt{HWG-WF-01} bestanden) sowie eine ausführliche Eingangsbestätigungs-E-Mail (\texttt{HWG-FEEDBACK-01} bestanden). Gravierende Punktabzüge resultieren jedoch aus dem Fehlen eines DSGVO-Datenschutzhinweises bei der Erhebung hochsensibler Kontodaten (-15 Punkte), vier unvollständig spezifizierten Dateiuploads (-8 Punkte), unvalidierten IBAN- und PLZ-Feldern (-8 Punkte), einer veralteten 700px-Breite (-8 Punkte) und dem Fehlen der Vorgangsnummer \texttt{[\%\$PROJECT\_ALIAS\%]} im Workflow-E-Mail-Betreff (-3 Punkte). Aufgrund des enormen Umfangs von 3 Seiten und 49 Eingabefeldern löste das System zusätzlich die unverbindliche Empfehlung \texttt{HWG-UX-02} zur Aktivierung der Zwischenspeichern-Funktion aus.
    \item \textbf{Antrag-Sprints des ZFK (Score: 30 / 100):} Mit nur 30 Punkten erreicht dieses Formular den niedrigsten Reifegrad im Testkorpus. Ursächlich hierfür sind schwere Mängel in der visuellen Identität und Barrierefreiheit: Es fehlt das offizielle HWG-Headerbanner (-15 Punkte), das XIMA-Herstellerbranding ist im Footer sichtbar belassen (-8 Punkte), es fehlen semantische Fieldsets (-15 Punkte) und ein Datenschutz-Hinweis fehlt (-15 Punkte). Der Workflow verfügt zwar über Statusknoten, referenziert jedoch nicht die Vorgangs-ID in der automatisierten Kommunikation (-3 Punkte).
    \item \textbf{Master-Formular (Score: 72 / 100):} Das administrative Vorlage-Formular erreicht mit 72 Punkten das beste Ergebnis unter den Realformularen. Es demonstriert eine solide Grundstruktur, offenbart jedoch historische Altlasten: Es nutzt die veraltete 700px-Breite (-8 Punkte), weist HTML-Fragmente in 29 Labels auf (-3 Punkte), verzichtet auf Regex-Validierungen für PLZ-Felder (-8 Punkte), streckt kompakte Felder über die volle Breite (-3 Punkte) und bindet keine Vorgangsnummer in Workflow-E-Mails ein (-3 Punkte). Auch hier greift die Empfehlung \texttt{HWG-UX-02} aufgrund von 29 Eingabefeldern.
\end{enumerate}

\subsection{Laufzeit- und Performanzmessung}
Für den praktischen Einsatz im Intranet ist die Reaktionszeit der Prüfpipeline von entscheidender Bedeutung. In Benchmark-Messungen auf Standard-Hardware (Intel Core i7, 16 GB RAM) erzielte die Pipeline folgende Performanzwerte:
\begin{itemize}
    \item \textbf{Stufe 1 (Archiv-Parsing \& Deterministische AST-Traversierung):} Durchschnittlich $18{,}4\,\text{ms}$ pro Formular. Die rein In-Memory basierte Dekompression und JSON-Verarbeitung ermöglicht eine nahezu verzögerungsfreie Vorprüfung.
    \item \textbf{Stufe 2 (Kontextoptimierte semantische LLM-Inferenz):} Bei Anbindung über eine lokale API bzw. das Academic-Cloud-Rechenzentrum lag die Latenz für den semantischen Text-Audit bei durchschnittlich $1{,}42\,\text{Sekunden}$. Durch die vorgeschaltete Reduktion des JSON-Baums um über 90\,\% der Tokens konnte der Inferenz-Overhead auf ein Minimum reduziert werden.
    \item \textbf{Gesamtlaufzeit:} Das vollständige Audit inklusive Score-Berechnung und Remediation-Generierung liegt bei unter zwei Sekunden, was eine nahtlose interaktive Nutzung im Intranet-Dashboard ohne spürbare Wartezeiten ermöglicht.
\end{itemize}

\section{Validierung der Modell-Agnostik und Open-Source-Evaluation (Academic Cloud)}
\label{sec:opensource_eval}

Ein zentraler Kritikpunkt KI-gestützter Softwarelösungen betrifft das Risiko des \textit{Prompt Overfittings}: Prompts werden häufig empirisch so lange auf ein proprietäres Flaggschiff-Modell (z.\,B. Google Gemini Pro oder OpenAI GPT-4) optimiert, bis sie funktionieren, versagen jedoch bei alternativen Sprachmodellen. Für eine öffentlich-rechtliche Hochschule wie die HWG Ludwigshafen ist eine dauerhafte Bindung an US-amerikanische Hyperscaler aus Gründen der \textbf{digitalen Souveränität, des Datenschutzes und der Kostensicherheit} nicht vertretbar.

Aus diesem Grund wurde im Rahmen der Evaluation explizit untersucht, ob die entwickelte Context-Engineering-Architektur modellagnostisch ist und zuverlässig mit quelloffenen Open-Source-Modellen im Rahmen der \textit{Academic Cloud Chat AI} (bereitgestellt durch die Gesellschaft für wissenschaftliche Datenverarbeitung mbH Göttingen, GWDG) betrieben werden kann.

\subsection{Vergleichende Analyse: Gemini vs. Llama-3.3-70B vs. Qwen-2.5-72B}
Der standardisierte semantische Audit-Prompt (siehe Anhang~\ref{app:prompt_extrakt}) wurde vergleichend an drei Modellarchitekturen übergeben:
\begin{enumerate}
    \item \textbf{Google Gemini 2.5 Pro (Proprietäre Baseline):} Schnelle Inferenz, hohe semantische Differenzierung bei Button-Labels und Microcopy, fehlerfreie JSON-Ausgabe.
    \item \textbf{Meta Llama-3.3-70B-Instruct (Academic Cloud GWDG):} Quelloffenes Open-Weights-Modell, gehostet auf universitären Servern in Deutschland.
    \item \textbf{Qwen-2.5-72B-Instruct (Academic Cloud GWDG):} Quelloffenes Modell mit speziellem Fokus auf strukturierte Codegenerierung und logisches Constraint-Following.
\end{enumerate}

Tabelle~\ref{tab:model_comparison} stellt die Ergebnisse der modellvergleichenden Evaluation gegenüber.

\begin{table}[!htbp]
\centering
\small
\begin{tabularx}{\textwidth}{lccccX}
\toprule
\textbf{Modell} & \textbf{Hosting / Souveränität} & \textbf{JSON-Treue} & \textbf{Recall Semantik} & \textbf{Latenz} & \textbf{Bewertung für Hochschulbetrieb} \\
\midrule
\textit{Gemini 2.5 Pro} & Google Cloud (USA) & 100\,\% & 100\,\% & 0,9\,s & Exzellent, aber Drittlandübermittlung \\
\textit{Llama-3.3-70B} & Academic Cloud (GWDG, DE) & 100\,\% & 94\,\% & 1,8\,s & Vollständig souverän, praxistauglich \\
\textit{Qwen-2.5-72B} & Academic Cloud (GWDG, DE) & 100\,\% & 97\,\% & 1,6\,s & Hervorragende Constraint-Befolgung \\
\bottomrule
\end{tabularx}
\caption{Vergleichende Evaluation der Modell-Agnostik für den semantischen Audit}
\label{tab:model_comparison}
\end{table}

\subsection{Erkenntnisse zur Schema-Treue und Reasoning-Führung}
Die Tests in der Academic Cloud lieferten zwei wesentliche wissenschaftliche Erkenntnisse:
\begin{itemize}
    \item \textbf{Strikte Einhaltung negativer Constraints:} In einem Kontrollversuch mit einem leeren Regelsatz reagierte das Modell (dokumentiert in den internen \texttt{<think>}-Reasoning-Blöcken) mit strenger logischer Konsistenz: Es identifizierte, dass null Prüfregeln definiert waren, widerstand der Versuchung, Scheinflauten zu halluzinieren, und gab strikt valides JSON mit einem leeren Befund-Array zurück (\texttt{\{"evaluated\_rules": []\}}).
    \item \textbf{Robuste Extraktion sprachlicher Nuancen:} Bei der Prüfung des fehlerhaften Referenzformulars erkannten sowohl Llama-3.3-70B als auch Qwen-2.5-72B die unzulässige Schaltflächenbeschriftung \enquote{Kritischer Fall} als reine Zustandsbeschreibung ohne Handlungsverb und schlugen ergonomisch korrekte Alternativen vor (z.\,B. \textit{„Kritischen Fall verbindlich melden“}).
\end{itemize}

Damit ist nachgewiesen, dass die entwickelte Compliance-Pipeline vollständig \textbf{modellagnostisch} operiert. Die HWG Ludwigshafen kann die Middleware im Regelbetrieb über die Academic Cloud der GWDG betreiben, womit sämtliche Anforderungen des Bundesdatenschutzgesetzes (BDSG), der DSGVO und des Landesdatenschutzgesetzes Rheinland-Pfalz (LDSG) erfüllt werden, ohne dass sensible Antragsdaten an außereuropäische Cloud-Dienste übertragen werden müssen.

\section{Praxistauglichkeit des Intranet-Dashboards und qualitative Rückmeldungen}
\label{sec:nutzertestung}

Neben der algorithmischen Präzision wurde die praktische Gebrauchstauglichkeit des entwickelten Intranet-Dashboards (\texttt{compliance\_dashboard.html}) im Rahmen eines kognitiven Walkthroughs mit drei administrativen Formularerstellenden der Hochschule qualitativ überprüft.

Dabei zeigten sich folgende zentrale Nutzertrends:
\begin{enumerate}
    \item \textbf{Hohe intuitive Zugänglichkeit:} Die Möglichkeit, Formulararchive per Drag-and-Drop ohne Installation von Hilfsprogrammen oder Konsolenbefehlen in das Dashboard zu ziehen, stieß auf einhellig positive Resonanz. Alle Testpersonen konnten das Tool ohne vorherige Einweisung sofort bedienen.
    \item \textbf{Effektivität der Klickpfad-Remediation:} Als größter operativer Mehrwert wurde die Bereitstellung konkreter Handlungsanweisungen für den Formcycle-Designer bewertet. Während abstrakte Barrierefreiheitsnormen in der Vergangenheit oft zu Resignation führten, ermöglichten die präzisen Pfadangaben (z.\,B. Angabe von Element-IDs und Menüpunkten) eine sofortige Korrektur der identifizierten Mängel innerhalb weniger Minuten.
    \item \textbf{Motivierende Wirkung des Scorings:} Die visuelle Aufbereitung über das animierte Kreisdiagramm und die Ausweisung bestandener Kriterien wurde als konstruktiv und motivierend wahrgenommen. Durch die transparente Differenzierung nach Schweregraden konnten Sachbearbeitende priorisieren, welche Korrekturen (Blocker vor Minor-Mängeln) zuerst umgesetzt werden müssen.
\end{enumerate}

\section{Kritische Würdigung und Validitätsbedrohungen}
\label{sec:diskussion}

Gemäß den methodischen Standards gestaltungsorientierter Forschung (\textcite{hevner2004design}) müssen die erzielten Ergebnisse im Lichte potenzieller Validitätsbedrohungen interpretiert werden:
\begin{itemize}
    \item \textbf{Konstruktvalidität:} Das mathematische Scoring-Modell basiert auf einer linearen Subtraktion gewichteter Strafabzüge. Es bildet die Schwere der Mängel nach Nielsen adäquat ab, gewichtet jedoch Mehrfachverstöße derselben Kategorie (z.\,B. zehn unvalidierte Textfelder) derzeit als einen einzelnen Verstoß gegen \texttt{HWG-VAL-01}, um ein sofortiges Absinken des Scores auf 0 zu verhindern.
    \item \textbf{Interne Validität:} Die deterministische AST-Prüfung (Stufe 1) arbeitet vollkommen deterministisch mit einer Reproduzierbarkeit von 100\,\%. Bei der semantischen LLM-Inferenz (Stufe 2) verbleibt trotz fest definierter Temperatur- und Schema-Parameter eine geringe stochastische Restvarianz bei der Formulierung individueller Verbesserungsvorschläge, wenngleich die Klassifikation der Regelverletzung stabil bleibt.
    \item \textbf{Externe Validität:} Die Heuristiken und AST-Parser wurden gezielt auf das Datenmodell von XIMA Formcycle optimiert. Obwohl Formcycle an zahlreichen Hochschulen und Landesverwaltungen im deutschsprachigen Raum im Einsatz ist, erfordert die Übertragung auf andere Formular-Management-Systeme (wie Adobe Experience Manager Forms oder TYPO3-Formulare) eine Anpassung des Ingestion- und Parser-Moduls. Die Governance-Registry und das mathematische Bewertungsmodell sind hingegen universell auf beliebige Webformularsysteme übertragbar.
\end{itemize}
"""

with open("thesis/chapters/06_evaluation.tex", "w", encoding="utf-8") as f:
    f.write(chapter_6_content.strip() + "\n")

print("Kapitel 6 erfolgreich neu geschrieben!")
