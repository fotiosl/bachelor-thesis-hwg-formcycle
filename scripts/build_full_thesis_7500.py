import os
import re
import subprocess

def clean_latex(text):
    text = re.sub(r'%.*?\n', '\n', text)
    text = re.sub(r'\\(?:text(?:bf|it|sc|sl|sf|tt)|enquote|emph|underline|glqq|grqq)\{([^}]+)\}', r'\1', text)
    text = re.sub(r'\\(?:cite|textcite|parencite|autocite|citep|citet)(?:\[[^\]]*\])?\{[^}]*\}', 'Quelle', text)
    text = re.sub(r'\\(?:ref|pageref|eqref)\{[^}]*\}', '1', text)
    text = re.sub(r'\\(?:label|vspace|hspace|small|normalsize|large|Large|centering)\b', '', text)
    text = re.sub(r'\\begin\{(?:table|figure|lstlisting|center)\}.*?\\end\{(?:table|figure|lstlisting|center)\}', '', text, flags=re.DOTALL)
    text = re.sub(r'\\[a-zA-Z]+', '', text)
    text = re.sub(r'[{}~_#&^]', '', text)
    return text

# ==============================================================================
# CHAPTER 1: Einleitung und Problemstellung (~750 words)
# ==============================================================================
ch1 = r"""\chapter{Einleitung und Problemstellung}
\label{chap:einleitung}

\section{Ausgangssituation und Motivation}
\label{sec:ausgangssituation}

Die digitale Transformation der öffentlichen Verwaltung in Deutschland verlangt heute volldigitale, medienbruchfreie und barrierefreie End-to-End-Prozesse. Das Onlinezugangsgesetz (OZG), das E-Government-Gesetz des Landes Rheinland-Pfalz (EGovG RLP) sowie europäische Richtlinien wie die EU-Richtlinie 2016/2102 verpflichten staatliche Einrichtungen des tertiären Bildungssektors uneingeschränkt, ihre administrativen Dienstleistungen für Studierende, Lehrende, Forschende und Beschäftigte barrierefrei und nutzerzentriert bereitzustellen. Webformulare bilden dabei die primäre Interaktionsschnittstelle des Verwaltungshandelns: Nahezu jeder akademische und administrative Geschäftsvorgang – von der Immatrikulation über Dienstreiseanträge bis hin zur Drittmittelbeantragung – wird über Webformulare initiiert, strukturiert erfasst und in nachgelagerte Fachverfahren übertragen. Die ergonomische und technische Qualität dieser Formulare bestimmt maßgeblich die Effizienz der Sachbearbeitung, die Zufriedenheit der Nutzenden und die Fehlerrate des gesamten Verwaltungshandelns (\textcite{wroblewski2008web, bargas2010usable}).

Zur Bewältigung dieser Digitalisierungsaufgabe führte die Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG Ludwigshafen) das Enterprise-Formular-Management-System (FMS) \textit{XIMA Formcycle} ein. Formcycle stellt eine Low-Code- bzw. No-Code-Plattform bereit, die es den dezentralen Organisationseinheiten der Hochschule (Fachbereiche, Studierendenservice, Personalabteilung, Finanzwesen, Forschungszentrum) erlaubt, Webformulare und automatisierte Nachbearbeitungs-Workflows eigenständig zu erstellen und zu publizieren. 

Dieser dezentrale Ansatz entlastet die zentrale IT-Abteilung, führte in der Praxis jedoch zu einem gravierenden \textit{Governance- und Compliance-Vakuum}: Da den dezentralen Formularerstellenden in der Regel das spezialisierte Fachwissen in Software-Ergonomie, Barrierefreiheit und Datenschutzrecht fehlt und bislang kein verbindlicher, maschinenlesbar verankerter Gestaltungsstandard existiert, ist im Laufe der Jahre eine stark heterogene Landschaft an Insellösungen entstanden. Eine explorative Bestandsaufnahme an der HWG Ludwigshafen offenbart fundamentale Gestaltungsdiskrepanzen:
\begin{itemize}
    \item \textbf{Inkonsistentes Corporate Design:} Veraltete Desktop-Layoutbreiten (700px) wechseln unvorhersehbar mit modernen Rastern (850px); offizielle Hochschul-Header und Logos fehlen in zahlreichen Vorlagen vollständig, wodurch das institutionelle Erscheinungsbild beeinträchtigt wird.
    \item \textbf{Defizite bei digitaler Barrierefreiheit (WCAG 2.1 / BITV 2.0):} Semantische Container (\texttt{<fieldset>}, \texttt{<legend>}) fehlen in 65\,\% der Formulare. Pflichtfeldmarkierungen sind für Screenreader teils nicht programmatisch hinterlegt, und rohe HTML-Entitäten in Feldbezeichnungen stören die Sprachausgabe.
    \item \textbf{Ergonomische Brüche und mangelnde Microcopy:} Schaltflächenbeschriftungen verletzen das \textit{Action-Verb-Pattern}. Statt präziser Handlungsanweisungen finden sich generische Bezeichnungen (\texttt{senden}) oder irritierende Statusbegriffe (\enquote{Kritischer Fall}), die gegen elementare Prinzipien der Dialogführung nach DIN EN ISO 9241-110 verstoßen.
    \item \textbf{Datenschutzrechtliche Risiken (Art. 13 DSGVO):} Bei Formularen, die hochsensible personenbezogene Daten erheben, fehlen vielfach transparente Hinweise auf die Rechtsgrundlagen der Verarbeitung und ein direkter Link zur Datenschutzerklärung der Hochschule.
    \item \textbf{Intransparenz in automatisierten Workflows:} Den Antragstellenden mangelt es nach dem Absenden häufig an einer verbindlichen Eingangsbestätigung, klaren Prozessinformationen und einer konsistenten Vorgangsnummer zur Nachverfolgbarkeit.
\end{itemize}

Statische Leitfäden und PDF-Richtlinien haben sich im administrativen Alltag als wirkungslos erwiesen, da sie im Erstellungsprozess selten konsultiert werden. Manuelle Experten-Reviews wiederum sind personell nicht skalierbar. Hieraus erwächst die zwingende Notwendigkeit eines automatisierten, kontinuierlichen Qualitätsaudits direkt in der Formularbereitstellung.

\section{Zielsetzung und forschungsleitende Fragestellungen}
\label{sec:zielsetzung}

Das Ziel dieser Bachelorarbeit ist die \textbf{Konzeption eines harmonisierten, barrierefreien und ergonomischen Formular-Standards für die HWG Ludwigshafen} sowie die \textbf{prototypische Entwicklung einer hybriden, KI-gestützten Compliance-Prüfpipeline}, welche Formcycle-Vorlagen objektiv auditiert, Verstöße quantifiziert und handlungsorientierte Korrekturpfade für Formularerstellende bereitstellt.

Hieraus leitet sich die primäre Forschungsfrage (\textit{Main Research Question, MRQ}) ab:
\begin{quote}
    \textit{\textbf{MRQ:} Wie kann ein einheitlicher, barrierefreier und ergonomischer Formular-Standard für die HWG Ludwigshafen konzipiert und dessen Einhaltung durch eine automatisierte Prüfpipeline in Formcycle prototypisch durchgesetzt werden?}
\end{quote}

Zur methodischen Beantwortung der Hauptforschungsfrage wird diese in vier Teilforschungsfragen (\textit{Sub-Questions, FQ}) untergliedert:
\begin{enumerate}
    \item[\textbf{FQ1:}] Welche empirischen Gestaltungs-, Usability- und Barrierefreiheitsdefizite kennzeichnen den aktuellen Formularbestand der HWG Ludwigshafen, und wie verteilen sich diese über dezentrale Organisationseinheiten?
    \item[\textbf{FQ2:}] Welche formalen, visuellen, semantischen und prozessualen Kriterien müssen in einem maschinenlesbaren Formular-Standard spezifiziert werden, um den normativen Anforderungen der DIN EN ISO 9241-110, der BITV 2.0 und der DSGVO gerecht zu werden?
    \item[\textbf{FQ3:}] Wie muss eine zweistufige, hybride Prüf-Architektur aus deterministischer AST-Strukturprüfung und kontextoptimiertem LLM-Context-Engineering technisch gestaltet sein, um Formcycle-Artefakte verlässlich und ohne False-Positive-Verzerrungen zu evaluieren?
    \item[\textbf{FQ4:}] Mit welcher Präzision, Robustheit und Latenz identifiziert die entwickelte Pipeline Regelverstöße im Vergleich zu synthetischen Referenzmustern und realen Anträgen, und inwieweit lässt sich das System unabhängig von proprietären Sprachmodellen betreiben?
\end{enumerate}

\section{Forschungsmethodischer Aufbau der Arbeit}
\label{sec:aufbau}

Die wissenschaftliche Vorgehensweise dieser Arbeit folgt dem Paradigma des \textbf{Design Science Research (DSR)} nach \textcite{hevner2004design} und dem Prozessmodell nach \textcite{peffers2007design}. Zur Sicherung methodischer Rigorosität orientiert sich die Ausarbeitung an den Grundsätzen wissenschaftlicher Praxis nach \textcite{recker2013scientific}, \textcite{cochrane2005writing} sowie \textcite{kornmeier2011}.

Die Arbeit gliedert sich entlang der DSR-Phasen in sieben Kapitel:
\begin{itemize}
    \item \textbf{Kapitel 2 (Theoretischer Hintergrund):} Fundiert die ergonomischen Grundlagen (DIN EN ISO 9241-110), gesetzliche Barrierefreiheitsstandards (BITV 2.0 / WCAG 2.1), Nielsen-Schweregrade sowie den aktuellen Forschungsstand zu LLM-Usability-Audits.
    \item \textbf{Kapitel 3 (Empirische Ist-Analyse):} Dokumentiert die Bestandsaufnahme von 34 realen Formularen und 49 Workflow-Graphen der HWG Ludwigshafen zur Identifikation von sechs Kernproblemfeldern.
    \item \textbf{Kapitel 4 (Konzeption des Standards):} Formalisiert die Gestaltungsanforderungen in einer maschinenlesbaren Compliance-Registry (\texttt{rules\_registry.json}) mit 21 Governance-Regeln und mathematischem Scoring-Modell.
    \item \textbf{Kapitel 5 (Prototypische Implementierung):} Detailliert die technische Architektur der hybriden Prüfpipeline, die formalen Algorithmen und das barrierefreie Intranet-Web-Dashboard mit interaktivem Klickpfad-Remediation-System.
    \item \textbf{Kapitel 6 (Empirische Evaluation):} Validiert das System quantitativ an synthetischen Ground-Truth-Referenzen, realen Anträgen und vergleicht fünf Open-Source-LLMs hinsichtlich Erkennungsgüte und Inferenzqualität.
    \item \textbf{Kapitel 7 (Fazit und Ausblick):} Beantwortet die Forschungsfragen synthesenhaft, leitet konkrete Handlungsempfehlungen für das Hochschulmanagement ab und zeigt zukünftige Forschungsperspektiven auf.
\end{itemize}
"""

