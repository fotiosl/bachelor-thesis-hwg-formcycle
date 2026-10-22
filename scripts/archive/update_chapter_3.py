with open('thesis/chapters/03_ist_analyse.tex', 'r', encoding='utf-8') as f:
    text = f.read()

target = r"""\subsection{Problemfeld 5: Defizite bei digitaler Barrierefreiheit (WCAG 2.1 / BITV 2.0)}
Die automatisierte DOM-Auswertung der gerenderten HTML-Dateien deckt erhebliche Mängel bezüglich digitaler Barrierefreiheit auf:
\begin{itemize}
    \item \textbf{Fehlen semantischer Gruppen (\texttt{<fieldset>}):} Während ältere Formulare semantisch korrekte \texttt{<fieldset>}-Tags mit \texttt{<legend>} einsetzen, verzichten moderne ZFK- und Beschaffungsformulare vollständig darauf und setzen rein visuelle \texttt{<div>}-Container ein. Für Screenreader geht dadurch der thematische Kontext von Eingabegruppen verloren.
    \item \textbf{Inkonsistente ARIA-Attribute:} In mehreren Formularen wird der Pflichtfeldstatus rein visuell über rote Sternchen signalisiert, ohne das maschinenlesbare Attribut \texttt{aria-required="true"} im Eingabeelement zu hinterlegen.
\end{itemize}

\section{Ableitung der Kernanforderungen an den Formular-Standard}
\label{sec:ableitung_anforderungen}

Aus der empirischen Ist-Analyse lassen sich vier fundamentale Anforderungen an den zu konzipierenden Standard und die automatisierte Prüfpipeline ableiten:

\begin{enumerate}
    \item \textbf{Standardisierte Layout- und CI-Vorgaben:} Verbindliche Festlegung auf ein einheitliches, responsives Desktop-Raster (850px) sowie zwingende Einbindung des offiziellen HWG-Header-Banners.
    \item \textbf{Zentrales Komponenten-Muster für Stammdaten:} Formalisierung eines verbindlichen Musters für persönliche Angaben mit fixer Feldabfolge (Anrede $\rightarrow$ Vorname $\rightarrow$ Nachname), standardisierter E-Mail-Syntax und konsistenter Pflichtfeld-Deklaration.
    \item \textbf{Kontext- und rollenabhängige Microcopy-Regeln:} Zwingende Formulierung von Schaltflächen als handlungsorientierte Verben im Infinitiv; strikte Entkopplung von fachlichen Ausnahme-Workflows und primären Absende-Aktionen.
    \item \textbf{Regelbasierte Barrierefreiheits-Governance:} Maschinenlesbare Durchsetzung von \texttt{<fieldset>}-Strukturen bei mehrteiligen Formularen sowie lückenlose Koppelung visueller Pflichtfeld-Sternchen an ARIA-Attribute.
\end{enumerate}

Diese Anforderungen werden im nachfolgenden Kapitel in eine formale, maschinenlesbare Komponenten- und Regel-Registry überführt."""

