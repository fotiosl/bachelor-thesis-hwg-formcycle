import docx
from docx.shared import Inches, Pt, RGBColor
from docx.enum.text import WD_ALIGN_PARAGRAPH
from docx.enum.style import WD_STYLE_TYPE

def create_expose_docx(output_path="docs/EXPOSE_HWG_Ludwigshafen.docx"):
    doc = docx.Document()
    
    # Page Setup DIN A4, 2.5 cm margins
    for section in doc.sections:
        section.top_margin = Inches(1)
        section.bottom_margin = Inches(1)
        section.left_margin = Inches(1)
        section.right_margin = Inches(1)
        
    # Set default style font
    normal_style = doc.styles['Normal']
    normal_style.font.name = 'Calibri'
    normal_style.font.size = Pt(11)
    normal_style.font.color.rgb = RGBColor(0x22, 0x22, 0x22)
    normal_style.paragraph_format.line_spacing = 1.2
    normal_style.paragraph_format.space_after = Pt(6)
    normal_style.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY

    # Title
    p_title = doc.add_paragraph()
    p_title.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_title.paragraph_format.space_after = Pt(12)
    run_title = p_title.add_run("Konzeption eines einheitlichen Formular-Standards für die HWG Ludwigshafen und prototypische Umsetzung einer KI-gestützten Compliance-Prüfung in Formcycle")
    run_title.font.size = Pt(16)
    run_title.font.bold = True
    run_title.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # Subtitle / Metadata
    p_meta = doc.add_paragraph()
    p_meta.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
    p_meta.paragraph_format.space_after = Pt(18)
    run_meta = p_meta.add_run(
        "Exposé zur Bachelorarbeit\n"
        "Autor: Fotios Logaras | Studiengang: Wirtschaftsinformatik\n"
        "Erstprüfer: Prof. Dr. Simon Kloker | Hochschule für Wirtschaft und Gesellschaft Ludwigshafen\n"
        "Bearbeitungszeitraum: 08.10.2026 – 07.12.2026 (Abgabefrist: 07.12.2026)"
    )
    run_meta.font.size = Pt(9.5)
    run_meta.font.italic = True
    run_meta.font.color.rgb = RGBColor(0x55, 0x55, 0x55)

    def add_h2(title):
        h = doc.add_paragraph()
        h.paragraph_format.space_before = Pt(12)
        h.paragraph_format.space_after = Pt(4)
        h.paragraph_format.keep_with_next = True
        r = h.add_run(title)
        r.font.size = Pt(13)
        r.font.bold = True
        r.font.color.rgb = RGBColor(0x00, 0x33, 0x66)
        return h

    def add_body(text):
        p = doc.add_paragraph()
        p.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
        p.paragraph_format.space_after = Pt(6)
        r = p.add_run(text)
        return p

    # 1. Problemstellung
    add_h2("Problemstellung & Motivation")
    add_body(
        "An der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen (HWG) fehlt derzeit ein verbindlicher "
        "Gestaltungs- und Strukturstandard für Online-Formulare, um den angestrebten vollständigen Übergang auf das "
        "Formular-Management-System Formcycle standardisiert zu vollziehen. Bestehende Papier- und PDF-Vorlagen müssen "
        "dabei inhaltlich konsistent und nutzerzentriert in die digitale Formcycle-Struktur überführt werden. Eine "
        "Analyse der bereits implementierten Formulare verdeutlicht jedoch deutliche UX-Inkonsistenzen: Komponenten, "
        "Benennungskonventionen und die visuelle Benutzerführung variieren regelmäßig. Für die Anwendenden führt dies "
        "zu Reibungsverlusten und Verwirrung bei der Dateneingabe, während für die Erstellenden klare Designvorgaben "
        "fehlen, was heterogene Insellösungen und technische Workarounds begünstigt. Dieser Mangel an Standardisierung "
        "erschwert die langfristige Wartbarkeit erheblich, da nachträgliche Anpassungen unverhältnismäßig viel "
        "Einarbeitungszeit erfordern oder im Extremfall eine vollständige Neugestaltung erzwingen."
    )

    # 2. Stand der Literatur
    add_h2("Stand der Literatur und Forschungslücke")
    add_body(
        "Die automatisierte Inspektion von Benutzeroberflächen auf Basis von Usability-Heuristiken und Gestaltungsrichtlinien "
        "hat durch die Integration von Large Language Models (LLMs) einen tiefgreifenden technologischen Wandel erfahren. "
        "Bisherige empirische Untersuchungen belegen jedoch deutliche Grenzen unstrukturierter Ansätze: Werden vortrainierte "
        "Modelle lediglich über naive Standard-Prompts mit der heuristischen Evaluation beauftragt, identifizieren sie im "
        "Vergleich zu menschlichen Fachleuten nur rund 21 % der tatsächlichen Usability-Probleme und neigen zu Fehlalarmen "
        "(Guerino et al., 2025). Ergänzend zeigen Zhong et al. (2025), dass LLMs zwar im Erkennen von Layout-Auffälligkeiten "
        "solide Ergebnisse erzielen, jedoch bei domänenspezifischen Komponenten und komplexen Interaktionsabfolgen ohne "
        "formalisierten Kontext scheitern. Um eine verlässliche Regelkonformität zu gewährleisten, weisen Cha et al. (2026) nach, "
        "dass registry-basierte Context-Engineering-Strategien zur Operationalisierung von Design-Systemen bei LLM-gestützten "
        "Schnittstellenprüfungen eine Compliance von über 95 % erzielen können. Hinsichtlich des operativen Feedback-Workflows "
        "zwischen Prüfsystem und UX-Designern demonstrieren Duan et al. (2024), dass automatisiertes Usability-Feedback besonders "
        "wirksam ist, wenn es direkt in die gewohnte Arbeitsumgebung eingebettet und als handlungsorientierte Optimierungsempfehlung "
        "aufbereitet wird. Gleichzeitig offenbaren aktuelle Studien, dass Sprachmodelle bei der Zuweisung objektiver Schweregrade "
        "(Severity Ratings) statistisch instabil urteilen, weshalb semantische Erkennung und quantitative Score-Kalkulation "
        "sinnvoll entkoppelt werden sollten (Guerino et al., 2025). In der aktuellen Forschung stehen diese Ansätze meist isoliert "
        "nebeneinander und beschränken sich vorwiegend auf abstrakte Labor-Mockups. Seither haben sich die Modelle jedoch maßgeblich "
        "weiterentwickelt, was eine Forschungslücke hinsichtlich einer praxistauglichen Synthese eröffnet: Es fehlt an einem Ansatz, "
        "der eine empirische Ist-Analyse gewachsener Hochschulformulare mit einer formalen Standarddefinition vereint und diesen "
        "Standard als registry-gestützte, hybride LLM-Prüfpipeline unmittelbar in ein Enterprise-System wie Formcycle integriert."
    )

    # 3. Forschungsfrage & Ziel
    add_h2("Forschungsfrage(n), Zielsetzung und Beitrag")
    add_body(
        "Das primäre Ziel der Arbeit besteht darin, einen hochschulweiten Governance-Leitfaden sowie einen funktionsfähigen "
        "Software-Prototypen zur automatisierten Compliance-Evaluation in der Formcycle-Infrastruktur zu entwickeln. Hierbei gilt "
        "es zu untersuchen, welche Gestaltungsstandards an der HWG bestehen müssen, wie eine maschinenlesbare Komponenten- und "
        "Regel-Registry aufgebaut sein muss und wie ein deterministisches Berechnungsmodell einen verlässlichen Compliance-Score "
        "ohne stochastische Verzerrungen liefert. Der Nutzen dieser Arbeit liegt darin, ein nachhaltiges Werkzeug zur Einhaltung "
        "von Formularstandards, digitaler Barrierefreiheit und Corporate Design an der HWG bereitzustellen."
    )
    p_rq = doc.add_paragraph()
    p_rq.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.JUSTIFY
    p_rq.paragraph_format.left_indent = Inches(0.4)
    p_rq.paragraph_format.right_indent = Inches(0.4)
    p_rq.paragraph_format.space_before = Pt(4)
    p_rq.paragraph_format.space_after = Pt(8)
    r_rq = p_rq.add_run("Zentrale Forschungsfrage:\n»Wie lässt sich ein einheitlicher Gestaltungsstandard für HWG-Formulare entwickeln und über KI automatisiert in Formcycle prüfen?«")
    r_rq.font.bold = True
    r_rq.font.italic = True
    r_rq.font.color.rgb = RGBColor(0x00, 0x33, 0x66)

    # 4. Methodik
    add_h2("Methodisches Vorgehen und Datenbasis")
    add_body(
        "Die Arbeit folgt einem gestaltungsorientierten Ansatz (Design Science Research) und gliedert sich in eine Analyse-, "
        "Konzeptions-, Implementierungs- und Evaluationsphase. Zunächst wird eine systematische Bestandsaufnahme durchgeführt: "
        "Hierfür werden ausgewählte PDF-, Papier- und Formcycle-Formulare der HWG analysiert, um redundante Felder, Usability-Defizite "
        "und Barrierefreiheitsmängel zu identifizieren und in Gegenüberstellungen visuell aufzubereiten. Auf dieser Basis wird ein "
        "verbindlicher Leitfaden definiert, der Vorgaben zu Typografie, Abständen, Pflichtfeldlogiken, digitaler Barrierefreiheit "
        "(WCAG 2.1) und Benennungskonventionen bündelt. Im nächsten Schritt wird dieses Regelwerk in eine maschinenlesbare JSON-Registry "
        "überführt, die als strukturierter Kontextanker für das Context-Engineering dient. Darauf aufbauend wird eine Middleware "
        "realisiert, welche die JSON-Struktur des Formulars aus Formcycle extrahiert, zur semantischen Mängelprüfung an ein LLM übergibt "
        "und den finalen Compliance-Score über einen deterministischen Algorithmus berechnet. Abschließend wird das System anhand "
        "synthetisch erstellter Testformulare in Benchmark-Läufen auf Erkennungsgenauigkeit und Fehlalarme evaluiert. Ein nachgelagerter "
        "Praxistest mit formularerstellenden Mitarbeitenden der HWG erfasst die Usability und Nachvollziehbarkeit des Feedbacks über "
        "einen standardisierten Fragebogen."
    )

    # 5. Zeitplan & Gliederung
    add_h2("Zeitplan und vorläufige Gliederung")
    add_body("Der Bearbeitungszeitraum erstreckt sich über 8,5 Wochen mit verbindlicher Abgabefrist am 07.12.2026:")

    milestones = [
        ("Woche 1–2 (08.10. – 18.10.2026)", "Abschluss der Literaturarbeit; Analyse des HWG-Formularbestands; Konzeption des Master-Regelwerks."),
        ("Woche 3–4 (19.10. – 01.11.2026)", "Formalisierung der JSON-Registry; Meilenstein 1: Erstellung der synthetischen, fehlerhaften Testformulare (Ground Truth)."),
        ("Woche 5–6 (02.11. – 15.11.2026)", "Prototypische Umsetzung der Formcycle-Middleware und Prüfpipeline; Meilenstein 2: Fertigstellung des Evaluationsfragebogens."),
        ("Woche 7 (16.11. – 22.11.2026)", "Durchführung der Benchmark-Läufe; Praxistests und Fragebogenerhebung mit Mitarbeitenden; Auswertung der Ergebnisse."),
        ("Woche 8 (23.11. – 29.11.2026)", "Intensive Schreibphase; Zusammenführung der Kapitel und Vorbereitung des Rohberichts."),
        ("Woche 9 (30.11. – 07.12.2026)", "Vorabkorrektur und Feedback-Einarbeitung; finale Formatierung (APA 7th, Layout); Abgabe am 07.12.2026.")
    ]
    for w, desc in milestones:
        p_m = doc.add_paragraph()
        p_m.paragraph_format.left_indent = Inches(0.2)
        p_m.paragraph_format.space_after = Pt(3)
        r_w = p_m.add_run(f"• {w}: ")
        r_w.font.bold = True
        p_m.add_run(desc)

    p_gl_head = doc.add_paragraph()
    p_gl_head.paragraph_format.space_before = Pt(8)
    p_gl_head.paragraph_format.space_after = Pt(2)
    p_gl_head.paragraph_format.keep_with_next = True
    r_gl = p_gl_head.add_run("Vorläufige Gliederung:")
    r_gl.font.bold = True

    sections = [
        "1. Einleitung und Problemstellung (Ausgangssituation, Forschungsfragen, DSR-Vorgehen)",
        "2. Theoretischer Hintergrund und Stand der Technik (Usability-Standards, Heuristik-Prüfung, Registry-Context-Engineering, Hybride Scoring-Architekturen)",
        "3. Empirische Ist-Analyse des HWG-Formularbestands (Methodik, Audit, Vorher-Nachher-Vergleich, Kernanforderungen)",
        "4. Konzeption des Formular-Standards und der Prüf-Registry (Gestaltungsrichtlinien, maschinenlesbare JSON-Registry)",
        "5. Prototypische Implementierung der Compliance-Prüfpipeline (Datenextraktion, Prompt-Design, deterministisches Scoring, Feedback-Visualisierung)",
        "6. Empirische Evaluation und Diskussion (Quantitative Benchmarks, qualitative Nutzertestung, Validitätsbedrohungen)",
        "7. Fazit und Ausblick (Zusammenfassung, Handlungsempfehlungen für die HWG, Ausblick)"
    ]
    for sec in sections:
        p_s = doc.add_paragraph()
        p_s.paragraph_format.left_indent = Inches(0.2)
        p_s.paragraph_format.space_after = Pt(2)
        p_s.add_run(sec)

    # 6. Verwertung
    add_h2("Verwertungsstrategie")
    add_body(
        "Zu den zentralen Adressaten der Bachelorarbeit zählen die Hochschulleitung, das Qualitätsmanagement sowie die "
        "Formcycle-Administration der HWG Ludwigshafen. Durch die Standardisierung wird ein konsistenter, barrierefreier "
        "Außenauftritt sichergestellt und der IT-Support nachhaltig entlastet, da fehleranfällige Insellösungen entfallen. "
        "Der entwickelte Leitfaden soll im Intranet als verbindliches Referenzwerk bereitgestellt werden und insbesondere "
        "bei der Einarbeitung neuer Mitarbeitender als verlässliche Orientierung dienen. Das softwarebasierte Prüfwerkzeug "
        "liefert direkt umsetzbare Optimierungsempfehlungen bei der Formularerstellung und wird durch eine verständliche "
        "Kurzanleitung für das Verwaltungspersonal ergänzt, um eine reibungslose Anwendung in der Praxis zu gewährleisten."
    )

    # 7. Literaturverzeichnis
    add_h2("Literaturverzeichnis (APA 7th Edition)")
    
    bib_entries = [
        "Cha, S., Jo, S., Shin, J., & Seo, K. (2026). Design System-Compliant User Interface Generation with LLM Agents: A Comparative Study of Context Engineering Strategies. In Extended Abstracts of the 2026 CHI Conference on Human Factors in Computing Systems (CHI EA '26). Association for Computing Machinery. https://doi.org/10.1145/3772363.3798616",
        "Duan, P., Warner, J., Li, Y., & Hartmann, B. (2024). Generating Automatic Feedback on UI Mockups with Large Language Models. In Proceedings of the 2024 CHI Conference on Human Factors in Computing Systems (CHI '24), Article 872, 1–20. Association for Computing Machinery. https://doi.org/10.1145/3613904.3642782",
        "Guerino, G. C., Rodrigues, L., Capeleti, B., Mello, R. F., Freire, A., & Zaina, L. (2025). Can GPT-4o Evaluate Usability Like Human Experts? A Comparative Study on Issue Identification in Heuristic Evaluation. In Human-Computer Interaction – INTERACT 2025 (Lecture Notes in Computer Science, Vol. 15286, pp. 381–402). Springer. https://arxiv.org/abs/2506.16345",
        "Zhong, R., McDonald, D. W., & Hsieh, G. (2025). Synthetic Heuristic Evaluation: A Comparison between AI- and Human-Powered Usability Evaluation. arXiv preprint. https://doi.org/10.48550/arXiv.2507.02306"
    ]
    for b in bib_entries:
        p_b = doc.add_paragraph()
        p_b.paragraph_format.alignment = WD_ALIGN_PARAGRAPH.LEFT
        p_b.paragraph_format.left_indent = Inches(0.4)
        p_b.paragraph_format.first_line_indent = Inches(-0.4) # Hanging indent for APA 7th
        p_b.paragraph_format.space_after = Pt(6)
        r_b = p_b.add_run(b)
        r_b.font.size = Pt(10)

    # 8. Dokumentation der KI-Nutzung
    add_h2("Dokumentation der KI-Nutzung (nach Leitfaden HWG Ludwigshafen)")
    add_body(
        "Gemäß den Betreuungsrichtlinien von Prof. Dr. Simon Kloker und den Grundsätzen der guten wissenschaftlichen Praxis "
        "der HWG Ludwigshafen wird die KI-Unterstützung transparent dokumentiert:"
    )
    ki_notes = [
        ("Problemstellung & Motivation:", "Vom Verfasser selbst formuliert, sprachlich und stilistisch mit KI überarbeitet."),
        ("Stand der Literatur & Forschungslücke:", "KI-gestützte Literaturanalyse und Formulierung der Synthese anhand der verifizierten Primärquellen."),
        ("Forschungsfrage & Zielsetzung:", "Vom Verfasser selbst formuliert, auf Prägnanz geschärft."),
        ("Methodisches Vorgehen & Datenbasis:", "Vom Verfasser selbst konzipiert (DSR-Framework), methodisch strukturiert."),
        ("Zeitplan & Gliederung:", "Konzipiert anhand der Prüfungsfrist 07.12.2026 und Betreuer-Meilensteine, tabellarisch aufbereitet."),
        ("Verwertungsstrategie:", "Vom Verfasser formuliert, an HWG-Bedarfe angepasst."),
        ("Verwendete KI-Systeme:", "Google Gemini 3.8 Flash (Thinking / Research) zur Rechercheunterstützung, Formulierungshilfe und Quellensynthese.")
    ]
    for k, v in ki_notes:
        p_k = doc.add_paragraph()
        p_k.paragraph_format.left_indent = Inches(0.2)
        p_k.paragraph_format.space_after = Pt(3)
        r_k = p_k.add_run(f"• {k} ")
        r_k.font.bold = True
        p_k.add_run(v)

    doc.save(output_path)
    print(f"Successfully generated: {output_path}")

if __name__ == "__main__":
    create_expose_docx()
