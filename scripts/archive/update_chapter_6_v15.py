with open('thesis/chapters/06_evaluation.tex', 'r', encoding='utf-8') as f:
    text = f.read()

target = r"""Tabelle~\ref{tab:eval_results} fasst die Ergebnisse der automatisierten Compliance-Prüfung (Registry v1.4.0) über alle Testinstanzen zusammen:

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lccccX}
\toprule
\textbf{Formular-Instanz} & \textbf{Typ} & \textbf{Score} & \textbf{Bestanden} & \textbf{Verstöße} & \textbf{Zentrale Befunde \& Empfehlungen} \\
\midrule
\textit{Synthetisch Konform} & Benchmark & 100 / 100 & 15 & 0 & Perfektes Referenzmuster \\
\textit{Synthetisch Fehlerhaft} & Benchmark & 0 / 100 & 1 & 14 & Alle 14 Injektionen erkannt \\
\midrule
\textit{Auslagenerstattung} & Real (Prod) & 41 / 100 & 6 & 9 & DSGVO, Uploads, IBAN unvalidiert, Workflow-Ref fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (49 Felder) \\
\textit{Antrag-Sprints ZFK} & Real (Test) & 30 / 100 & 7 & 8 & Kein Logo, XIMA-Footer aktiv, keine Fieldsets, DSGVO, Workflow-Ref fehlt \\
\textit{Master-Formular} & Real (Admin) & 72 / 100 & 9 & 6 & 700px, HTML-Entities, PLZ gestreckt, Workflow-Ref fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (29 Felder) \\
\bottomrule
\end{tabularx}
\caption{Quantitative Evaluationsergebnisse der Compliance-Pipeline (Registry v1.4.0)}
\label{tab:eval_results}
\end{table}

\subsection{Analyse der Erkennungsleistung}
Am synthetischen Kontrollkorpus erreichte die Pipeline eine Erkennungsgenauigkeit (\textit{Accuracy}) von 100\,\%:
\begin{itemize}
    \item Beim fehlerhaften Referenzformular wurden sämtliche 14 injizierten Mängel (von der veralteten 700px-Breite und dem aktivierten XIMA-Footer-Logo über fehlende Datenschutz-Klauseln und unzulässige Button-Labels bis hin zu Workflow-Governance-Defiziten) lückenlos identifiziert.
    \item Beim vollkonformen Formular traten keinerlei Fehlalarme (\textit{False Positives}) auf.
\end{itemize}

\subsection{Ergebnisse am realen HWG-Bestand}
Die Auswertung der realen Bestandsformulare unterstreicht die hohe diagnostische Trennschärfe der erweiterten Registry v1.4.0:
\begin{itemize}
    \item Das Produktivformular \textit{Auslagenerstattung} erreicht einen Score von 41 Punkten. Positiv hervorzuheben ist, dass das XIMA-Logo im Footer deaktiviert wurde (\texttt{HWG-CD-03} bestanden) und im hinterlegten Workflow eine ausführliche Eingangsbestätigungs-E-Mail existiert (\texttt{HWG-FEEDBACK-01} bestanden). Abzüge resultieren primär aus dem Fehlen einer DSGVO-Klausel im Formular, unvollständigen Upload-Beschränkungen, unmaskierten IBAN-/PLZ-Eingaben sowie dem Fehlen der Vorgangsnummer (\texttt{[\%\$PROJECT\_ALIAS\%]}) im E-Mail-Betreff (\texttt{HWG-WF-01}). Zudem löst die hohe Komplexität (3 Seiten, 49 Eingabefelder) die abzugsfreie Empfehlung \texttt{HWG-UX-02} zur Ergänzung einer Zwischenspeichern-Funktion aus.
    \item Der \textit{Antrag-Sprints} des ZFK (Score: 30 Punkte) verfügt zwar über eine vorbildliche Workflow-Eingangsbestätigung per E-Mail, weist jedoch im Frontend gravierende Mängel auf (fehlendes Logo, aktives XIMA-Herstellerbranding, fehlende Fieldsets und fehlende DSGVO-Klausel).
    \item Das interne \textit{Master-Formular} bestätigt mit 72 Punkten seine Eignung als Blaupause, offenbart jedoch bestehende Nachbesserungsbedarfe bezüglich 700px-Breite, HTML-Entities und unvalidierter PLZ-Felder.
\end{itemize}"""