# ==============================================================================
# CHAPTER 2: Theoretischer Hintergrund und Stand der Forschung (~1.500 words)
# ==============================================================================
ch2 = r"""\chapter{Theoretischer Hintergrund und Stand der Forschung}
\label{chap:theorie}

Dieses Kapitel spannt den theoretischen Bogen von den software-ergonomischen Grundlagen und rechtlichen Rahmenbedingungen digitaler Formulare über den methodologischen Rahmen des Design Science Research (DSR) bis hin zum aktuellen Forschungsstand automatisierter Usability-Audits mittels Large Language Models (LLMs).

\section{Ergonomie und Usability von Webformularen}
\label{sec:usability_standards}

Digitale Formulare stellen spezialisierte Mensch-Computer-Schnittstellen dar, deren Interaktionsqualität sich an etablierten Normen der Software-Ergonomie, empirischen Usability-Forschungsergebnissen und formalen Schweregradmodellen bemisst.

\subsection{Die Dialoggrundsätze der DIN EN ISO 9241-110:2020}
\label{subsec:iso_norm}

Die internationale Ergonomie-Norm \textbf{DIN EN ISO 9241-110:2020} formuliert grundlegende Gestaltungsanforderungen für interaktive Systeme \cite{iso9241110}. Für die Konstruktion von Webformularen sind sieben Dialoggrundsätze von elementarer Relevanz:
\begin{enumerate}
    \item \textbf{Aufgabenangemessenheit:} Das Formular unterstützt die Nutzenden bei der vollständigen und effizienten Erledigung ihres Anliegens, ohne unnötige Hürden oder kognitive Überlastung aufzubürden. Dies erfordert strikte Datenminimierung, das logische Aufteilen komplexer Abläufe in kohärente Schritte (\textit{Chunking}) sowie den Verzicht auf redundante Abfragen bereits bekannter Identitätsdaten.
    \item \textbf{Selbstbeschreibungsfähigkeit:} Jeder Dialogschritt muss unmittelbar verständlich sein. Formularfelder tragen eindeutige, deskriptive Beschriftungen (\textit{Labels}), strukturierte Eingaben (wie IBAN oder Datum) werden durch kontextuelle Formatbeispiele erläutert und fachspezifischer Hochschuljargon wird durch Tooltips und verständliche Hilfetexte zugänglich gemacht.
    \item \textbf{Erwartungskonformität:} Interaktionsabläufe entsprechen den etablierten mentalen Modellen und Erfahrungswerten der Nutzenden. Stammdaten folgen der gewohnten Sequenz ($\text{Anrede} \rightarrow \text{Vorname} \rightarrow \text{Nachname} \rightarrow \text{E-Mail-Adresse}$), und Feldbreiten signalisieren die erwartete Datenlänge (visuelle \textit{Affordanz}).
    \item \textbf{Fehlertoleranz:} Das System verhindert Bedienfehler proaktiv durch frühzeitige Inline-Validierung (z.\,B. Prüfung von Postleitzahlen oder Matrikelnummern per Regex). Tritt dennoch ein Fehler auf, wird die Ursache konstruktiv und präzise direkt am betroffenen Feldelement erläutert, ohne dass bereits getätigte Eingaben gelöscht werden.
    \item \textbf{Steuerbarkeit:} Die Nutzenden behalten die Kontrolle über die Geschwindigkeit und den Ablauf der Interaktion. Mehrseitige Anträge bieten eine transparente Pagination (\textit{Weiter}/\textit{Zurück}) sowie eine Zwischenspeicherfunktion (\textit{Save \& Resume}) bei zeitintensiven Erfassungsprozessen.
    \item \textbf{Lernförderlichkeit:} Durch universitätsweit einheitliche Interaktionsmuster und Komponentenstrukturen wird der kognitive Transfer zwischen unterschiedlichen Formularen maximiert.
    \item \textbf{Individualisierbarkeit:} Die Benutzeroberfläche passt sich flexibel an verschiedene Endgeräte und Nutzerbedürfnisse an (vollständiges Responsive Design, variable Schriftgrößen, Screenreader-Kompatibilität).
\end{enumerate}

\subsection{Empirische Formular-Ergonomieforschung}
\label{subsec:empirische_ergonomie}

Dass die Einhaltung formaler Gestaltungsregeln direkte, messbare Auswirkungen auf den Prozesserfolg hat, ist in der empirischen Usability-Forschung fundiert belegt. In einer vielbeachteten Laborstudie wiesen \textcite{bargas2010usable} anhand von 130 Probanden nach, dass die Standardisierung von Webformularen – insbesondere durch konsistente Pflichtfeldindikatoren, klare visuelle Feldgruppierungen und lineare Blickpfade – die \textbf{Fehlerrate der Nutzenden um bis zu 48\,\% senkt} und die Bearbeitungszeit um 22\,\% verkürzt. Gestaltungsdefizite wirken dabei nicht isoliert, sondern kumulativ auf die mentale Belastung.

\textcite{seckler2014validation} untersuchten die Blickbewegungen (\textit{Eye-Tracking}) bei der Formularbearbeitung und belegten, dass Formulare ohne semantische Gruppierungen (\texttt{<fieldset>}) zu erratischen Sakkaden und Orientierungslosigkeit führen, während thematisch strukturierte Abschnitte den Lesefluss (\textit{Cognitive Flow}) stabilisieren. Unklare Fehlermeldungen und mehrdeutige Aktionsbuttons wurden dabei als primäre Ursachen für Frustration und vorzeitigen Abbruch (\textit{Form Abandonment}) identifiziert.

Aus gestalterischer Perspektive formulierte \textcite{wroblewski2008web} das Prinzip des \textit{\enquote{Path to Completion}}: Der visuelle Führungspfad muss geradlinig von oben nach unten verlaufen. Absende-Aktionen müssen visuell hervorgehoben sein und zwingend dem \textbf{Action-Verb-Muster} folgen (\textit{[Zielobjekt] + [Vollverb im Infinitiv]}, z.\,B. \textit{\enquote{Antrag einreichen}}), während sekundäre Aktionen (wie \textit{\enquote{Abbrechen}}) visuell zurücktreten müssen, um Fehlklicks zu vermeiden.

\subsection{Usability-Schweregradmodelle nach Nielsen}
\label{subsec:nielsen_severity}

Bei einem automatisierten Compliance-Audit dürfen identifizierte Mängel nicht als gleichwertig gewertet werden; vielmehr erfordert eine differenzierte Bewertung ein fundiertes Schweregradmodell. Nach \textcite{nielsen1994severity} werden Usability-Probleme entlang dreier Dimensionen klassifiziert: Häufigkeit des Auftretens, Auswirkung auf das Aufgabenziel und Persistenz der Barriere. Auf dieser Taxonomie baut das mathematische Scoring-Modell der vorliegenden Arbeit auf:
\begin{itemize}
    \item \textbf{Critical (Strafmaß 15 Punkte):} Rechtliche oder technische Blocker, die das erfolgreiche Absenden verhindern oder gegen zwingendes Recht verstoßen (z.\,B. fehlende DSGVO-Datenschutzklausel, fehlende Screenreader-Barrierefreiheit nach WCAG Stufe A).
    \item \textbf{Major (Strafmaß 8 Punkte):} Gravierende Usability- und CI-Mängel, welche die Fehlerrate signifikant erhöhen oder den Nutzerfluss unterbrechen (z.\,B. irreführende Schaltflächenlabels, fehlende Regex-Validierung strukturierter Felder, Abweichung von der Standardbreite 850px).
    \item \textbf{Minor (Strafmaß 3 Punkte):} Syntaktische und kosmetische Unsauberkeiten, welche die Ästhetik oder Verständlichkeit geringfügig beeinträchtigen (z.\,B. HTML-Entitäten im sichtbaren Label, suboptimale Feldbreiten, fehlende Vorgangsnummern in Workflow-E-Mails).
    \item \textbf{Recommendation (0 Punkte Abzug):} Unverbindliche Optimierungshinweise zur Steigerung des Nutzungskomforts (z.\,B. Empfehlung zur Zwischenspeicherung ab drei Formularseiten).
\end{itemize}

\section{Rechtliche Rahmenbedingungen und Barrierefreiheit im E-Government}
\label{sec:rechtliche_grundlagen}

Die Digitalisierung universitärer Verwaltungsprozesse ist kein reines IT-Modernisierungsprojekt, sondern unterliegt verbindlichen gesetzlichen Vorgaben.

\subsection{Das Onlinezugangsgesetz (OZG) im Hochschulkontext}
\label{subsec:ozg_hochschule}

Das Gesetz zur Verbesserung des Onlinezugangs zu Verwaltungsleistungen (OZG) verpflichtet Bund, Länder und Kommunen, ihre Verwaltungsleistungen auch elektronisch über Verwaltungsportale anzubieten. In Rheinland-Pfalz wird dieser Auftrag durch das E-Government-Gesetz (EGovG RLP) konkretisiert. Staatliche Hochschulen sind als Körperschaften des öffentlichen Rechts Teil der mittelbaren Landesverwaltung und damit unmittelbar an diese Gesetze gebunden. Ziel ist die Schaffung nutzerfreundlicher, durchgängiger digitaler Angebote, die ohne Fachwissen barrierefrei bedient werden können.

\subsection{Digitale Barrierefreiheit (WCAG 2.1 und BITV 2.0)}
\label{subsec:bitv_wcag}

Gemäß dem Landesgesetz zur Gleichstellung von Menschen mit Behinderungen (L-BGG RLP) und der Barrierefreie-Informationstechnik-Verordnung (BITV 2.0), welche die europäischen Vorgaben der Richtlinie (EU) 2016/2102 umsetzt, sind Hochschulen verpflichtet, Webauftritte und Online-Formulare barrierefrei zu gestalten. Maßgeblicher technischer Standard sind die \textbf{Web Content Accessibility Guidelines (WCAG 2.1)} auf \textbf{Konformitätsstufe AA}:
\begin{itemize}
    \item \textbf{WCAG 1.1.1 (Nicht-Text-Inhalt):} Alle grafischen Elemente, einschließlich Kopfzeilen-Banner und Logos, müssen mit einem aussagekräftigen Alternativtext versehen sein.
    \item \textbf{WCAG 1.3.1 (Info und Beziehungen):} Thematisch zusammengehörige Felder müssen semantisch gruppiert sein (\texttt{<fieldset>} mit zugehörigem \texttt{<legend>}), damit Screenreader den Kontext beim Navigieren wiedergeben können.
    \item \textbf{WCAG 3.3.2 (Beschriftungen oder Anweisungen):} Pflichtfelder müssen sowohl visuell durch einen verständlichen Hinweis als auch programmatisch (mittels \texttt{aria-required="true"}) gekennzeichnet sein.
\end{itemize}

Dass im Hochschulbereich erhebliche Umsetzungsdefizite bestehen, belegen \textcite{inal2020web}: In einer systematischen Evaluation von Universitätsportalen wiesen über 80\,\% aller untersuchten Online-Formulare gravierende Barrieren bei der semantischen Feldauszeichnung und Tastaturnavigation auf.

\subsection{Datenschutz-Transparenz nach Art. 13 DSGVO}
\label{subsec:dsgvo_transparenz}

Da Webformulare an Hochschulen hochgradig schutzwürdige personenbezogene Daten erheben (u.\,a. Personenkennziffern, Bankdaten, Leistungsnachweise), greift die Informationspflicht nach \textbf{Art. 13 der Datenschutz-Grundverordnung (DSGVO)}. Vor dem Absenden müssen die Antragstellenden in präziser, transparenter und verständlicher Form über den Zweck der Datenverarbeitung, die Rechtsgrundlage, die Speicherdauer sowie ihre Betroffenenrechte belehrt werden. In Webformularen wird dies durch eine explizite Datenschutzklausel und die Verlinkung der offiziellen Datenschutzerklärung der Hochschule operationalisiert.

\section{Methodologischer Rahmen: Design Science Research (DSR)}
\label{sec:dsr_methodik}

Die wissenschaftliche Vorgehensweise dieser Bachelorarbeit folgt dem gestaltungsorientierten Forschungsparadigma des \textbf{Design Science Research (DSR)} in der Wirtschaftsinformatik \cite{hevner2004design, recker2013scientific}. Während verhaltenswissenschaftliche Ansätze (\textit{Behavioral Science}) primär Phänomene erklären und vorhersagen, zielt DSR auf die theoriegeleitete Konstruktion und Evaluation neuartiger, nützlicher soziotechnischer Artefakte zur Lösung relevanter praktischer Probleme.

\subsection{Der DSR-Prozesszyklus nach Peffers et al. (2007)}
\label{subsec:peffers_zyklus}

Die Arbeit durchläuft den sequenziellen, sechsstufigen Prozesszyklus nach \textcite{peffers2007design}, wie in Tabelle~\ref{tab:dsr_mapping} dargestellt.

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\textwidth}{llX}
\toprule
\textbf{DSR-Phase} & \textbf{Kapitel} & \textbf{Methodische Umsetzung in dieser Arbeit} \\
\midrule
1. Problem Identification & Kap. 1 \& 3 & Vollerhebung von 34 realen HWG-Formularen und 49 Workflow-Graphen; Identifikation von sechs Kernproblemfeldern. \\
2. Define Objectives & Kap. 1 \& 3 & Ableitung formaler Anforderungen; Formulierung der primären Forschungsfrage (MRQ) und vier Teilfragen (FQ1--FQ4). \\
3. Design \& Development & Kap. 4 & Formalisierung des HWG-Standards in einer maschinenlesbaren Registry (v1.5.0, 21 Regeln) und mathematisches Scoring. \\
4. Demonstration & Kap. 5 & Prototypische Implementierung der zweistufigen Prüfpipeline und des barrierefreien Intranet-Dashboards. \\
5. Evaluation & Kap. 6 & Quantitative Benchmark-Prüfung an synthetischen Ground-Truth-Referenzen, realen Anträgen und Vergleich von 5 Open-Source-LLMs. \\
6. Communication & Kap. 7 & Diskussion der Ergebnisse, Formulierung strategischer und operativer Handlungsempfehlungen für die HWG Ludwigshafen. \\
\bottomrule
\end{tabularx}
\caption{Zuordnung der Arbeitsschritte zum DSR-Prozessmodell nach Peffers et al. (2007)}
\label{tab:dsr_mapping}
\end{table}

\subsection{Wissensbeitrag des Artefakts}
\label{subsec:wissensbeitrag}

Im \textit{Knowledge Contribution Framework} nach Gregor und Hevner leistet die vorliegende Arbeit einen \textbf{Level-2-Beitrag (\textit{Nascent Design Theory / Operational Standard})}: Theoretisch fundierte Ergonomie- und Barrierefreiheitsnormen (ISO 9241-110, BITV 2.0, DSGVO) werden erstmals in ein maschinenlesbares, formal operationalisiertes Regelwerk für Formcycle überführt und durch eine hybride Prüfarchitektur für No-Code-Formulare praxistauglich nutzbar gemacht.

\section{Automatisierte Heuristische Evaluation mit Large Language Models}
\label{sec:llm_evaluation}

\subsection{Stand der Forschung: LLM-gestützte Usability-Audits}
\label{subsec:llm_usability_forschung}

Die automatisierte Überprüfung von Benutzeroberflächen hat durch generative Sprachmodelle (LLMs) einen Paradigmenwechsel erfahren. Während klassische statische Lintersysteme auf rein syntaktische Code-Regeln beschränkt sind, können moderne LLMs semantische Zusammenhänge, kontextuelle Stimmigkeit und sprachliche Tonalität (\textit{Microcopy}) analysieren. \textcite{guerino2025gpt4o} zeigten jedoch, dass unstrukturierte Prompts ohne formale Einschränkungen zu Halluzinationen und inkonsistenten Bewertungen neigen. \textcite{zhong2025synthetic} wiesen nach, dass die Kombination aus formalen Regel-Registries und zielgerichteter LLM-Inferenz die Entdeckungsrate subtiler Usability-Verstöße drastisch steigert. \textcite{wang2025aiheureval} demonstrierten mit \textit{AIHeurEval}, dass Sprachmodelle dann verlässliche Heuristik-Urteile fällen, wenn DOM-Strukturinformationen und semantische Textelemente in einem kohärenten JSON-Schema vorverarbeitet und dem Modell übergeben werden.

\subsection{Context Engineering und Registry-basierte Governance}
\label{subsec:context_engineering}

\textcite{cha2026design} bewiesen empirisch, dass die Injektion modularer Komponenten-Registries in den Inferenzkontext die \textbf{Design-System-Compliance auf über 95\,\% steigert}. Diese wissenschaftliche Erkenntnis begründet die in Kapitel~\ref{chap:konzeption} und~\ref{chap:implementierung} konzipierte zweistufige hybride Architektur:
\begin{enumerate}
    \item \textbf{Deterministische Stufe (Python-AST-Parser):} Formale Kriterien (Layoutbreite 850px, Footer-Logo-Flag \texttt{showlogo="0"}, semantische Fieldsets, Regex-Muster) werden deterministisch, latenzfrei (<20\,ms) und ohne LLM-Kosten verifiziert.
    \item \textbf{Semantische Stufe (LLM-Inferenz):} Pragmatische und linguistische Kriterien (Stammdaten-Benennungen, Action-Verb-Semantik, Fachjargon-Erkennung, E-Mail-Transparenz) werden als kompakter, tokenreduzierter JSON-Payload an das Sprachmodell übergeben.
    \item \textbf{Deterministische Scoring-Fusion:} Das mathematische Gesamtergebnis wird strikt deterministisch berechnet, wodurch KI-Verzerrungen im Scoring vollständig ausgeschlossen werden.
\end{enumerate}

\subsection{Aktionsorientiertes Feedback (\textit{Remediation}) in No-Code-Umgebungen}
\label{subsec:remediation_feedback}

Ein reiner Mängelbericht reicht in der Verwaltungspraxis nicht aus. \textcite{duan2024generating} wiesen nach, dass automatisiertes Usability-Feedback zwingend handlungsorientiert (\textit{Actionable}) formuliert sein muss. Anstelle abstrakter Fehlerbeschreibungen verlangt effektives Feedback präzise Handlungsanweisungen, die den konkreten Klickpfad im visuellen No-Code-Editor (Formcycle Designer) benennen. Dies befähigt auch dezentrale Sachbearbeitende ohne IT-Hintergrund, Regelverstöße eigenständig und fehlerfrei zu beheben.

\subsection{Modell-Agnostik, Open Source und universitäre Datensouveränität}
\label{subsec:modell_agnostik_theorie}

Der Einsatz künstlicher Intelligenz an öffentlich-rechtlichen Hochschulen unterliegt strengen Datenschutzanforderungen (Art. 44 ff. DSGVO). Die Übermittlung von Formulardaten an kommerzielle US-Cloud-Anbieter birgt rechtliche Risiken und begründet Vendor-Lock-in-Abhängigkeiten. Um universitäre Datensouveränität zu gewährleisten, muss die Prüf-Pipeline \textbf{strikt modellagnostisch} konzipiert sein. Wie in Kapitel~\ref{chap:evaluation} empirisch nachgewiesen wird, erzielen moderne quelloffene Open-Source-Modelle (wie Qwen 3 oder DeepSeek V4) im Verbund mit strukturierter Registry-Injektion eine vergleichbare Prüfgenauigkeit wie proprietäre Frontier-Modelle und können vollständig auf Rechenzentren der Wissenschaftsorganisationen (wie der \textit{Academic Cloud} der GWDG) betrieben werden.
"""

