with open('thesis/chapters/04_konzeption_standard.tex', 'r', encoding='utf-8') as f:
    text = f.read()

target = r"""\subsection{Katalog der formalisierten Governance-Regeln}
Tabelle~\ref{tab:rules_overview} fasst die 19 formalisierten Prüfregeln (18 bewertete Compliance-Regeln sowie 1 unverbindliche Empfehlungsregel) der Registry v1.3.0 zusammen:

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
\bottomrule
\end{tabularx}
\caption{Übersicht der formalisierten Formular-Governance-Regeln in der Registry v1.3.0}
\label{tab:rules_overview}
\end{table}"""

replacement = r"""\subsection{Katalog der formalisierten Governance-Regeln}
Tabelle~\ref{tab:rules_overview} fasst die 20 formalisierten Prüfregeln (19 bewertete Compliance-Regeln sowie 1 unverbindliche Empfehlungsregel) der Registry v1.4.0 zusammen:

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
\texttt{HWG-WF-01} & Workflow-Governance & Workflow & Deterministisch & Minor (3 Pkt): Status-Nomenklatur \& Ref-ID \\
\bottomrule
\end{tabularx}
\caption{Übersicht der formalisierten Formular-Governance-Regeln in der Registry v1.4.0}
\label{tab:rules_overview}
\end{table}"""

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_rep = replacement.replace('\r\n', '\n')

if norm_target in norm_text:
    norm_text = norm_text.replace(norm_target, norm_rep)
    with open('thesis/chapters/04_konzeption_standard.tex', 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print("SUCCESS: Chapter 4 updated")
else:
    print("ERROR: target not found in Chapter 4")