replacement = r"""\subsection{Problemfeld 5: Defizite bei digitaler Barrierefreiheit (WCAG 2.1 / BITV 2.0)}
Die automatisierte DOM-Auswertung der gerenderten HTML-Dateien deckt erhebliche Mängel bezüglich digitaler Barrierefreiheit auf:
\begin{itemize}
    \item \textbf{Fehlen semantischer Gruppen (\texttt{<fieldset>}):} Während ältere Formulare semantisch korrekte \texttt{<fieldset>}-Tags mit \texttt{<legend>} einsetzen, verzichten moderne ZFK- und Beschaffungsformulare vollständig darauf und setzen rein visuelle \texttt{<div>}-Container ein. Für Screenreader geht dadurch der thematische Kontext von Eingabegruppen verloren.
    \item \textbf{Inkonsistente ARIA-Attribute:} In mehreren Formularen wird der Pflichtfeldstatus rein visuell über rote Sternchen signalisiert, ohne das maschinenlesbare Attribut \texttt{aria-required="true"} im Eingabeelement zu hinterlegen.
\end{itemize}

\subsection{Problemfeld 6: Workflow-Fragmentierung und vertikale Abteilungssilos}
\label{subsec:workflow_silos}

Im Rahmen einer vertieften Untersuchung aller 49 im HWG-Instanzverzeichnis auffindbaren Formcycle-Vorlagen (15 Produktiv- sowie 34 Entwicklungs- und Testarchive) wurde empirisch überprüft, ob hochschulweit standardisierte Prozessketten über mehrere Verwaltungseinheiten hinweg existieren (z.\,B. eine universelle Abfolge von Stammdatenerfassung $\rightarrow$ Haushaltsabteilung $\rightarrow$ IT-Service $\rightarrow$ Personalabteilung).

Die Datenanalyse der hinterlegten Prozessmodelle (\texttt{workflowVersions} in den \texttt{.fcexport}-Dateien) widerlegt die Existenz einer solchen übergreifenden Standardkette:
\begin{itemize}
    \item \textbf{Hoher Anteil isolierter Einzelaufgaben:} Lediglich 14 der 49 Formulare binden überhaupt zwei oder mehr Abteilungen bzw. Prüfinstanzen ein. Die überwiegende Mehrheit (35 Vorlagen) verbleibt als rein lokale Einzelaufgabe innerhalb einer spezifischen Organisationseinheit.
    \item \textbf{Vertikale funktionale Silos statt einheitlicher Querschnittsprozesse:} Wo mehrstufige Genehmigungsketten existieren, sind diese strikt fachdomänenspezifisch strukturiert:
    \begin{enumerate}
        \item \textit{Personalbereich (HR):} Antragstellende $\rightarrow$ Führungskraft $\rightarrow$ Personalabteilung $\rightarrow$ Personalrat (PR) $\rightarrow$ Hochschulleitung (Kanzlerin/Präsident).
        \item \textit{Finanzen und Beschaffung:} Antragstellende $\rightarrow$ Sachbearbeitung Haushalt $\rightarrow$ Kontierung/Budgetverwaltung $\rightarrow$ (bei Beträgen $> 3.000$\,\euro) Genehmigungsinstanz Kanzlerin $\rightarrow$ Auszahlung/Archiv.
        \item \textit{Forschung und Transfer (ZFK):} Antragstellende $\rightarrow$ ZFK-Vorprüfung $\rightarrow$ Haushaltsabteilung $\rightarrow$ Justiziariat $\rightarrow$ Hochschulleitung $\rightarrow$ ZFK-Bewilligung.
    \end{enumerate}
    \item \textbf{Inkonsistente Status-Nomenklatur und fehlende Vorgangstransparenz:} Die dezentrale Konfiguration führt zu einer heterogenen Status-Landschaft. Ein identischer Prozessschritt (\enquote{Genehmigung}) wird in Formcycle uneinheitlich als \textit{\enquote{Akzeptiert - VG}}, \textit{\enquote{Vergabe genehmigt}}, \textit{\enquote{Antrag Praktikum angenommen}} oder \textit{\enquote{Antrag genehmigt}} bezeichnet. Zudem fehlen in vielen automatisierten E-Mails an Antragstellende eindeutige Vorgangsnummern (\texttt{[\%\$PROJECT\_ALIAS\%]}), was die manuelle Zuordnung bei Rückfragen erschwert.
\end{itemize}

\section{Ableitung der Kernanforderungen an den Formular-Standard}
\label{sec:ableitung_anforderungen}

Aus der empirischen Ist-Analyse lassen sich fünf fundamentale Anforderungen an den zu konzipierenden Standard und die automatisierte Prüfpipeline ableiten:

\begin{enumerate}
    \item \textbf{Standardisierte Layout- und CI-Vorgaben:} Verbindliche Festlegung auf ein einheitliches, responsives Desktop-Raster (850px) sowie zwingende Einbindung des offiziellen HWG-Header-Banners und Deaktivierung herstellerseitiger Fußzeilen-Logos (\texttt{showlogo="0"}).
    \item \textbf{Zentrales Komponenten-Muster für Stammdaten:} Formalisierung eines verbindlichen Musters für persönliche Angaben mit fixer Feldabfolge (Anrede $\rightarrow$ Vorname $\rightarrow$ Nachname), kanonischen Bezeichnungen (\enquote{E-Mail-Adresse}) und konsistenter Pflichtfeld-Deklaration.
    \item \textbf{Kontext- und rollenabhängige Microcopy-Regeln:} Zwingende Formulierung von Schaltflächen als handlungsorientierte Verben im Infinitiv (Action-Verb-Pattern); strikte Entkopplung von fachlichen Ausnahme-Workflows und primären Absende-Aktionen.
    \item \textbf{Regelbasierte Barrierefreiheits-Governance:} Maschinenlesbare Durchsetzung von \texttt{<fieldset>}-Strukturen bei mehrteiligen Formularen sowie lückenlose Koppelung visueller Pflichtfeld-Sternchen an ARIA-Attribute.
    \item \textbf{Workflow-Harmonisierung und Prozesstransparenz:} Standardisierung der Lebenszyklus-Zustände (Eingang $\rightarrow$ Prüfung $\rightarrow$ Entscheidung), verbindliche Führung von Vorgangs-IDs in automatisierten Bestätigungs-E-Mails sowie automatisierte Empfehlungen für Zwischenspeicher-Funktionen bei komplexen Mehrseiten-Anträgen.
\end{enumerate}

Diese Anforderungen werden im nachfolgenden Kapitel in eine formale, maschinenlesbare Komponenten- und Regel-Registry überführt."""

if target in text:
    text = text.replace(target, replacement)
    with open('thesis/chapters/03_ist_analyse.tex', 'w', encoding='utf-8') as f:
        f.write(text)
    print("SUCCESS: Chapter 3 updated")
else:
    print("WARNING: target not matched directly, normalizing newlines...")
    norm_text = text.replace('\r\n', '\n')
    norm_target = target.replace('\r\n', '\n')
    norm_rep = replacement.replace('\r\n', '\n')
    if norm_target in norm_text:
        norm_text = norm_text.replace(norm_target, norm_rep)
        with open('thesis/chapters/03_ist_analyse.tex', 'w', encoding='utf-8') as f:
            f.write(norm_text)
        print("SUCCESS: Chapter 3 updated with normalized newlines")
    else:
        print("ERROR: target still not matched")