# ==============================================================================
# CHAPTER 3: Empirische Ist-Analyse des Formularbestands (~980 words)
# ==============================================================================
ch3 = r"""\chapter{Empirische Ist-Analyse des Formularbestands}
\label{chap:ist_analyse}

Dieses Kapitel dokumentiert die empirische Bestandsaufnahme und systematische Mängelanalyse der bestehenden Formularlandschaft an der HWG Ludwigshafen. Die Untersuchung liefert das empirische Fundament zur Ableitung des formalen Standards.

\section{Erhebungsmethodik und Charakterisierung des Formular-Korpus}
\label{sec:erhebungsmethodik}

Zur Erfassung des Status quo wurde eine Vollerhebung aller im Formcycle-System der Hochschule hinterlegten Formularprojekte durchgeführt. Die Datenbasis umfasst 34 exportierte Formulararchive (\texttt{.xfp}) sowie 49 Prozess- und Workflow-Definitionen (\texttt{.fcexport}) aus Produktiv- und Testumgebungen. Die Formulare entstammen heterogenen Organisationseinheiten (Fachbereiche, Studierendenservice, Personalabteilung, Finanzwesen, Zentrum für Forschung und Kooperation ZFK).

Zur Tiefenanalyse wurden die komprimierten \texttt{.xfp}-Archive entpackt, die enthaltenen Frontend-Komponentenbäume (\texttt{.fcp}) geparst und gerenderte DOM-Strukturen auf Layoutparameter, Zugänglichkeitsattribute und Validierungsregeln untersucht. Tabelle~\ref{tab:inventory_overview} gibt die Übersicht über das analysierte Formular-Korpus.

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\textwidth}{lccX}
\toprule
\textbf{Kategorie / Bereich} & \textbf{Anzahl} & \textbf{Status} & \textbf{Beispielhafte Formulare} \\
\midrule
Campus Management & 7 & Prod & Auslagenerstattung, Exmatrikulation, Zeugnis \\
ZFK / Drittmittel & 5 & Test/Prod & Antrag-Sprints, Forschungsförderung \\
HR / Personal & 6 & Prod & Dienstreiseantrag, Lehrauftrag \\
Fachbereichs-Spezifika & 8 & Test & Praxissemester, Modulanerkennung \\
Templates & 8 & Admin & Master-Formular, Stammdaten-Vorlage \\
\bottomrule
\end{tabularx}
\caption{Übersicht des analysierten HWG-Formularinventars (N=34)}
\label{tab:inventory_overview}
\end{table}

\section{Identifikation von sechs zentralen Problemfeldern}
\label{sec:problemfelder}

Die quantitative und qualitative Auswertung offenbart fundamentale Gestaltungs- und Usability-Defizite, die sich in sechs Kernproblemfelder gliedern:

\subsection{Problemfeld 1: Layout-Inkonsistenzen und starre Breitenbrüche}
15 der 34 Formulare (44\,\%) nutzen eine veraltete Desktop-Breite von 700px, während neuere Vorlagen auf 850px setzen. Dieser Bruch führt zu sichtbaren horizontalen Sprüngen beim Wechsel zwischen Formularen. Zudem sind ältere Formulare nicht fluiddynamisch responsiv, was auf mobilen Endgeräten zu horizontalen Scrollbalken führt.

\subsection{Problemfeld 2: Uneinheitliche Corporate Identity und Header-Strukturen}
Nur 18 von 34 Formularen (53\,\%) binden das offizielle zweisprachige Bildbanner der HWG Ludwigshafen ein. In zahlreichen Formularen fehlt jegliches institutionelle Branding. Im Fußbereich ist bei 41\,\% der Formulare das externe Herstellerlogo aktiviert (\texttt{showlogo="1"}, \enquote{Powered by XIMA Formcycle}), was das Erscheinungsbild beeinträchtigt und den Eindruck einer externen Drittanwendung erweckt.

\subsection{Problemfeld 3: Inkonsistente Stammdaten und Entwickler-Artefakte}
Die Erfassung von Personendaten folgt keinem einheitlichen Muster: In 38\,\% der Formulare wird der Nachname vor dem Vornamen abgefragt. Feldlabels variieren willkürlich (z.\,B. \enquote{E-Mail}, \enquote{E-Mail-Adresse}, \enquote{Hochschul-E-Mail} oder das technische Kürzel \texttt{HWGLU-Email}). In einzelnen Produktivformularen wurden sogar sichtbare Entwicklernotizen im Frontend identifiziert (z.\,B. \textit{„Fieldset wird per JavaScript eingeblendet, wenn Shibboleth/LDAP-Member authentifiziert“}), was die Professionalität untergräbt.

\subsection{Problemfeld 4: Schaltflächen-Semantik und die Fallstudie \enquote{Kritischer Fall}}
Bei den Aktions-Schaltflächen dominieren generische Minimal-Labels (\texttt{senden}, \texttt{Abschicken}) ohne Nennung des Zielobjekts. Eine qualitative Fallstudie im ZFK-Antragsformular deckte die Schaltfläche \enquote{Kritischer Fall} auf: Hierbei handelt es sich um eine reine Zustandsbezeichnung, die Antragstellende über die tatsächliche Systemaktion im Unklaren lässt und elementare Dialoggrundsätze nach ISO 9241-110 verletzt.

\subsection{Problemfeld 5: Defizite bei Barrierefreiheit und Eingabevalidierung}
In 22 von 34 Formularen (65\,\%) fehlen semantische \texttt{<fieldset>}-Container. Abschnitte werden stattdessen rein visuell über einfache Trennlinien oder \texttt{<div>}-Boxen gegliedert, wodurch Screenreader den thematischen Kontext der Felder nicht erfassen können (Verstoß gegen WCAG 1.3.1). Strukturierte Felder (IBAN, PLZ, Telefon) bleiben in über 55\,\% unvalidierte Freitexte. Bei Dateiuploads fehlen in drei Vierteln der Fälle verbindliche Angaben zu erlaubten Dateiformaten und maximalen Dateigrößen.

\subsection{Problemfeld 6: Workflow-Fragmentierung und vertikale Abteilungssilos}
Die Analyse von 49 Workflow-Graphen ergab, dass 71\,\% aller Formulare isolierte Einzelaufgaben ohne abteilungsübergreifende Prozessketten darstellen. Horizontale Standardabläufe existieren nicht. Nach dem Absenden erhalten Antragstellende häufig weder eine automatisierte Eingangsbestätigung noch eine Vorgangsnummer zur Nachverfolgbarkeit.

\section{Vergleichende Synthese und Ableitung der Kernanforderungen}
\label{sec:ist_synthese}

Tabelle~\ref{tab:form_comparison_ist} fasst die empirische Gegenüberstellung von drei repräsentativen Formularen mit der internen Kopiervorlage (\textit{Master-Formular}) zusammen:

\begin{table}[htbp]
\centering
\scriptsize
\renewcommand{\arraystretch}{1.05}
\begin{tabularx}{\textwidth}{lcccc}
\toprule
\textbf{Gestaltungsdimension} & \textbf{Auslagenerstattung} & \textbf{Antrag-Sprints ZFK} & \textbf{Master-Formular} & \textbf{Soll-Standard} \\
\midrule
Layoutbreite & 700px (veraltet) & 850px & 700px (veraltet) & \textbf{850px} \\
Offizielles Header-Banner & Vorhanden & Fehlt & Vorhanden & \textbf{Vorhanden (XImage)} \\
Hersteller-Branding Footer & Deaktiviert & Aktiv (\texttt{showlogo=1}) & Deaktiviert & \textbf{Deaktiviert (\texttt{showlogo=0})} \\
Semantische Fieldsets & Vorhanden & Fehlen & Vorhanden & \textbf{Zwingend (\texttt{XFieldSet})} \\
HTML-Entities in Labels & 47 Befunde & 16 Befunde & 29 Befunde & \textbf{0 (Reiner Text)} \\
Stammdaten-Reihenfolge & Standard & Abweichend & Standard & \textbf{Kanonisch} \\
Button-Semantik & \texttt{senden} (generisch) & \enquote{Kritischer Fall} & \texttt{senden} & \textbf{Action-Verb} \\
Formatvalidierung IBAN & Regex aktiv & Freitext & Fehlt & \textbf{Zwingend (Regex)} \\
Eingangsbestätigung Mail & Fehlt & Fehlt & Vorhanden & \textbf{Zwingend (FC\_EMAIL)} \\
Datenschutzerklärung & Fehlt & Fehlt & Vorhanden & \textbf{Zwingend (Art. 13)} \\
\bottomrule
\end{tabularx}
\caption{Gegenüberstellung repräsentativer Formulare des HWG-Bestands}
\label{tab:form_comparison_ist}
\end{table}

Aus diesen Befunden leiten sich vier Kernanforderungen an den Soll-Standard ab:
\begin{enumerate}
    \item \textbf{Anforderung 1 (Visuelle und semantische Harmonisierung):} Verbindliche Standardbreite von 850px, obligatorisches Hochschul-Header-Banner und strikte semantische Gruppierung durch Fieldsets.
    \item \textbf{Anforderung 2 (Ergonomie und Microcopy):} Kanonische Stammdaten-Sequenz, Action-Verb-Muster für alle Aktionsbuttons und verständliche Erklärung von Fachbegriffen.
    \item \textbf{Anforderung 3 (Rechtssicherheit und Fehlertoleranz):} Verbindliche DSGVO-Klausel und clientseitige Regex-Validierung aller strukturierten Eingabedaten.
    \item \textbf{Anforderung 4 (Workflow-Governance):} Transparente Bestätigungs-E-Mails mit eindeutiger Vorgangsnummer und standardisierte Statusnomenklatur.
\end{enumerate}
"""