replacement = r"""Tabelle~\ref{tab:eval_results} fasst die Ergebnisse der automatisierten Compliance-Prüfung (Registry v1.5.0) über alle Testinstanzen zusammen:

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lccccX}
\toprule
\textbf{Formular-Instanz} & \textbf{Typ} & \textbf{Score} & \textbf{Bestanden} & \textbf{Verstöße} & \textbf{Zentrale Befunde \& Empfehlungen} \\
\midrule
\textit{Synthetisch Konform} & Benchmark & 100 / 100 & 16 & 0 & Perfektes Referenzmuster \\
\textit{Synthetisch Fehlerhaft} & Benchmark & 0 / 100 & 1 & 15 & Alle 15 Injektionen erkannt \\
\midrule
\textit{Auslagenerstattung} & Real (Prod) & 41 / 100 & 7 & 9 & DSGVO, Uploads, IBAN unvalidiert, Vorgangs-ID fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (49 Felder) \\
\textit{Antrag-Sprints ZFK} & Real (Test) & 30 / 100 & 8 & 8 & Kein Logo, XIMA-Footer aktiv, keine Fieldsets, DSGVO, Vorgangs-ID fehlt \\
\textit{Master-Formular} & Real (Admin) & 72 / 100 & 10 & 6 & 700px, HTML-Entities, PLZ gestreckt, Vorgangs-ID fehlt; \textit{Empfehlung:} \texttt{HWG-UX-02} (29 Felder) \\
\bottomrule
\end{tabularx}
\caption{Quantitative Evaluationsergebnisse der Compliance-Pipeline (Registry v1.5.0)}
\label{tab:eval_results}
\end{table}

\subsection{Analyse der Erkennungsleistung}
Am synthetischen Kontrollkorpus erreichte die Pipeline eine Erkennungsgenauigkeit (\textit{Accuracy}) von 100\,\%:
\begin{itemize}
    \item Beim fehlerhaften Referenzformular wurden sämtliche 15 injizierten Mängel (von der veralteten 700px-Breite und dem aktivierten XIMA-Footer-Logo über fehlende Datenschutz-Klauseln und unzulässige Button-Labels bis hin zu fehlenden Status-Knoten und fehlenden Vorgangsnummern) lückenlos identifiziert.
    \item Beim vollkonformen Formular traten keinerlei Fehlalarme (\textit{False Positives}) auf.
\end{itemize}

\subsection{Ergebnisse am realen HWG-Bestand}
Die Auswertung der realen Bestandsformulare unterstreicht die hohe diagnostische Trennschärfe der erweiterten Registry v1.5.0:
\begin{itemize}
    \item Das Produktivformular \textit{Auslagenerstattung} erreicht einen Score von 41 Punkten. Positiv hervorzuheben ist, dass das XIMA-Logo im Footer deaktiviert wurde (\texttt{HWG-CD-03} bestanden), der Workflow strukturierte Statusknoten besitzt (\texttt{HWG-WF-01} bestanden) und eine ausführliche Eingangsbestätigungs-E-Mail existiert (\texttt{HWG-FEEDBACK-01} bestanden). Abzüge resultieren primär aus dem Fehlen einer DSGVO-Klausel im Formular, unvollständigen Upload-Beschränkungen, unmaskierten IBAN-/PLZ-Eingaben sowie dem Fehlen der Vorgangsnummer (\texttt{[\%\$PROJECT\_ALIAS\%]}) im E-Mail-Betreff (\texttt{HWG-WF-02}). Zudem löst die hohe Komplexität (3 Seiten, 49 Eingabefelder) die abzugsfreie Empfehlung \texttt{HWG-UX-02} zur Ergänzung einer Zwischenspeichern-Funktion aus.
    \item Der \textit{Antrag-Sprints} des ZFK (Score: 30 Punkte) verfügt zwar über funktionierende Statusknoten (\texttt{HWG-WF-01}) und eine Bestätigungs-E-Mail, weist jedoch im Frontend gravierende Mängel auf (fehlendes Logo, aktives XIMA-Herstellerbranding, fehlende Fieldsets und fehlende DSGVO-Klausel) und lässt die Vorgangs-ID in E-Mails vermissen (\texttt{HWG-WF-02}).
    \item Das interne \textit{Master-Formular} bestätigt mit 72 Punkten seine Eignung als Blaupause, offenbart jedoch bestehende Nachbesserungsbedarfe bezüglich 700px-Breite, HTML-Entities, unvalidierter PLZ-Felder und fehlender Vorgangsnummern-Referenz.
\end{itemize}"""

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_rep = replacement.replace('\r\n', '\n')

norm_text = norm_text.replace('v1.3.0', 'v1.5.0').replace('18 bewerteten', '20 bewerteten').replace('12 definierte', '15 definierte').replace('13 definierte', '15 definierte')

if norm_target in norm_text:
    norm_text = norm_text.replace(norm_target, norm_rep)
    with open('thesis/chapters/06_evaluation.tex', 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print("SUCCESS: Chapter 6 updated to v1.5.0")
else:
    print("ERROR: target not found in Chapter 6")
