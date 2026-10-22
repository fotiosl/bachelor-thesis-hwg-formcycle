import os
import re

# =========================================================
# Chapter 1 Streamlined (~720 words)
# =========================================================
ch1_content = r"""\chapter{Einleitung und Problemstellung}
\label{chap:einleitung}

\section{Ausgangssituation und Motivation}
\label{sec:ausgangssituation}

Die digitale Transformation der öffentlichen Verwaltung in Deutschland verlangt zunehmend durchgängig integrierte, medienbruchfreie und barrierefreie End-to-End-Prozesse. Das Onlinezugangsgesetz (OZG), das E-Government-Gesetz Rheinland-Pfalz (EGovG RLP) sowie europäische Richtlinien (EU-Richtlinie 2016/2102) verpflichten auch staatliche Hochschulen, ihre administrativen Dienstleistungen digital zugänglich zu machen. Webformulare bilden dabei die primäre Schnittstelle zwischen Studierenden, Lehrenden, Forschenden und der Verwaltung. Ihre ergonomische Qualität bestimmt maßgeblich die Effizienz und Fehleranfälligkeit des Verwaltungshandelns (\textcite{wroblewski2008web, bargas2010usable}).

An der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG Ludwigshafen) wurde zur Bewältigung dieser Digitalisierungsaufgabe das Enterprise-Formular-Management-System (FMS) \textit{XIMA Formcycle} eingeführt. Formcycle ermöglicht es dezentralen Fachbereichen und Abteilungen, Formulare eigenständig im Low-Code-Verfahren zu erstellen. In der Praxis führte diese Dezentralisierung jedoch zu einem \textit{Governance- und Compliance-Vakuum}. Da ein verbindlicher, maschinenlesbarer Standard bislang fehlte, entstanden stark heterogene Insellösungen mit gravierenden Mängeln:
\begin{itemize}
    \item \textbf{Inkonsistentes Corporate Design:} Veraltete Breiten (700px) wechseln unvorhersehbar mit modernen Rastern (850px); offizielle Hochschul-Header fehlen vielfach.
    \item \textbf{Barrierefreiheitsdefizite (WCAG 2.1 / BITV 2.0):} Semantische Fieldsets fehlen häufig, und Pflichtfelder sind für Screenreader teils nicht maschinenlesbar hinterlegt.
    \item \textbf{Ergonomische Brüche:} Schaltflächen verletzen das \textit{Action-Verb-Pattern} durch generische Labels (\texttt{senden}) oder irritierende Statusbezeichnungen (\enquote{Kritischer Fall}) entgegen DIN EN ISO 9241-110.
    \item \textbf{Datenschutz- und Prozesstransparenz:} Bei personenbezogenen Daten fehlen oft DSGVO-Hinweise (Art. 13 DSGVO), und Antragstellende erhalten keine automatisierten Eingangsbestätigungen mit eindeutigen Vorgangsnummern.
\end{itemize}

Statische Leitfäden werden im Arbeitsalltag selten konsultiert, und manuelle Audits sind personell nicht skalierbar. Hieraus erwächst der Bedarf für ein automatisiertes, kontinuierliches Qualitätsaudit direkt in der Formular-Pipeline.

\section{Zielsetzung und forschungsleitende Fragestellungen}
\label{sec:zielsetzung}

Das Ziel dieser Bachelorarbeit ist die \textbf{Konzeption eines harmonisierten Formular-Standards für die HWG Ludwigshafen} sowie die \textbf{prototypische Entwicklung einer hybriden, KI-gestützten Compliance-Prüfpipeline}, welche Formcycle-Vorlagen objektiv auditiert, Verstöße quantifiziert und handlungsorientierte Korrekturpfade bereitstellt.

Hieraus leitet sich die primäre Forschungsfrage ab:
\begin{quote}
    \textit{\textbf{MRQ:} Wie kann ein einheitlicher, barrierefreier und ergonomischer Formular-Standard für die HWG Ludwigshafen konzipiert und dessen Einhaltung durch eine automatisierte Prüfpipeline in Formcycle prototypisch durchgesetzt werden?}
\end{quote}

Die Beantwortung erfolgt entlang von vier Teilforschungsfragen:
\begin{enumerate}
    \item[\textbf{FQ1:}] Welche empirischen Gestaltungs-, Usability- und Barrierefreiheitsdefizite kennzeichnen den aktuellen Formularbestand der HWG Ludwigshafen?
    \item[\textbf{FQ2:}] Welche Kriterien müssen in einem maschinenlesbaren Standard spezifiziert werden, um ISO 9241-110, BITV 2.0 und DSGVO zu genügen?
    \item[\textbf{FQ3:}] Wie muss eine hybride Prüfarchitektur aus deterministischer AST-Strukturprüfung und semantischem LLM-Context-Engineering technisch gestaltet sein?
    \item[\textbf{FQ4:}] Mit welcher Präzision und Robustheit identifiziert die Pipeline Regelverstöße, und inwieweit lässt sich das System unabhängig von proprietären Sprachmodellen betreiben?
\end{enumerate}

\section{Forschungsmethodischer Aufbau der Arbeit}
\label{sec:aufbau}

Die wissenschaftliche Vorgehensweise folgt dem Paradigma des \textbf{Design Science Research (DSR)} nach \textcite{hevner2004design} und dem Prozessmodell nach \textcite{peffers2007design}. Zur Sicherung methodischer Rigorosität orientiert sich die Ausarbeitung an den Grundsätzen wissenschaftlicher Praxis nach \textcite{recker2013scientific}, \textcite{cochrane2005writing} sowie \textcite{kornmeier2011}.

Die Arbeit gliedert sich wie folgt:
\begin{itemize}
    \item \textbf{Kapitel 2 (Theoretischer Hintergrund):} Fundierung der Usability-Normen (ISO 9241-110), Barrierefreiheitsstandards (BITV 2.0), Heuristiken und LLM-Audits.
    \item \textbf{Kapitel 3 (Empirische Ist-Analyse):} Bestandsaufnahme von 34 realen HWG-Formularen und 49 Workflow-Definitionen zur Identifikation von sechs Problemfeldern.
    \item \textbf{Kapitel 4 (Konzeption des Standards):} Formalisierung der Governance-Vorgaben in einer maschinenlesbaren Compliance-Registry (\texttt{rules\_registry.json}) mit 21 Regeln und mathematischem Scoring-Modell.
    \item \textbf{Kapitel 5 (Prototypische Implementierung):} Technische Umsetzung der zweistufigen Prüfpipeline und des barrierefreien Intranet-Dashboards.
    \item \textbf{Kapitel 6 (Empirische Evaluation):} Quantitative Validierung an synthetischen Ground-Truth-Mustern, realen Anträgen und empirischer Vergleich von fünf Open-Source-LLMs.
    \item \textbf{Kapitel 7 (Fazit und Ausblick):} Beantwortung der Forschungsfragen, Handlungsempfehlungen für die HWG Ludwigshafen und Forschungsausblick.
\end{itemize}
"""

with open("thesis/chapters/01_einleitung.tex", "w", encoding="utf-8") as f:
    f.write(ch1_content.strip() + "\n")

print("Kapitel 1 gestrafft!")