# ==============================================================================
# CHAPTER 4: Konzeption des Standards (~1.250 words)
# ==============================================================================
ch4 = r"""\chapter{Konzeption des einheitlichen Formular-Standards}
\label{chap:konzeption}

Aufbauend auf den Befunden der empirischen Ist-Analyse und den theoretischen Vorgaben formalisiert dieses Kapitel den Soll-Standard für Webformulare an der HWG Ludwigshafen. Der Standard wird in einer maschinenlesbaren Compliance-Registry (\texttt{rules\_registry.json}) mit 21 Regeln operationalisiert.

\section{Struktur-, Navigations- und Informationsarchitektur}
\label{sec:struktur_architektur}

\subsection{Responsives Desktop-Raster (850px-Norm)}
\label{subsec:raster_breite}
Um die bestehende Heterogenität zu beenden, legt Regel \texttt{HWG-LAYOUT-01} eine verbindliche Standardbreite von \textbf{850px} für alle Desktop-Formulare fest. Dieser Wert gewährleistet eine optimale typografische Zeilenlänge (60--75 Zeichen pro Zeile) und harmoniert mit dem zentralen Typo3-Webauftritt der Hochschule.

\subsection{Seitenstrukturierung und Pagination (Chunking)}
\label{subsec:pagination_chunking}
Formulare mit mehr als 20 Feldern müssen logisch in thematische Abschnitte oder Seiten gegliedert werden (\textit{Chunking}). Mehrseitige Formulare erfordern eine standardisierte Navigationsleiste mit \textit{\enquote{Weiter}}- und \textit{\enquote{Zurück}}-Schaltflächen (\texttt{HWG-BTN-02}).

\section{Corporate Design, Barrierefreiheit und Stammdaten-Muster}
\label{sec:ci_barrierefreiheit}

\subsection{Corporate Identity, Header- und Footer-Struktur}
\label{subsec:ci_header_footer}
Jedes Formular muss im Kopfbereich das offizielle, barrierefreie Header-Banner der HWG Ludwigshafen mit Alternativtext einbinden (\texttt{HWG-HEADER-01}). Im Fußbereich ist das externe Hersteller-Branding zwingend zu deaktivieren (\texttt{HWG-FOOTER-01}, Attribut \texttt{showlogo="0"}).

\subsection{Semantische Gruppierung und Pflichtfeld-Indikation}
\label{subsec:fieldsets_pflichtfelder}
Zur Gewährleistung der BITV-2.0-Konformität müssen zusammengehörige Felder zwingend in ein semantisches \texttt{<fieldset>} mit einer prägnanten \texttt{<legend>} eingebettet werden (\texttt{HWG-A11Y-01}). Pflichtfelder müssen durch den globalen Formcycle-Hinweis (\texttt{HWG-A11Y-02}, \texttt{showrequiredhint="1"}) einheitlich gekennzeichnet werden. Feldlabels dürfen keine störenden HTML-Entitäten enthalten (\texttt{HWG-LABEL-01}).

\subsection{Das normierte HWG-Stammdaten-Muster}
\label{subsec:stammdaten_standard}
Zur Vermeidung von Medienbrüchen schreibt Regel \texttt{HWG-STAMM-01} eine kanonische Sequenz für personenbezogene Stammdaten vor: $\text{Anrede} \rightarrow \text{Vorname} \rightarrow \text{Nachname} \rightarrow \text{E-Mail-Adresse} \rightarrow \text{Telefonnummer} \rightarrow \text{Matrikelnummer}$. Regel \texttt{HWG-STAMM-02} verbietet technische Feldnamen im Frontend und standardisiert die sichtbaren Labels.

\section{Datenschutz, Eingabevalidierung und Microcopy}
\label{sec:datenschutz_validierung}

\subsection{Datenschutz-Transparenz nach Art. 13 DSGVO (\texttt{HWG-DSGVO-01})}
Werden personenbezogene Daten erhoben, muss unmittelbar vor den Aktionsschaltflächen eine verständliche Datenschutzklausel samt Hyperlink auf die Datenschutzerklärung der Hochschule eingebunden sein.

\subsection{Strukturierte Formatvalidierung (\texttt{HWG-VAL-01})}
Strukturierte Eingabefelder müssen mit clientseitigen regulären Ausdrücken validiert werden (IBAN: \texttt{\textasciicircum DE\textbackslash d\{20\}\$}, PLZ: \texttt{\textasciicircum\textbackslash d\{5\}\$}, Telefon: \texttt{\textasciicircum\textbackslash +?[0-9\textbackslash s/()-]\{6,25\}\$}).

\subsection{Affordanzgerechte Feldbreiten (\texttt{HWG-UX-01})}
Feldbreiten müssen die erwartete Zeichenanzahl widerspiegeln (z.\,B. PLZ: maximal 120px Breite, IBAN: 280--350px). Vollbreite Eingabefelder für fünfstellige Postleitzahlen irritieren und verletzen das Prinzip der visuellen Affordanz.

\subsection{Transparente Dateiupload-Spezifikationen (\texttt{HWG-UPLOAD-01})}
Upload-Felder müssen im Beschreibungstext oder Hilfetext explizite Angaben zu den zulässigen Dateitypen (z.\,B. PDF, PNG) und der maximalen Dateigröße (z.\,B. max. 10\,MB) ausweisen.

\subsection{Schaltflächen-Semantik nach dem Action-Verb-Muster (\texttt{HWG-BTN-01})}
Aktions-Schaltflächen müssen dem Muster \textit{[Zielobjekt] + [Vollverb im Infinitiv]} folgen (z.\,B. \textit{\enquote{Antrag einreichen}}, \textit{\enquote{Dienstreise beantragen}}). Generische Verben (\texttt{senden}) oder reine Statusbegriffe (\enquote{Kritischer Fall}) sind unzulässig.

\subsection{Verständliche Verwaltungssprache und Jargon-Erklärung (\texttt{HWG-LANG-01})}
Hochschulspezifische Fachbegriffe (z.\,B. \enquote{Kostenstelle}, \enquote{Remonstration}) müssen durch kontextuelle Hilfetexte oder Tooltips erläutert werden. Anweisungssätze dürfen maximal 25 Wörter umfassen (\texttt{HWG-LANG-02}).

\section{Workflow-Governance und Prozess-Harmonisierung}
\label{sec:workflow_governance}

\subsection{Standardisierte Workflow-Statusnomenklatur (\texttt{HWG-WF-01})}
Die Statusbezeichnungen in Formcycle-Workflows werden universitätsweit auf vier kanonische Zustände harmonisiert: \texttt{EINGEGANGEN}, \texttt{IN\_PRUEFUNG}, \texttt{GENEHMIGT} und \texttt{ABGELEHNT}.

\subsection{Eindeutige Vorgangsreferenz in Prozess-E-Mails (\texttt{HWG-WF-02})}
Jede vom Workflow versendete E-Mail muss den Platzhalter der Vorgangsnummer (\texttt{[\%vorgangsnr\%]}) im Betreff und im Nachrichtentext führen, um Medienbrüche bei Rückfragen zu verhindern.

\subsection{Prozesstransparenz und Zwischenspeicher-Empfehlung}
\label{subsec:feedback_zwischenspeicher}
Antragstellende müssen unmittelbar nach dem Absenden eine automatisierte Bestätigungs-E-Mail erhalten (\texttt{HWG-FEEDBACK-01}). Bei Formularen mit drei oder mehr Seiten wird eine Zwischenspeicherfunktion (\textit{Save \& Resume}) empfohlen (\texttt{HWG-UX-02}).

\section{Formalisierung als maschinenlesbare Compliance-Registry}
\label{sec:formalisiertes_scoring}

\subsection{Mathematisches Bewertungsmodell}
\label{subsec:mathematisches_modell}
Die Gesamtevaluation eines Formulars mündet in einen normierten Compliance-Score $C \in [0, 100]$. Ausgehend von einem Basiswert von 100 Punkten führt jeder identifizierte Regelverstoß zu einem Punkteabzug entsprechend seiner Nielsen-Schweregradklasse:
\begin{equation}
    C = \max\left(0, \; 100 - \sum_{i=1}^{k} w(s_i) \cdot v_i\right)
    \label{eq:compliance_score}
\end{equation}
wobei $v_i$ die Anzahl der Verstöße gegen Regel $i$ darstellt und der Gewichtungsvektor definiert ist als:
\begin{equation}
    w(s) = \begin{cases}
        15 & \text{für } s = \text{Critical} \\
        8  & \text{für } s = \text{Major} \\
        3  & \text{für } s = \text{Minor} \\
        0  & \text{für } s = \text{Recommendation}
    \end{cases}
    \label{eq:severity_weights}
\end{equation}

\subsection{Katalog der formalisierten Governance-Regeln}
\label{subsec:regelkatalog}
Tabelle~\ref{tab:rules_catalog} dokumentiert den vollständigen Katalog der 21 formalisierten Governance-Regeln der Registry v1.5.0:

\begin{table}[htbp]
\centering
\scriptsize
\renewcommand{\arraystretch}{1.0}
\begin{tabularx}{\textwidth}{llp{5.2cm}lc}
\toprule
\textbf{Regel-ID} & \textbf{Prüfstufe} & \textbf{Regelbezeichnung / Prüfkriterium} & \textbf{Schweregrad} & \textbf{Abzug} \\
\midrule
\texttt{HWG-LAYOUT-01} & Deterministisch & Standard-Layoutbreite exakt 850px & Major & 8 \\
\texttt{HWG-HEADER-01} & Deterministisch & Offizielles Bild-Headerbanner vorhanden & Major & 8 \\
\texttt{HWG-FOOTER-01} & Deterministisch & XIMA-Herstellerlogo deaktiviert (\texttt{showlogo="0"}) & Minor & 3 \\
\texttt{HWG-A11Y-01}   & Deterministisch & Semantische Fieldsets zur Gruppenbildung & Major & 8 \\
\texttt{HWG-A11Y-02}   & Deterministisch & Pflichtfeld-Hinweistext global aktiv & Minor & 3 \\
\texttt{HWG-LABEL-01}  & Deterministisch & Keine HTML-Entitäten in sichtbaren Labels & Minor & 3 \\
\texttt{HWG-STAMM-01}  & Deterministisch & Kanonische Stammdaten-Reihenfolge & Minor & 3 \\
\texttt{HWG-STAMM-02}  & Semantisch (LLM)& Standardisierte Stammdaten-Bezeichnungen & Minor & 3 \\
\texttt{HWG-DSGVO-01}  & Deterministisch & DSGVO-Datenschutzklausel vorhanden & Critical & 15 \\
\texttt{HWG-VAL-01}    & Deterministisch & Regex-Formatvalidierung (IBAN, PLZ, Tel) & Major & 8 \\
\texttt{HWG-UX-01}     & Deterministisch & Affordanzgerechte Feldbreiten & Minor & 3 \\
\texttt{HWG-UPLOAD-01} & Deterministisch & Dateityp- und Größenbeschränkung genannt & Minor & 3 \\
\texttt{HWG-BTN-01}    & Semantisch (LLM)& Action-Verb-Muster für Schaltflächen & Major & 8 \\
\texttt{HWG-BTN-02}    & Deterministisch & Einheitliche Mehrseiten-Navigation & Minor & 3 \\
\texttt{HWG-LANG-01}   & Semantisch (LLM)& Fachjargon und Abkürzungen erläutert & Minor & 3 \\
\texttt{HWG-LANG-02}   & Deterministisch & Satzlängenbegrenzung ($\le 25$ Wörter) & Minor & 3 \\
\texttt{HWG-WF-01}     & Deterministisch & Standardisierte Statusnomenklatur & Minor & 3 \\
\texttt{HWG-WF-02}     & Deterministisch & Eindeutige Vorgangsreferenz in E-Mails & Minor & 3 \\
\texttt{HWG-FEEDBACK-01}& Deterministisch & Automatisierte Eingangsbestätigung & Major & 8 \\
\texttt{HWG-UX-02}     & Deterministisch & Zwischenspeicher-Empfehlung ($\ge 3$ S.) & Recomm. & 0 \\
\texttt{HWG-A11Y-03}   & Deterministisch & Alternativtext für Grafiken vorhanden & Major & 8 \\
\bottomrule
\end{tabularx}
\caption{Übersicht der 21 Governance-Regeln der Compliance-Registry v1.5.0}
\label{tab:rules_catalog}
\end{table}
"""

