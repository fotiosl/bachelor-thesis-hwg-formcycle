import os

chapter4_content = r"""\chapter{Konzeption des Formular-Standards und der Prüf-Registry}
\label{chap:konzeption}

Aufbauend auf den Befunden der empirischen Ist-Analyse und den theoretischen Grundlagen der Dialogergonomie (DIN EN ISO 9241-110), der digitalen Barrierefreiheit (BITV 2.0 / WCAG 2.1) und des Datenschutzes (Art. 13 DSGVO) wird in diesem Kapitel der formale Formular-Standard für die Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG) entwickelt. Dieser Standard harmonisiert visuelle, strukturelle, ergonomische und prozessuale Dimensionen. Anschließend wird der Standard in eine maschinenlesbare Komponenten- und Regel-Registry (\texttt{rules\_registry.json}, Version 1.5.0) überführt, welche als formale Wissensbasis für die automatisierte Compliance-Prüfpipeline dient.

\section{Struktur-, Navigations- und Informationsarchitektur}
\label{sec:architektur}

Eine verlässliche institutionelle Governance erfordert eindeutige architektonische Leitplanken, die das visuelle Erscheinungsbild im Hochschulportal homogenisieren und die kognitive Belastung der Nutzenden minimieren.

\subsection{Responsives Desktop-Raster (850px-Norm)}
\label{subsec:breiten_norm}

Die in Kapitel~\ref{subsec:problem_breiten} aufgedeckte Fragmentierung zwischen älteren 700px- und neueren 850px-Layouts wird durch eine verbindliche Standardbreite aufgelöst:
\begin{itemize}
    \item \textbf{Normierung auf 850px (\texttt{HWG-CD-01}):} Sämtliche Formularvorlagen werden verbindlich auf eine Maximalbreite von \texttt{850px} (\texttt{max-width: 850px; min-width: 300px;}) normiert. 
    \item \textbf{Ergonomische Begründung:} Bei einer Standard-Schriftgröße von 14\,px bis 16\,px resultiert eine Zeilenbreite von 850\,px in einem optimalen Textband von 65 bis 75 Zeichen pro Zeile. Dies entspricht den typografischen Empfehlungen nach \textcite{wroblewski2008web} und verhindert überdehnte Zeilenlängen bei horizontalen Formularfeldern. Zugleich fügt sich das 850px-Raster nahtlos in das Content-Management-System (Typo3) des Hochschulportals ein.
    \item \textbf{Mobile Responsivität:} Durch die Mindestbreite von \texttt{300px} in Kombination mit prozentualen Spaltenbreiten (\texttt{colwidth}) brechen mehrspaltige Formularzeilen auf mobilen Endgeräten (Smartphones, Tablets) automatisch in ein ergonomisches einspaltiges Layout um.
\end{itemize}

\subsection{Seitenstrukturierung und Pagination (Chunking)}
\label{subsec:pagination_chunking}

Komplexe Verwaltungsprozesse im Hochschulbereich (wie Auslagenerstattungen, Drittmittelanträge oder Stellenausschreibungen) umfassen häufig 50 bis über 100 Einzelfelder. Ein monolithisches Single-Page-Design überfordert Nutzende kognitiv und führt zu hohen Abbruchraten \cite{bargas2010usable, seckler2014validation}.

\begin{itemize}
    \item \textbf{Regelbasiertes Chunking:} Formulare mit mehr als 20 Einzelelementen müssen in logisch abgegrenzte, sequenzielle Bildschirmseiten (\texttt{XPage}) unterteilt werden. Die Unterteilung folgt fachlichen Phasen: (1) Persönliche Angaben / Stammdaten $\rightarrow$ (2) Sachverhalts- und Antragsdaten $\rightarrow$ (3) Finanzielle Kalkulation / Belege $\rightarrow$ (4) Bestätigung, Datenschutz und Abschluss.
    \item \textbf{Lineare Navigationssteuerung (\texttt{HWG-BTN-02}):} Zur Seitensteuerung dürfen ausschließlich standardisierte Schaltflächen mit den Beschriftungen \textit{\enquote{Weiter}} (primär, rechtsbündig) und \textit{\enquote{Zurück}} (sekundär, linksbündig) eingesetzt werden. Unpräzise Bezeichnungen wie \textit{\enquote{weiter zu Seite 2}} oder \textit{\enquote{nächster Schritt}} sind unzulässig, da sie bei nachträglichen Seitenverschiebungen im Designer inkonsistent werden.
\end{itemize}

\section{Corporate Design, Barrierefreiheit und Stammdaten-Muster}
\label{sec:cd_komponenten}

Die visuelle und programmatische Gestaltung bildet die Brücke zwischen der institutionellen Identität der HWG Ludwigshafen und den gesetzlichen Anforderungen an die Barrierefreiheit nach BITV 2.0.

\subsection{Corporate Identity, Header- und Footer-Struktur}
\label{subsec:ci_header_footer}

Jedes öffentlich zugängliche oder interne Formular repräsentiert die Hochschule als administrative Behörde:
\begin{itemize}
    \item \textbf{Offizielles Bildbanner (\texttt{HWG-CD-02}):} Im Kopfbereich des Formulars muss zwingend das offizielle Bildbanner der Hochschule als \texttt{XImage}-Komponente platziert werden. Zur Erfüllung von WCAG 2.1 Erfolgskriterium 1.1.1 (Nicht-Text-Inhalt) muss das Bild mit dem Alternativtext \textit{\enquote{Hochschule für Wirtschaft und Gesellschaft Ludwigshafen}} hinterlegt sein.
    \item \textbf{Deaktivierung herstellerseitiger Werbelogos (\texttt{HWG-CD-03}):} In der Fußzeile (\texttt{XFooter}) muss der herstellerseitige Hinweis \textit{\enquote{Powered by XIMA Formcycle}} deaktiviert werden. Dies geschieht im Formcycle-Designer durch Abwählen der Option \textit{\enquote{Logo anzeigen}} (\texttt{properties.showlogo = "0"}). Dies eliminiert fremdes Software-Branding und unterstreicht die Authentizität des hochschuleigenen Dienstes.
\end{itemize}

\subsection{Semantische Gruppierung und Pflichtfeld-Indikation}
\label{subsec:fieldsets_aria}

Die in Kapitel~\ref{subsec:problem_a11y} aufgedeckten Barrierefreiheitsdefizite erfordern verbindliche technische Vorgaben für Formcycle-Autoren:

\begin{itemize}
    \item \textbf{Semantische Fieldset-Gruppierung (\texttt{HWG-A11Y-01}):} Gemäß WCAG 2.1 Erfolgskriterium 1.3.1 (Info und Beziehungen) dürfen thematische Blöcke nicht ausschließlich durch rein visuelle \texttt{<div>}-Container oder einfache Rahmen strukturiert werden. Jeder logische Abschnitt muss als semantisches \texttt{XFieldSet} angelegt und mit einer lesbaren Legende (\texttt{legend}) versehen werden (z.\,B. \textit{\enquote{Persönliche Angaben}}, \textit{\enquote{Bankverbindung}}, \textit{\enquote{Projektdetails}}). Screenreader kündigen diese Legende beim Betreten jedes enthaltenen Feldes an.
    \item \textbf{Konsistente Pflichtfeld-Indikation und ARIA-Deklaration (\texttt{HWG-A11Y-02}):} Gemäß WCAG 2.1 Erfolgskriterium 3.3.2 muss jedes erforderliche Feld sowohl für sehende als auch für blinde Nutzende zweifelsfrei erkennbar sein:
    \begin{enumerate}
        \item Im Formcycle-Designer muss unter \textit{Einschränkungen} das Kontrollkästchen \textit{\enquote{Pflichtfeld}} (\texttt{required = "1"}) gemeinsam mit \textit{\enquote{Pflichtfeldhinweis anzeigen}} (\texttt{showrequiredhint = "1"}) aktiviert werden. Formcycle rendert hierdurch automatisch sowohl das visuelle Sternchen (\texttt{*}) als auch das HTML-Attribut \texttt{aria-required="true"}.
        \item Bei Feldern, die erst dynamisch durch JavaScript oder Formcycle-Bedingungen zum Pflichtfeld werden (\texttt{requiredif}), muss \texttt{aria-required="true"} explizit im Designer unter \textit{Erweitert $\rightarrow$ HTML-Attribute} hinterlegt werden.
        \item Manuelle Textsternchen im Feldlabel sind verboten, um Kollisionen mit geschlechtergerechter Sprache (\textit{\enquote{Antragsteller*in}}) und Doppelansagen im Screenreader zu verhindern.
    \end{enumerate}
    \item \textbf{Bereinigung von HTML-Fragmenten (\texttt{HWG-A11Y-03}):} Feldlabels und Hilfetexte müssen als reiner Text hinterlegt werden. HTML-Tags wie \texttt{<p>}, \texttt{<br>} oder HTML-Entities wie \texttt{\&szlig;} dürfen nicht im Label-String verbleiben.
\end{itemize}

\subsection{Das normierte HWG-Stammdaten-Muster}
\label{subsec:stammdaten_muster}

Um die empirisch festgestellten Copy-Paste-Abweichungen und Vertauschungen (z.\,B. Name vor Vorname) dauerhaft zu unterbinden, definiert der Standard ein starres Stammdaten-Muster:

\begin{enumerate}
    \item \textbf{Sequenz-Garantie (\texttt{HWG-STAMM-01}):} Persönliche Angaben folgen ausnahmslos der natürlichen Sequenz:
    \begin{equation}
        \text{Anrede} \longrightarrow \text{Vorname} \longrightarrow \text{Nachname} \longrightarrow \text{E-Mail-Adresse}
    \end{equation}
    Eine Voranstellung des Nachnamens ist nur in behördlichen Sonderregistern gestattet.
    \item \textbf{Kanonische Feldbezeichnungen (\texttt{HWG-STAMM-02}):} Zur Vermeidung von Mehrdeutigkeiten sind ausschließlich die kanonischen Standardbezeichnungen zulässig:
    \begin{itemize}
        \item \textit{\enquote{Anrede}} (als \texttt{XSelect} mit den Optionen Herr, Frau, Divers, Keine Angabe),
        \item \textit{\enquote{Vorname}} (ohne Zusätze),
        \item \textit{\enquote{Nachname}} (nicht bloß \enquote{Name} und ohne Rollenzusätze wie \enquote{Name Antragstellende/r}),
        \item \textit{\enquote{E-Mail-Adresse}} (bzw. \textit{\enquote{Hochschul-E-Mail}}, falls eine Authentifizierung über die Hochschuldomäne erforderlich ist).
    \end{itemize}
    \item \textbf{Bereinigung von Entwickler-Rückständen (\texttt{HWG-UI-01}):} Sichtbare Skript-Kommentare, LDAP-Authentifizierungs-Hinweise oder interne Programmiernotizen im Formular-Frontend sind im Produktivzustand strikt untersagt.
\end{enumerate}

\section{Datenschutz, Eingabevalidierung und Microcopy}
\label{sec:datenschutz_validierung}

Über das Layout hinaus werden zentrale funktionale Qualitätsanforderungen formalisiert, die Fehleingaben verhindern und Rechtssicherheit schaffen.

\subsection{Datenschutz-Transparenz nach Art. 13 DSGVO (\texttt{HWG-DSGVO-01})}
\label{subsec:dsgvo_standard}

Sobald ein Formular personenbezogene Daten erfasst (Vorname, Nachname, E-Mail, Matrikelnummer oder Bankverbindungen), muss unmittelbar vor der finalen Absende-Schaltfläche oder über den aktivierten Datenschutzbereich des Footers (\texttt{privacyPolicyShow = "1"}) ein verständlicher Datenschutzhinweis eingebunden sein. Dieser muss den Verarbeitungszweck knapp umreißen und einen aktiven Hyperlink auf die zentrale Datenschutzerklärung der HWG Ludwigshafen (\url{https://www.hwg-lu.de/datenschutz}) enthalten.

\subsection{Strukturierte Formatvalidierung (\texttt{HWG-VAL-01})}
\label{subsec:validierung_standard}

Eingabefelder für strukturierte Datenformate dürfen keinesfalls als unvalidierte Freitexte verbleiben. Es sind formale Validierungsmuster (Regex) im Formcycle-Designer zu konfigurieren:
\begin{itemize}
    \item \textbf{Postleitzahl:} Deutsche Postleitzahlen müssen über das Muster \texttt{\^{}[0-9]\{5\}\$} auf exakt fünf Ziffern validiert werden.
    \item \textbf{IBAN:} Bankverbindungen müssen nach dem SEPA-Standard validiert werden (z.\,B. \texttt{\^{}[A-Z]\{2\}[0-9]\{20\}\$} für deutsche Konten).
    \item \textbf{Telefonnummern und Datumsfelder:} Müssen über standardisierte Formcycle-Presets oder Regex-Ausdrücke gegen Fehleingaben abgesichert sein.
\end{itemize}

\subsection{Affordanzgerechte Feldbreiten (\texttt{HWG-UX-01})}
\label{subsec:affordanz_breiten}

Kurze strukturierte Eingabefelder (z.\,B. fünfstellige Postleitzahlen oder Hausnummern) dürfen nicht auf 100\,\% der Zeilenbreite gestreckt werden. Die visuelle Feldlänge fungiert als nonverbale Affordanz nach \textcite{wroblewski2008web} und signalisiert den Nutzenden die erwartete Zeichenanzahl. Kompakte Felder müssen daher über \texttt{colwidth} oder \texttt{maxwidth} auf maximal \texttt{150px} begrenzt werden.

\subsection{Transparente Dateiupload-Spezifikationen (\texttt{HWG-UPLOAD-01})}
\label{subsec:upload_standard}

Dateiupload-Elemente (\texttt{XUpload}, \texttt{XFile}) stellen häufige Fehlerquellen dar. Erstellende müssen im Label oder im Hilfetext transparent ausweisen:
\begin{enumerate}
    \item die zulässigen Dateiformate (z.\,B. \textit{\enquote{Erlaubte Formate: PDF, JPG, PNG}}),
    \item die maximale Dateigröße pro Upload (z.\,B. \textit{\enquote{Maximale Dateigröße: 10 MB}}).
\end{enumerate}

\subsection{Schaltflächen-Semantik nach dem Action-Verb-Muster (\texttt{HWG-BTN-01})}
\label{subsec:action_verb_standard}

Schaltflächen stellen den kritischen Übergang zwischen Benutzerinteraktion und Systemtransaktion dar. Zur Wahrung der \textbf{Erwartungskonformität und Selbstbeschreibungsfähigkeit (ISO 9241-110)} müssen alle Aktionsschaltflächen dem \textbf{Action-Verb-Muster} folgen:
\begin{itemize}
    \item Sie müssen aus einer Kombination aus Zielobjekt und einem konkreten Vollverb im Infinitiv bestehen (z.\,B. \textit{\enquote{Antrag einreichen}}, \textit{\enquote{Bedarfsmeldung absenden}}, \textit{\enquote{Kritischen Fall einreichen}}).
    \item Reine Substantive oder Statusbezeichnungen (wie im Negativbeispiel \textit{\enquote{Kritischer Fall}}) sind verboten.
    \item Generische Minimal-Labels (wie das kleingeschriebene \textit{\enquote{senden}} oder \textit{\enquote{Submit}}) sind unzulässig.
\end{itemize}

\subsection{Verständliche Verwaltungssprache und Jargon-Erklärung (\texttt{HWG-LANG-01}, \texttt{HWG-LANG-02})}
\label{subsec:sprache_standard}

Formulare der Hochschulverwaltung enthalten regelmäßig verwaltungsspezifische Fachbegriffe (z.\,B. \textit{Kostenstelle}, \textit{Vergabevermerk}, \textit{KAP}, \textit{Remonstration}, \textit{GStB}). Gemäß WCAG 2.1 Richtlinie 3.1 (Verständlichkeit) gilt:
\begin{itemize}
    \item Fachjargon darf verwendet werden, muss jedoch zwingend von einem erläuternden Hilfetext oder Tooltip begleitet sein (\texttt{HWG-LANG-01}).
    \item Anweisungen und Hilfetexte müssen barrierearm formuliert sein; verschachtelte Schachtelsätze mit mehr als 25 Wörtern sind zu vermeiden (\texttt{HWG-LANG-02}).
\end{itemize}

\section{Workflow-Governance und Prozess-Harmonisierung}
\label{sec:workflow_governance}

Wie die empirische Untersuchung in Kapitel~\ref{subsec:workflow_silos} belegte, sind Verwaltungsprozesse an der HWG Ludwigshafen historisch in vertikalen Abteilungssilos gewachsen. Um diese Schnittstellen zu harmonisieren, erweitert der Standard die Governance auf den nachgelagerten Bearbeitungsprozess:

\subsection{Standardisierte Workflow-Statusnomenklatur (\texttt{HWG-WF-01})}
\label{subsec:workflow_status}

Jeder mehrstufige Formcycle-Workflow muss über explizite Statusänderungs-Knoten (\texttt{FC\_CHANGE\_STATE}) verfügen. Um die beobachtete Begriffsverwirrung (z.\,B. \textit{Akzeptiert - VG} vs. \textit{Vergabe genehmigt}) zu beenden, wird ein kanonischer Standard-Lebenszyklus definiert:
\begin{equation}
    \text{Eingegangen} \longrightarrow \text{In Prüfung} \longrightarrow \left[\text{Nachforderung ausstehend}\right] \longrightarrow \text{Genehmigt} \, / \, \text{Abgelehnt} \longrightarrow \text{Archiviert}
\end{equation}
Ad-hoc-Zustände ohne klare Prozessbedeutung (wie \textit{\enquote{Durch VG ergänzt}} oder \textit{\enquote{Kritischer Fall Rückmeldung}}) sind unzulässig.

\subsection{Eindeutige Vorgangsreferenz in Prozess-E-Mails (\texttt{HWG-WF-02})}
\label{subsec:workflow_ref}

Zur Gewährleistung der Nachvollziehbarkeit müssen sämtliche im Workflow generierten automatisierten E-Mails (\texttt{FC\_EMAIL}) an Antragstellende und Sachbearbeitende zwingend die eindeutige Systemvariable der Vorgangsnummer (\texttt{[\%\$PROJECT\_ALIAS\%]}) im Betreff oder Textkörper führen. Dies ermöglicht es allen Beteiligten, Rückfragen und Bescheide ohne manuelle Suchzeiten dem korrekten Vorgang zuzuordnen.

\subsection{Prozesstransparenz und Zwischenspeicher-Empfehlung (\texttt{HWG-FEEDBACK-01}, \texttt{HWG-UX-02})}
\label{subsec:feedback_save_resume}

\begin{itemize}
    \item \textbf{Eingangsbestätigung (\texttt{HWG-FEEDBACK-01}):} Der Workflow muss nach dem Absenden unmittelbar eine Eingangsbestätigung per E-Mail an die antragstellende Person versenden, welche über den Eingang, die zuständige Stelle und die durchschnittliche Bearbeitungsdauer transparent informiert.
    \item \textbf{Empfehlung für Zwischenspeichern (\texttt{HWG-UX-02}):} Überschreitet ein Formular eine kritische Komplexitätsschwelle ($\ge 3$ Bildschirmseiten oder $\ge 25$ Eingabefelder), spricht die Registry eine unverbindliche Empfehlung (\textit{Recommendation}, 0 Punkte Abzug) aus: Im Formular sollte eine \textit{\enquote{Zwischenspeichern}}-Schaltfläche integriert werden, die den Bearbeitungsstand sichert und den Nutzenden einen Fortsetzungs-Link per E-Mail zusendet.
\end{itemize}

\section{Formalisierung als maschinenlesbare Komponenten- und Regel-Registry}
\label{sec:registry_definition}

Um die Einhaltung dieser Vorgaben objektiv und automatisiert auditieren zu können, werden alle Kriterien in ein maschinenlesbares JSON-Schema (\texttt{rules\_registry.json}, Version 1.5.0) überführt.

\subsection{Mathematisches Bewertungsmodell}
\label{subsec:scoring_modell}

Das Konformitätsniveau eines Formulars wird über einen normalisierten Compliance-Score $S \in [0, 100]$ quantifiziert. Ausgehend von einem Basisscore von 100 Punkten führt jeder detektierte Verstoß zu einem fest definierten Punktabzug in Abhängigkeit von seiner Schweregrad-Klasse nach \textcite{nielsen1994severity}:

\begin{equation}
    S = \max\left(0, \, 100 - \sum_{i=1}^{M} w(r_i) \cdot v(r_i)\right)
    \label{eq:compliance_score}
\end{equation}

Hierbei bezeichnet:
\begin{itemize}
    \item $v(r_i) \in \{0, 1\}$ den binären Auslösestatus der Regel $r_i$ ($1 = \text{Verstoß ausgelöst}$, $0 = \text{konform}$).
    \item $w(r_i)$ das theoretisch fundierte Strafmaß der jeweiligen Schweregrad-Kategorie:
    \begin{equation}
        w(r_i) = \begin{cases}
            15 & \text{für } \textit{critical} \text{ (rechtliche/technische Blocker nach Nielsen)} \\
            8  & \text{für } \textit{major} \text{ (schwere Usability-/CI-Verletzungen)} \\
            3  & \text{für } \textit{minor} \text{ (syntaktische oder gestalterische Mängel)} \\
            0  & \text{für } \textit{recommendation} \text{ (unverbindliche UX-Empfehlung ohne Punktabzug)}
        \end{cases}
    \end{equation}
\end{itemize}

\subsection{Katalog der formalisierten Governance-Regeln}
\label{subsec:regelkatalog_tabelle}

Tabelle~\ref{tab:rules_overview} fasst die 21 formalisierten Prüfregeln (20 bewertete Compliance-Regeln sowie 1 unverbindliche Empfehlungsregel) der Registry v1.5.0 zusammen:

\begin{table}[H]
\centering
\scriptsize
\begin{tabularx}{\textwidth}{llllX}
\toprule
\textbf{Regel-ID} & \textbf{Bezeichnung} & \textbf{Kategorie} & \textbf{Typ} & \textbf{Schweregrad \& Begründung} \\
\midrule
\texttt{HWG-CD-01} & Standardbreite 850px & Corporate Design & Deterministisch & Major (8 Pkt): Einheitliches Raster \\
\texttt{HWG-CD-02} & Offizieller CI-Header & Corporate Design & Deterministisch & Critical (15 Pkt): Authentizität / Logo \\
\texttt{HWG-CD-03} & Kein XIMA-Logo im Footer & Corporate Design & Deterministisch & Major (8 Pkt): \texttt{showlogo="0"} im Footer \\
\texttt{HWG-A11Y-01} & Fieldset-Gruppierung & Accessibility & Deterministisch & Critical (15 Pkt): WCAG 1.3.1 \\
\texttt{HWG-A11Y-02} & Pflichtfeld-Stern/ARIA & Accessibility & Deterministisch & Major (8 Pkt): WCAG 3.3.2 (\texttt{required="1"}) \\
\texttt{HWG-A11Y-03} & Saubere Label-Syntax & Accessibility & Deterministisch & Minor (3 Pkt): Keine HTML-Entities \\
\texttt{HWG-STAMM-01} & Stammdaten-Sequenz & Stammdaten & Deterministisch & Major (8 Pkt): Natürlicher Lesefluss \\
\texttt{HWG-STAMM-02} & Kanonische Stammdaten & Stammdaten & Semantisch & Minor (3 Pkt): Einheitliche Feldlabels \\
\texttt{HWG-UI-01} & Keine Dev-Notizen & UI-Qualität & Deterministisch & Critical (15 Pkt): Saubere UI ohne Artefakte \\
\texttt{HWG-BTN-01} & Action-Verb-Muster Buttons & Microcopy & Semantisch & Major (8 Pkt): Zielobjekt + Vollverb \\
\texttt{HWG-BTN-02} & Einheitliche Pagination & Microcopy & Semantisch & Minor (3 Pkt): Weiter/Zurück \\
\texttt{HWG-DSGVO-01} & Datenschutz-Transparenz & Datenschutz & Deterministisch & Critical (15 Pkt): Art. 13 DSGVO \\
\texttt{HWG-UPLOAD-01} & Upload-Spezifikation & Validierung/UX & Deterministisch & Major (8 Pkt): Dateitypen \& Max-Größe \\
\texttt{HWG-VAL-01} & Formatvalidierung & Validierung/UX & Deterministisch & Major (8 Pkt): IBAN/PLZ/Datum-Regex \\
\texttt{HWG-UX-01} & Feldbreiten-Affordanz & Validierung/UX & Deterministisch & Minor (3 Pkt): Kompakte Breiten \\
\texttt{HWG-UX-02} & Zwischenspeichern-Option & Validierung/UX & Semantisch & Recommendation (0 Pkt): Ab 3 S. / 25 Feldern \\
\texttt{HWG-LANG-01} & Amtsjargon mit Erklärung & Leichte Sprache & Semantisch & Major (8 Pkt): WCAG 3.1 \\
\texttt{HWG-LANG-02} & Barrierearme Sprache & Leichte Sprache & Semantisch & Minor (3 Pkt): Keine Schachtelsätze \\
\texttt{HWG-FEEDBACK-01} & Workflow-E-Mail-Feedback & Transparenz & Semantisch & Minor (3 Pkt): \texttt{FC\_EMAIL} im Workflow \\
\texttt{HWG-WF-01} & Workflow-Status-Lebenszyklus & Workflow & Deterministisch & Minor (3 Pkt): Kanonische Statusknoten \\
\texttt{HWG-WF-02} & Vorgangs-ID in E-Mails & Workflow & Deterministisch & Minor (3 Pkt): [\%$\$$PROJECT\_ALIAS\%] \\
\bottomrule
\end{tabularx}
\caption{Übersicht der formalisierten Formular-Governance-Regeln in der Registry v1.5.0}
\label{tab:rules_overview}
\end{table}

Diese formalisierte Registry bildet das exakte Fundament für die im folgenden Kapitel beschriebene zweistufige Prüfpipeline.
"""

with open('thesis/chapters/04_konzeption_standard.tex', 'w', encoding='utf-8') as f:
    f.write(chapter4_content)

print(f"SUCCESS: Chapter 4 written ({len(chapter4_content)} characters)")
