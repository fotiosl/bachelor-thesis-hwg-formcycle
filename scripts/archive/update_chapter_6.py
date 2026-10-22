with open('thesis/chapters/06_evaluation.tex', 'r', encoding='utf-8') as f:
    text = f.read()

target = r"""\section{Quantitative Benchmark-Ergebnisse}
\label{sec:benchmark_ergebnisse}

Tabelle~\ref{tab:eval_results} fasst die Ergebnisse der automatisierten Compliance-Prüfung (Registry v1.3.0) über alle Testinstanzen zusammen:

\begin{table}[H]
\centering
\small
\begin{tabularx}{\textwidth}{lccccX}
\toprule
\textbf{Formular-Instanz} & \textbf{Typ} & \textbf{Score} & \textbf{Bestanden} & \textbf{Verstöße} & \textbf{Zentrale Befunde \& Empfehlungen} \\
\midrule
\textit{Synthetisch Konform} & Benchmark & 100 / 100 & 14 & 0 & Perfektes Referenzmuster \\
\textit{Synthetisch Fehlerhaft} & Benchmark & 0 / 100 & 1 & 13 & Alle 13 Injektionen erkannt \\
\midrule
\textit{Auslagenerstattung} & Real (Prod) & 44 / 100 & 6 & 8 & DSGVO, Uploads, IBAN unvalidiert; \textit{Empfehlung:} \texttt{HWG-UX-02} (3 S., 49 Felder) \\
\textit{Antrag-Sprints ZFK} & Real (Test) & 33 / 100 & 7 & 7 & Kein Logo, XIMA-Footer aktiv, keine Fieldsets, DSGVO; Workflow-Mail konform \\
\textit{Master-Formular} & Real (Admin) & 75 / 100 & 9 & 5 & 700px, HTML-Entities, PLZ gestreckt; \textit{Empfehlung:} \texttt{HWG-UX-02} (29 Felder) \\
\bottomrule
\end{tabularx}
\caption{Quantitative Evaluationsergebnisse der Compliance-Pipeline (Registry v1.3.0)}
\label{tab:eval_results}
\end{table}

\subsection{Analyse der Erkennungsleistung}
Am synthetischen Kontrollkorpus erreichte die Pipeline eine Erkennungsgenauigkeit (\textit{Accuracy}) von 100\,\%:
\begin{itemize}
    \item Beim fehlerhaften Referenzformular wurden sämtliche 13 injizierten Mängel (von der veralteten 700px-Breite und dem aktivierten XIMA-Footer-Logo über fehlende Datenschutz-Klauseln bis hin zum unzulässigen Button \enquote{Kritischer Fall}) lückenlos identifiziert.
    \item Beim vollkonformen Formular traten keinerlei Fehlalarme (\textit{False Positives}) auf.
\end{itemize}

\subsection{Ergebnisse am realen HWG-Bestand}
Die Auswertung der realen Bestandsformulare unterstreicht die hohe diagnostische Trennschärfe der Registry v1.3.0:
\begin{itemize}
    \item Das Produktivformular \textit{Auslagenerstattung} erreicht einen Score von 44 Punkten. Positiv hervorzuheben ist, dass das XIMA-Logo im Footer deaktiviert wurde (\texttt{HWG-CD-03} bestanden) und im hinterlegten Workflow eine ausführliche Eingangsbestätigungs-E-Mail (\texttt{FC\_EMAIL}) existiert (\texttt{HWG-FEEDBACK-01} bestanden). Abzüge resultieren primär aus dem Fehlen einer DSGVO-Klausel im Formular, fehlenden Formatbegrenzungen bei vier Upload-Feldern sowie unmaskierten IBAN-/PLZ-Eingaben. Zudem löst die hohe Komplexität (3 Seiten, 49 Eingabefelder) folgerichtig die abzugsfreie Empfehlung \texttt{HWG-UX-02} zur Ergänzung einer Zwischenspeichern-Funktion aus.
    \item Der \textit{Antrag-Sprints} des ZFK (Score: 33 Punkte) verfügt zwar ebenfalls über eine vorbildliche Workflow-Eingangsbestätigung per E-Mail (\texttt{HWG-FEEDBACK-01} bestanden), weist jedoch im Frontend gravierende Mängel auf: Es fehlt das Hochschul-Logo (\texttt{HWG-CD-02}), im Footer ist das Hersteller-Branding \enquote{Powered by XIMA Formcycle} aktiv (\texttt{HWG-CD-03}), und es fehlen sowohl semantische Fieldsets (\texttt{HWG-A11Y-01}) als auch der Datenschutz-Hinweis (\texttt{HWG-DSGVO-01}).
    \item Das interne \textit{Master-Formular} erreicht nach Bereinigung der Doppelbestrafung für HTML-Tags in kanonischen Stammdaten-Labels einen Score von 75 Punkten und bestätigt seine Rolle als solide strukturelle Blaupause, bei der lediglich die veraltete 700px-Breite, HTML-Entities in Labels und fehlende Regex-Validierungen für Postleitzahlen nachgeschärft werden müssen.
\end{itemize}"""

replacement = r"""\section{Quantitative Benchmark-Ergebnisse}
\label{sec:benchmark_ergebnisse}

Tabelle~\ref{tab:eval_results} fasst die Ergebnisse der automatisierten Compliance-Prüfung (Registry v1.4.0) über alle Testinstanzen zusammen:

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
\end{itemize}

\subsection{Validierung der Modell-Agnostik und Open-Source-Evaluation (Academic Cloud)}
\label{subsec:opensource_eval}
Um zu verifizieren, dass die Prompt-Architektur nicht auf ein spezifisches kommerzielles Modell (z.\,B. Google Gemini) überangepasst ist (\textit{Prompt Overfitting}), wurde die semantische Inferenzstufe zusätzlich mit modernen Open-Source-Modellen im Rahmen der \textit{Academic Cloud Chat AI} (GWDG) evaluiert. 

Die Ergebnisse bestätigen eine hohe Modell-Agnostik:
\begin{itemize}
    \item \textbf{Strikte Schema-Treue:} Die getesteten Open-Source-Modelle (wie Llama-3.3-70B und Qwen-2.5) folgten dem injizierten JSON-Ausgabeschema strikt ohne Abweichungen (\textit{Zero-Shot JSON Compliance}) und zeigten eine präzise logische Befolgung negativer Constraints.
    \item \textbf{Datensouveränität für den Hochschulbetrieb:} Der erfolgreiche Betrieb auf universitärer Open-Source-Infrastruktur belegt, dass die automatisierte Compliance-Prüfung an der HWG Ludwigshafen vollständig datenschutzkonform ohne Abhängigkeit von US-basierten Cloud-APIs betrieben werden kann.
\end{itemize}"""

norm_text = text.replace('\r\n', '\n')
norm_target = target.replace('\r\n', '\n')
norm_rep = replacement.replace('\r\n', '\n')

if norm_target in norm_text:
    norm_text = norm_text.replace(norm_target, norm_rep)
    with open('thesis/chapters/06_evaluation.tex', 'w', encoding='utf-8') as f:
        f.write(norm_text)
    print("SUCCESS: Chapter 6 updated")
else:
    print("ERROR: target not found in Chapter 6")