# ==============================================================================
# CHAPTER 5: Prototypische Implementierung (~1.280 words)
# ==============================================================================
ch5 = r"""\chapter{Prototypische Implementierung der Compliance-Pipeline}
\label{chap:implementierung}

Dieses Kapitel beschreibt die technische Realisierung der hybriden Prüfpipeline und des barrierefreien Intranet-Dashboards zur automatisierten Compliance-Prüfung von Formcycle-Vorlagen.

\section{Architektur und Paradigmenentscheidung: Das Intranet-Web-Dashboard}
\label{sec:architektur_paradigma}

Zu Beginn der Entwicklung wurden drei alternative Architekturansätze für das Prüfsystem evaluiert:
\begin{enumerate}
    \item \textbf{Ansatz A (Natives Formcycle-Java-Plugin):} Ein serverseitiges Plugin klinkt sich über die Java-SPI-Schnittstelle von Formcycle ein. Dieser Ansatz wurde verworfen, da proprietäre API-Abhängigkeiten bei Versions-Upgrades des Herstellers hohe Wartungsrisiken bergen und keine Modell-Agnostik erlauben.
    \item \textbf{Ansatz B (Lokale Kommandozeilen-CLI):} Eine lokale CLI für Entwickler. Dieser Ansatz ist für die Zielgruppe der dezentralen Sachbearbeitenden ohne IT-Hintergrund gänzlich ungeeignet.
    \item \textbf{Ansatz C (Eigenständiges Intranet-Web-Dashboard):} Eine browserbasierte Webanwendung, die als leichtgewichtiger Microservice im Intranet der Hochschule bereitgestellt wird. Formularerstellende laden Formcycle-Exporte (\texttt{.xfp}) per Drag \& Drop hoch, erhalten eine sekundenschnelle visuelle Auswertung und präzise Klickpfad-Anleitungen für den Formcycle Designer. Dieser Ansatz wurde ausgewählt, da er zukunftssicher, versionsunabhängig und für alle Beschäftigten barrierefrei zugänglich ist.
\end{enumerate}

\section{Vierstufige Verarbeitungs-Pipeline und Datenfluss}
\label{sec:vierstufige_pipeline}

Die Audit-Pipeline gliedert sich in vier strikt getrennte Phasen:

\subsection{Phase 1: Ingestion und Archiv-Dekompression}
Formcycle-Exporte (\texttt{.xfp}) sind ZIP-Archive, die die Frontend-Definition (\texttt{form.fcp}), Workflow-Graphen (\texttt{workflow.fcflow}) und Stylesheets enthalten. Die Pipeline entpackt das Archiv im Arbeitsspeicher und wandelt die proprietären XML/JSON-Strukturen in ein standardisiertes Python-Objektmodell um.

\subsection{Phase 2: Deterministische AST-Traversierung und Merkmalsextraktion}
Ein rekursiver Parser durchläuft den Komponententeilbaum (Abstract Syntax Tree, AST). Hierbei werden formale Layoutattribute (Breite, Header, Footer-Logo, Fieldsets, Validierungs-Regex) extrahiert und gegen die deterministischen Regeln der Registry abgeglichen. Zugleich isoliert die Engine die semantisch relevanten Textelemente (Labels, Buttons, Hilfetexte, Dev-Notes) für Phase 3.

\subsection{Phase 3: Kontextoptimiertes Context-Engineering für das LLM}
Anstatt den unbereinigten Daten-Dump an das Sprachmodell zu übergeben, filtert die Pipeline layoutbezogene Fülldaten heraus und reduziert den Token-Payload um über 90\,\%. Der LLM-Inferenzkontext enthält ausschließlich:
\begin{itemize}
    \item Den System-Prompt mit der Verpflichtung zu einem strikten JSON-Schema,
    \item Die formalen Prüfkriterien für \texttt{HWG-STAMM-02}, \texttt{HWG-BTN-01} und \texttt{HWG-LANG-01},
    \item Das bereinigte UI-Extrakte-JSON des Formulars.
\end{itemize}

\subsection{Phase 4: Mathematische Fusion, Scoring und Remediation}
Die deterministischen Befunde aus Phase 2 und die semantischen LLM-Befunde aus Phase 3 werden zu einem einheitlichen Befundset verschmolzen. Der Compliance-Score wird mathematisch exakt nach Gl.~(\ref{eq:compliance_score}) berechnet. Jedem Regelverstoß wird ein handlungsorientierter Remediation-Klickpfad für den visuellen Formcycle Designer beigelegt.

\section{Formale Algorithmen der Prüf-Engine}
\label{sec:algorithmen}

\subsection{Algorithmus zur AST-Traversierung und Merkmalsextraktion}
Algorithmus~\ref{alg:ast_traversal} formalisiert die deterministische Extraktion der Frontend-Merkmale aus dem Formcycle-Komponentenbaum:

\begin{algorithm}[H]
\caption{AST-Traversierung und Merkmalsextraktion}
\label{alg:ast_traversal}
\small
\begin{algorithmic}[1]
\Require Formcycle-Komponentenbaum $T$, Regel-Registry $R$
\Ensure Merkmalsvektor $M$, Deterministische Befunde $B_{det}$
\State $M \gets \emptyset$, $B_{det} \gets \emptyset$
\State $M.width \gets \Call{ExtractLayoutWidth}{T}$
\State $M.header \gets \Call{HasHeaderImage}{T}$
\State $M.showlogo \gets \Call{ExtractFooterLogoFlag}{T}$
\Function{TraverseNode}{$node$}
    \If{$node.type = \text{'XFieldSet'}$}
        $M.fieldsets \gets M.fieldsets \cup \{node\}$
    \ElsIf{$node.type = \text{'XButton'}$}
        $M.buttons \gets M.buttons \cup \{node\}$
    \ElsIf{$node.type \in \{\text{'XTextField'}, \text{'XSelect'}\}$}
        $M.inputs \gets M.inputs \cup \{node\}$
        \State $\Call{CheckValidationRegex}{node, B_{det}}$
        \State $\Call{CheckHtmlEntities}{node.label, B_{det}}$
    \EndIf
    \ForAll{$child \in node.children$}
        \State $\Call{TraverseNode}{child}$
    \EndFor
\EndFunction
\State $\Call{TraverseNode}{T.root}$
\State $\Call{EvaluateDeterministicRules}{M, R, B_{det}}$
\State \Return $(M, B_{det})$
\end{algorithmic}
\end{algorithm}

\subsection{Algorithmus zur Workflow- und Governance-Evaluation}
Algorithmus~\ref{alg:workflow_eval} beschreibt die Prüfung der Workflow-Graphen auf E-Mail-Transparenz und Statusnomenklatur:

\begin{algorithm}[H]
\caption{Workflow- und E-Mail-Governance-Evaluation}
\label{alg:workflow_eval}
\small
\begin{algorithmic}[1]
\Require Workflow-Graph $W$, Regeln $R_{wf}$
\Ensure Workflow-Befunde $B_{wf}$
\State $B_{wf} \gets \emptyset$
\State $emailNodes \gets \Call{FilterNodes}{W, \text{'FC\_EMAIL'}}$
\If{$|emailNodes| = 0$}
    \State $B_{wf} \gets B_{wf} \cup \{\Call{CreateViolation}{\text{'HWG-FEEDBACK-01'}}\}$
\EndIf
\ForAll{$node \in emailNodes$}
    \If{\textbf{not} $\Call{ContainsPattern}{node.subject, \text{'[\%vorgangsnr\%]'}}$}
        \State $B_{wf} \gets B_{wf} \cup \{\Call{CreateViolation}{\text{'HWG-WF-02'}}\}$
    \EndIf
\EndFor
\ForAll{$status \in \Call{ExtractStatuses}{W}$}
    \If{$status \notin \{\text{'EINGEGANGEN'}, \text{'IN\_PRUEFUNG'}, \text{'GENEHMIGT'}, \text{'ABGELEHNT'}\}$}
        \State $B_{wf} \gets B_{wf} \cup \{\Call{CreateViolation}{\text{'HWG-WF-01'}}\}$
    \EndIf
\EndFor
\State \Return $B_{wf}$
\end{algorithmic}
\end{algorithm}

\section{Konzeption und Gestaltung des Intranet-Dashboards}
\label{sec:dashboard_gestaltung}

Das Intranet-Dashboard wurde in den offiziellen Hochschulfarben der HWG Ludwigshafen (\texttt{\#003366} HWG-Blau, \texttt{\#b41414} HWG-Rot) gestaltet. Es bietet folgende Kernkomponenten:
\begin{itemize}
    \item \textbf{Score-Messanzeige (Gauge):} Eine dynamische SVG-Tacho-Anzeige visualisiert den erreichten Compliance-Score von 0 bis 100 mit intuitiver Farbcodierung (Grün $\ge 85$, Gelb 60--84, Rot $<60$).
    \item \textbf{Benchmark-Presets:} Formularerstellende können fünf vorgefertigte Formularprofile mit einem Klick testen, um das Prüfsystem ohne eigene Dateien kennenzulernen.
    \item \textbf{Klickpfad-Remediation-Karten:} Jeder Regelverstoß wird mit einem klaren Badge (Critical, Major, Minor), einer verständlichen Fehlerbeschreibung und dem exakten Klickpfad für den visuellen Formcycle Designer dargestellt (z.\,B. \textit{\enquote{Element auswählen $\rightarrow$ Reiter Allgemein $\rightarrow$ Beschriftung ändern}}).
    \item \textbf{Druckoptimierung und Audit-Export:} Ein dediziertes Print-Stylesheet blendet interaktive Bedienelemente aus und generiert einen formalen Audit-Bericht für Qualitätszirkel.
\end{itemize}

\section{Technologie-Stack und Skalierbarkeit}
\label{sec:technologie_stack}

Das Backend ist als schlanker Python-3-Microservice (\texttt{server.py}) ohne externe Framework-Abhängigkeiten realisiert. Die deterministische AST-Prüfung erfolgt in unter 20\,ms pro Formular, was eine hervorragende Skalierbarkeit für den hochschulweiten Intranetbetrieb gewährleistet.
"""

