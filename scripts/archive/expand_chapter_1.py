import os

chapter_1_content = r"""\chapter{Einleitung und Problemstellung}
\label{chap:einleitung}

\section{Ausgangssituation und Motivation}
\label{sec:ausgangssituation}

Die digitale Transformation der öffentlichen Verwaltung in Deutschland befindet sich in einer entscheidenden Konsolidierungsphase. Während die erste Welle der Verwaltungsdigitalisierung primär auf die elektronische Bereitstellung von Dokumenten und Formularen im PDF-Format abzielte, fordern moderne E-Government-Rahmenwerke heute volldigitale, medienbruchfreie und durchgängig integrierte End-to-End-Prozesse. Auf bundes- und landesgesetzlicher Ebene setzen das Onlinezugangsgesetz (OZG bzw. OZG 2.0), das E-Government-Gesetz des Landes Rheinland-Pfalz (EGovG RLP) sowie europäische Vorgaben wie das \textit{Single Digital Gateway} (SDG) und die Richtlinie (EU) 2016/2102 verbindliche Standards für die Digitalisierung von Bürgerservices. Für staatliche Einrichtungen des tertiären Bildungssektors gilt diese Verpflichtung uneingeschränkt: Hochschulen müssen ihre administrativen Dienstleistungen für Studierende, Lehrende, Forschende, Beschäftigte und externe Kooperationspartner barrierefrei, rechtssicher und nutzerzentriert digital zugänglich machen.

Digitale Webformulare bilden dabei den Dreh- und Angelpunkt der hochschulischen Interaktion. Ob Immatrikulation, Prüfungsanmeldung, Urlaubssemester, Dienstreiseantrag, Drittmittelbeantragung oder die Erstattung von Auslagen – nahezu jeder akademische und verwaltungsbezogene Geschäftsvorgang wird über Webformulare initiiert, strukturiert erfasst und in nachgelagerte Fachverfahren (z.\,B. Campus-Management- oder ERP-Systeme) überführt. Die Qualität dieser digitalen Schnittstellen bestimmt maßgeblich die Effizienz der Sachbearbeitung, die Zufriedenheit der Nutzenden und die Fehleranfälligkeit des gesamten Verwaltungshandelns (\textcite{wroblewski2008web, bargas2010usable}).

Zur Bewältigung dieser Digitalisierungsaufgabe führte die Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG Ludwigshafen) das Enterprise-Formular-Management-System (FMS) \textit{XIMA Formcycle} ein. Formcycle stellt eine No-Code- bzw. Low-Code-Plattform bereit, die es den dezentralen Organisationseinheiten der Hochschule – den vier Fachbereichen, dem Studierendenservice, der Personalabteilung, dem Finanzwesen sowie dem Zentrum für Forschung und Kooperation (ZFK) – ermöglicht, Webformulare und automatisierte Nachbearbeitungs-Workflows eigenständig zu erstellen, anzupassen und zu publizieren. 

Dieser dezentrale Low-Code-Ansatz löst zwar das Kapazitätsproblem zentraler IT-Abteilungen und beschleunigt die Bereitstellung neuer Online-Dienste; in der Praxis führt er jedoch zu einem gravierenden \textit{Governance- und Compliance-Vakuum}. Da den dezentralen Formularerstellenden in der Regel das spezialisierte Fachwissen in den Bereichen Software-Ergonomie, Web-Accessibility und Datenschutzrecht fehlt und bislang kein verbindlicher, maschinenlesbar verankerter Gestaltungsstandard existiert, ist im Laufe der Jahre eine heterogene Landschaft an Insellösungen entstanden. Eine explorative Voruntersuchung des Formularbestands der HWG Ludwigshafen offenbart fundamentale Gestaltungsdiskrepanzen:
\begin{itemize}
    \item \textbf{Inkonsistentes visuelles Corporate Design:} Veraltete Desktop-Layoutbreiten (700px) wechseln unvorhersehbar mit modernen Breiten (850px); offizielle Hochschul-Header und Logos fehlen in zahlreichen Vorlagen vollständig, wodurch die institutionelle Authentizität und das Vertrauen der Nutzenden untergraben werden.
    \item \textbf{Defizite in der digitalen Barrierefreiheit (WCAG 2.1 / BITV 2.0):} Semantische HTML-Strukturelemente (\texttt{<fieldset>}, \texttt{<legend>}) werden häufig durch rein optische Container ersetzt. Pflichtfeldmarkierungen sind für assistive Technologien wie Screenreader oft nicht programmatisch auslesbar hinterlegt, und rohe HTML-Entitäten in Feldbezeichnungen stören die Sprachausgabe.
    \item \textbf{Ergonomische Brüche und mangelnde Microcopy:} Schaltflächenbeschriftungen genügen selten dem ergonomisch geforderten \textit{Action-Verb-Pattern}. Statt präziser Handlungsanweisungen finden sich generische Bezeichnungen (\texttt{senden}) oder irritierende Zustandsbegriffe (\enquote{Kritischer Fall}), die gegen elementare Prinzipien der Dialogführung (DIN EN ISO 9241-110) verstoßen.
    \item \textbf{Rechtliche Compliance und Datenschutz:} Bei Formularen, die hochsensible personenbezogene Daten erheben, fehlen vielfach transparente Hinweise auf die Rechtsgrundlagen der Verarbeitung gemäß Art. 13 DSGVO.
    \item \textbf{Intransparenz in automatisierten Workflows:} Den Einreichenden mangelt es nach dem Absenden häufig an einer verbindlichen Eingangsbestätigung, klaren Prozessinformationen und einer konsistenten Vorgangsnummer zur Nachverfolgbarkeit.
\end{itemize}

Bisherige Versuche, diese Mängel über statische Richtliniendokumente (PDF-Leitfäden oder Styleguides) einzudämmen, scheitern in der Praxis regelmäßig: Statische Dokumente sind langatmig, werden im Arbeitsalltag selten konsultiert und bieten keine proaktive Unterstützung bei der Fehlerbehebung. Gleichzeitig ist ein manuelles Experten-Audit jedes neu erstellten oder modifizierten Formulars angesichts beschränkter personeller Ressourcen ökonomisch nicht tragfähig. Hieraus erwächst die dringende Notwendigkeit eines automatisierten, kontinuierlichen und praxisorientierten Qualitätsaudits, das direkt an den Artefakten der Formularplattform ansetzt.

\section{Zielsetzung und forschungsleitende Fragestellungen}
\label{sec:zielsetzung}

Das übergeordnete Ziel der vorliegenden Bachelorarbeit besteht darin, diese Lücke durch einen theoriegeleiteten, methodisch fundierten und technisch validierten Lösungsansatz zu schließen. Dies umfasst die \textbf{Konzeption eines harmonisierten, verbindlichen Formular-Standards für die HWG Ludwigshafen} sowie die \textbf{prototypische Entwicklung und Evaluation einer automatisierten, hybriden Compliance-Prüfpipeline}, welche Formcycle-Vorlagen objektiv auditiert, Abweichungen mathematisch quantifiziert und handlungsorientierte Korrekturpfade bereitstellt.

Aus dieser Zielsetzung leitet sich die primäre Forschungsfrage (\textit{Main Research Question, MRQ}) ab:
\begin{quote}
    \textit{\textbf{MRQ:} Wie kann ein einheitlicher, barrierefreier und ergonomischer Formular-Standard für die HWG Ludwigshafen konzipiert und dessen Einhaltung durch eine automatisierte Prüfpipeline in Formcycle prototypisch durchgesetzt werden?}
\end{quote}

Zur systematischen Beantwortung der Hauptforschungsfrage wird diese in vier methodisch aufeinander aufbauende Teilforschungsfragen (\textit{Sub-Questions, FQ}) untergliedert:
\begin{enumerate}
    \item[\textbf{FQ1:}] \textit{Welche empirischen Gestaltungs-, Usability- und Barrierefreiheitsdefizite kennzeichnen den aktuellen Formularbestand der HWG Ludwigshafen, und wie verteilen sich diese über dezentrale Organisationseinheiten?}
    \item[\textbf{FQ2:}] \textit{Welche formalen, visuellen, semantischen und prozessualen Kriterien müssen in einem maschinenlesbaren Formular-Standard spezifiziert werden, um den normativen Anforderungen der DIN EN ISO 9241-110, der BITV 2.0 und der DSGVO gerecht zu werden?}
    \item[\textbf{FQ3:}] \textit{Wie muss eine zweistufige, hybride Prüf-Architektur aus deterministischer AST-Strukturprüfung und kontextoptimiertem LLM-Context-Engineering technisch gestaltet sein, um Formcycle-Artefakte verlässlich und ohne False-Positive-Verzerrungen zu evaluieren?}
    \item[\textbf{FQ4:}] \textit{Mit welcher Präzision, Robustheit und Latenz identifiziert die entwickelte Pipeline Regelverstöße im Vergleich zu synthetischen Referenzmustern und realen Anträgen, und inwieweit lässt sich das System unabhängig von proprietären Sprachmodellen betreiben?}
\end{enumerate}

\section{Forschungsmethodischer Aufbau der Arbeit}
\label{sec:aufbau}

Die wissenschaftliche Vorgehensweise dieser Arbeit orientiert sich an den Prinzipien der gestaltungsorientierten Wirtschaftsinformatik (\textit{Design Science Research, DSR}) nach \textcite{hevner2004design} und dem Prozessmodell nach \textcite{peffers2007design}. Der DSR-Ansatz eignet sich in besonderer Weise für die vorliegende Problemstellung, da er die theoriegeleitete Konstruktion innovativer soziotechnischer Artefakte zur Lösung realer organisatorischer Probleme mit einer rigorosen empirischen Evaluation verbindet.

Der Aufbau der Arbeit gliedert sich entlang der DSR-Phasen in sieben Kapitel:
\begin{enumerate}
    \item \textbf{Kapitel 1 (Einleitung und Problemstellung):} Umreißt die motivationale Ausgangslage, formuliert die Problemstellung im Kontext der Hochschuldigitalisierung, leitet die forschungsleitenden Fragen ab und stellt das methodische Vorgehen dar.
    \item \textbf{Kapitel 2 (Theoretischer Hintergrund und Stand der Forschung):} Etabliert das theoretische Fundament der Arbeit. Es analysiert die software-ergonomischen Normen der Dialoggestaltung (DIN EN ISO 9241-110), gesetzliche Barrierefreiheitsstandards (WCAG 2.1, BITV 2.0), formale Usability-Heuristiken und Nielsen-Schweregrade sowie den aktuellen Forschungsstand zum Einsatz von Large Language Models (LLMs) in automatisierten Heuristik-Audits.
    \item \textbf{Kapitel 3 (Empirische Ist-Analyse des Formularbestands):} Dokumentiert die systematische Bestandsaufnahme und Komponenten-Analyse von 34 realen Formularen der HWG Ludwigshafen sowie die Untersuchung von 49 Workflow-Definitionen. Anhand detaillierter DOM- und Parameteruntersuchungen werden sechs fundamentale Problemfelder herausgearbeitet.
    \item \textbf{Kapitel 4 (Konzeption des einheitlichen Formular-Standards):} Führt die Soll-Konzeption ein und formalisiert diese in einer maschinenlesbaren Compliance-Registry (\texttt{rules\_registry.json}) mit 21 Governance-Regeln und einem deterministischen, nach Nielsen-Schweregraden gewichteten Scoring-Modell.
    \item \textbf{Kapitel 5 (Prototypische Implementierung der Prüfpipeline):} Beschreibt die technische Realisierung der hybriden Prüf-Middleware und des barrierefreien Intranet-Dashboards. Neben der deterministischen AST-Traversierung und dem semantischen Context-Engineering werden die formalen Algorithmen und das praxisorientierte Klickpfad-Remediation-System detailliert.
    \item \textbf{Kapitel 6 (Empirische Evaluation):} Validiert das Gesamtsystem anhand synthetischer Ground-Truth-Formulare (100\,\% Best-Practice vs. 0\,\% Worst-Case) sowie realer Anträge aus dem Produktiv- und Testsystem der Hochschule. Darüber hinaus wird die Modellauswahl kritisch diskutiert und die Eignung offener, datenschutzkonformer Open-Source-Sprachmodelle für den autonomen Hochschulbetrieb analysiert.
    \item \textbf{Kapitel 7 (Fazit und Ausblick):} Fasst die wesentlichen wissenschaftlichen und praktischen Erkenntnisse thesenartig zusammen, beantwortet die Forschungsfragen, reflektiert die methodischen Limitationen und zeigt Anknüpfungspunkte für zukünftige Forschungsarbeiten auf.
\end{enumerate}
"""

with open("thesis/chapters/01_einleitung.tex", "w", encoding="utf-8") as f:
    f.write(chapter_1_content.strip() + "\n")

print("Kapitel 1 erfolgreich neu geschrieben!")