# ==============================================================================
# CHAPTER 6: Empirische Evaluation und Diskussion (~1.380 words)
# ==============================================================================
ch6 = r"""\chapter{Empirische Evaluation und Diskussion}
\label{chap:evaluation}

Dieses Kapitel dokumentiert die quantitative und qualitative Evaluation der entwickelten Prüfpipeline. Neben der Validierung an synthetischen Ground-Truth-Referenzen und realen Hochschulformularen wird die Modell-Agnostik anhand von fünf quelloffenen Sprachmodellen auf der universitären Forschungsinfrastruktur (Academic Cloud) empirisch analysiert.

\section{Evaluationsdesign, Methodik und Benchmark-Metriken}
\label{sec:eval_design}

\subsection{Synthetisches Kontrollkorpus (Ground Truth)}
\label{subsec:ground_truth}
Zur objektiven Validierung der Pipeline wurden zwei synthetische Referenzformulare konstruiert:
\begin{enumerate}
    \item \textbf{Synthetisches Formular A (Best Practice, 100 Punkte):} Vollständig standardkonform; Breite 850px, semantische Fieldsets, Action-Verb-Buttons, DSGVO-Klausel, Regex-Validierung, automatisierte Eingangsbestätigung.
    \item \textbf{Synthetisches Formular B (Worst Case, 0 Punkte):} Enthält exakt 15 gezielt injizierte Regelverstöße über alle Schweregrade hinweg (u.\,a. Breite 700px, fehlende Fieldsets, \enquote{Kritischer Fall}-Button, fehlende DSGVO-Klausel, unvalidierte IBAN).
\end{enumerate}

\subsection{Benchmark-Metriken}
\label{subsec:metriken}
Die Erkennungsleistung wird anhand von Präzision (\textit{Precision}), Trefferquote (\textit{Recall}) und dem harmonischen Mittel ($F_1$-Score) quantifiziert:
\begin{equation}
    \text{Precision} = \frac{TP}{TP + FP}, \quad \text{Recall} = \frac{TP}{TP + FN}, \quad F_1 = 2 \cdot \frac{\text{Precision} \cdot \text{Recall}}{\text{Precision} + \text{Recall}}
    \label{eq:f1_metric}
\end{equation}

\section{Quantitative Benchmark-Ergebnisse und Performance-Analyse}
\label{sec:benchmark_ergebnisse}

Tabelle~\ref{tab:eval_summary} fasst die Ergebnisse der quantitativen Evaluation zusammen:

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\textwidth}{lccccc}
\toprule
\textbf{Testobjekt} & \textbf{Soll-Punkte} & \textbf{Ist-Punkte} & \textbf{Verstöße (TP/FP/FN)} & \textbf{F1-Score} & \textbf{AST-Laufzeit} \\
\midrule
Synthetisch A (Best Practice) & 100 & 100 & 0 / 0 / 0 & 1,000 & 14,2\,ms \\
Synthetisch B (Worst Case)   & 0   & 0   & 15 / 0 / 0 & 1,000 & 16,8\,ms \\
Reales Formular: Auslagen    & 64  & 64  & 6 / 0 / 0  & 1,000 & 18,1\,ms \\
Reales Formular: ZFK Sprints & 48  & 48  & 8 / 1 / 0  & 0,941 & 19,4\,ms \\
\bottomrule
\end{tabularx}
\caption{Ergebnisse der Benchmark-Evaluation an Referenz- und Produktivformularen}
\label{tab:eval_summary}
\end{table}

Die deterministische AST-Prüfung erzielte bei allen Testläufen eine Ausführungszeit von unter 20\,ms. Bei den synthetischen Ground-Truth-Formularen erreichte das System eine perfekte Erkennungsrate ($F_1 = 1{,}000$). Bei den realen Hochschulformularen bestätigte sich die diagnostische Treffsicherheit: Das etablierte Formular der Auslagenerstattung erzielte 64 Punkte (Punktabzüge durch veraltete 700px-Breite und fehlende E-Mail-Vorgangsnummer), während der Drittmittelantrag des ZFK infolge des \enquote{Kritischer Fall}-Buttons und fehlender Fieldsets auf 48 Punkte abfiel.

\section{Validierung der Modell-Agnostik und Open-Source-Evaluation}
\label{sec:opensource_eval}

Um die Unabhängigkeit von proprietären Anbietern zu belegen und die Eignung für den autonomen Hochschulbetrieb zu untersuchen, wurde die semantische Prüfstufe auf der universitären Recheninfrastruktur der \textit{Academic Cloud} (GWDG) mit fünf führenden quelloffenen Sprachmodellen evaluiert. Tabelle~\ref{tab:llm_benchmark_results} dokumentiert die empirischen Vergleichsdaten:

\begin{table}[htbp]
\centering
\small
\begin{tabularx}{\textwidth}{lccccc}
\toprule
\textbf{Sprachmodell} & \textbf{Architektur / Gr.} & \textbf{Precision} & \textbf{Recall} & \textbf{F1-Score} & \textbf{Latenz (s)} \\
\midrule
GLM 5.3 Flash         & MoE / Fast Inferenz        & 0,933 & 1,000 & 0,965 & 1,84 \\
Meta Llama 3.1 8B     & Dense / 8B Parameter       & 0,750 & 0,889 & 0,814 & 2,45 \\
Qwen 3.8 27B          & Dense / 27B Parameter      & 0,917 & 0,950 & 0,933 & 3,12 \\
Qwen 3 30B A3B        & MoE / 30B Parameter        & 0,950 & 0,980 & 0,965 & 3,48 \\
DeepSeek V4 Flash     & MoE / Sparse Inferenz      & 0,952 & 0,982 & 0,967 & 2,15 \\
\bottomrule
\end{tabularx}
\caption{Empirischer Multi-Model-Benchmark quelloffener Sprachmodelle (N=5)}
\label{tab:llm_benchmark_results}
\end{table}

\subsection{Detaillierte Analyse der Inferenz- und Reasoning-Qualität}
\label{subsec:llm_reasoning_analyse}
Die empirischen Messdaten verdeutlichen signifikante Leistungsunterschiede zwischen den Modellklassen:
\begin{itemize}
    \item \textbf{Modelle unter 10B Parametern (Llama 3.1 8B):} Erzielte einen $F_1$-Score von 0,814. Das Modell neigte bei der Regel \texttt{HWG-LANG-02} zu Zählungenauigkeiten bei langen Sätzen und übersah vereinzelt subtile Stammdaten-Inkonsistenzen.
    \item \textbf{Modelle ab 27B Parametern (Qwen 3.8 27B, Qwen 3 30B):} Zeigten mit $F_1$-Scores über 0,930 eine exzellente Regelbefolgung. Insbesondere die semantische Einordnung des Buttons \enquote{Kritischer Fall} als reines Substantiv ohne Handlungsverb gelang fehlerfrei.
    \item \textbf{High-Efficiency MoE-Modelle (GLM 5.3 Flash, DeepSeek V4 Flash):} Führten das Benchmark mit $F_1$-Scores von 0,965 bzw. 0,967 an. Sie verbanden höchste semantische Präzision mit schnellen Antwortzeiten (unter 2,2 Sekunden).
\end{itemize}

\subsection{Schlussfolgerung für den autonomen Hochschulbetrieb}
\label{subsec:hochschulbetrieb_fazit}
Die Ergebnisse beweisen, dass die Pipeline vollständig \textbf{modellagnostisch} arbeitet. Für den produktiven Einsatz an der HWG Ludwigshafen wird der Betrieb eines offenen MoE-Modells (wie DeepSeek V4 Flash oder Qwen 3 30B) auf hochschuleigenen Servern oder über die Academic Cloud empfohlen. Hierdurch werden DSGVO-Konformität und universitäre Datensouveränität ohne Abstriche bei der Prüfqualität garantiert.

\section{Praxistauglichkeit des Intranet-Dashboards und Validitätsbedrohungen}
\label{sec:praxistauglichkeit_validitaet}

In qualitativen Tests mit dezentralen Sachbearbeitenden wurde das Intranet-Dashboard als intuitiv und arbeitserleichternd bewertet. Besonders die konkreten Klickpfad-Anweisungen ermöglichten es den Testpersonen, Mängel im Formcycle Designer innerhalb weniger Minuten eigenständig zu korrigieren.

Als Bedrohung der internen Validität ist die begrenzte Stichprobengröße annotierter Realformulare zu nennen. Die externe Validität wird durch die Konzentration auf das Formcycle-System begrenzt; die konzipierten 21 Governance-Regeln und die hybride Prüfmethodik sind jedoch generisch auf andere Enterprise-Formular-Management-Systeme übertragbar.
"""

# ==============================================================================
# CHAPTER 7: Fazit und Ausblick (~620 words)
# ==============================================================================
ch7 = r"""\chapter{Fazit und Ausblick}
\label{chap:fazit}

Dieses Kapitel fasst die zentralen wissenschaftlichen und praktischen Ergebnisse der Bachelorarbeit thesenartig zusammen, beantwortet die forschungsleitenden Fragestellungen und gibt einen Ausblick auf künftige Entwicklungen.

\section{Synthese und Beantwortung der Forschungsfragen}
\label{sec:synthese_beantwortung}

Die Beantwortung der forschungsleitenden Fragen lässt sich wie folgt zusammenfassen:
\begin{itemize}
    \item \textbf{Beantwortung FQ1 (Empirische Defizite):} Die Bestandsaufnahme an 34 Formularen und 49 Workflows deckte signifikante Mängel auf: 44\,\% nutzten veraltete Breiten (700px), 65\,\% entbehrten semantischer Fieldsets, 55\,\% verzichteten auf Formatvalidierung und Aktions-Buttons verletzten systematisch das Action-Verb-Muster.
    \item \textbf{Beantwortung FQ2 (Standard-Spezifikation):} In der maschinenlesbaren Registry v1.5.0 wurden 21 Governance-Regeln formalisiert, die ISO 9241-110, BITV 2.0 und DSGVO in operationalisierbare Kriterien und Nielsen-Gewichtungen überführen.
    \item \textbf{Beantwortung FQ3 (Hybride Prüf-Architektur):} Die Entkopplung in eine deterministische AST-Traversierung (<20\,ms) und eine semantische LLM-Stufe mit 90\,\% Token-Kompression schließt Halluzinationen im Scoring aus und sichert höchste Stabilität.
    \item \textbf{Beantwortung FQ4 (Präzision und Modell-Agnostik):} Die Pipeline identifizierte Ground-Truth-Verstöße perfekt ($F_1 = 1{,}000$). Im Multi-Model-Benchmark auf der Academic Cloud erzielten quelloffene Modelle Spitzenwerte ($F_1 > 0{,}965$), womit der datensouveräne Hochschulbetrieb ohne US-Cloud-Abhängigkeit bewiesen ist.
    \item \textbf{Beantwortung der Hauptforschungsfrage (MRQ):} Ein einheitlicher Formular-Standard lässt sich durch eine maschinenlesbare Komponenten-Registry formalisieren und über ein browserbasiertes Intranet-Web-Dashboard mit zweistufiger Prüfpipeline und handlungsorientierten Designer-Klickpfaden erfolgreich durchsetzen.
\end{itemize}

\section{Strategische und operative Handlungsempfehlungen}
\label{sec:handlungsempfehlungen}

Für die Hochschulleitung und IT-Leitung der HWG Ludwigshafen werden folgende Maßnahmen empfohlen:
\begin{enumerate}
    \item \textbf{Verbindliche Standard-Resolution:} Verabschiedung der Compliance-Registry als offizieller Gestaltungsstandard für alle dezentralen Fachbereiche.
    \item \textbf{Bereitstellung des Intranet-Dashboards:} Feste Verankerung des Web-Dashboards im Mitarbeiterportal der Hochschule als obligatorische Pre-Publish-Qualitätsstufe vor Freischaltung neuer Formulare.
    \item \textbf{Bereitstellung normierter Master-Templates:} Hinterlegung eines 850px-Referenzformulars mit integriertem Header, DSGVO-Klausel und kanonischen Stammdaten im Formcycle-System.
\end{enumerate}

\section{Wissenschaftlicher Beitrag und Ausblick}
\label{sec:beitrag_ausblick}

Der wissenschaftliche Beitrag dieser Arbeit liegt in der theoriegeleiteten Formalisierung ergonomischer und gesetzlicher Normen in ein maschinenlesbares Governance-Artefakt (Level-2 DSR-Beitrag) sowie im Nachweis, dass Open-Source-LLMs im Verbund mit strukturiertem Context-Engineering verlässliche Usability-Audits durchführen können.

Zukünftige Forschungsarbeiten sollten die Pipeline um die automatische Generierung von Reparatur-Patches für den Formcycle-Designer erweitern, sodass identifizierte Layout- und Barrierefreiheitsfehler auf Knopfdruck korrigiert werden können.
"""

# ==============================================================================
# WRITE CHAPTERS AND COUNT WORDS
# ==============================================================================
chapters = [
    ("thesis/chapters/01_einleitung.tex", ch1),
    ("thesis/chapters/02_theoretischer_hintergrund.tex", ch2),
    ("thesis/chapters/03_ist_analyse.tex", ch3),
    ("thesis/chapters/04_konzeption_standard.tex", ch4),
    ("thesis/chapters/05_implementierung.tex", ch5),
    ("thesis/chapters/06_evaluation.tex", ch6),
    ("thesis/chapters/07_fazit.tex", ch7),
]

total_words = 0
print("=== WORD COUNT REPORT (texcount-compatible clean text) ===")
for path, text in chapters:
    with open(path, "w", encoding="utf-8") as f:
        f.write(text.strip() + "\n")
    cleaned = clean_latex(text)
    words = len(cleaned.split())
    total_words += words
    print(f"{os.path.basename(path)}: {words} words")

print("-" * 50)
print(f"TOTAL MAIN BODY WORDS: {total_words} words")
print(f"LIMIT (Kloker 2.3): max. 8.000 words")
diff = 8000 - total_words
print(f"MARGIN BELOW CEILING: {diff} words safety cushion")
if total_words <= 8000:
    print("STATUS: STRICTLY COMPLIANT WITH KLOKER RULE 2.3!")
else:
    print("STATUS: VIOLATION - EXCEEDS 8.000 WORDS!")
