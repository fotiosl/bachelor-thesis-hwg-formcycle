import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))


def generate_dashboard():
    with open("data/rules/rules_registry.json", "r", encoding="utf-8") as f:
        registry = json.load(f)

    from test_rule_engine import evaluate_form

    presets = {
        "synth_comp": {
            "name": "Synthetisches Referenzformular (Best-Practice)",
            "file": "data/test_forms/synthetic_compliant_form.json",
            "eval": evaluate_form("data/test_forms/synthetic_compliant_form.json", registry),
        },
        "synth_noncomp": {
            "name": "Synthetisches Negativformular (Worst-Case)",
            "file": "data/test_forms/synthetic_noncompliant_form.json",
            "eval": evaluate_form("data/test_forms/synthetic_noncompliant_form.json", registry),
        },
        "auslagen": {
            "name": "Reales Formular: Auslagenerstattung (Finanzen)",
            "file": "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
            "eval": evaluate_form("data/raw_forms/prod/Auslagenerstattung _20260929.xfp", registry),
        },
        "sprints": {
            "name": "Reales Formular: Antrag-Sprints Drittmittel (ZFK)",
            "file": "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
            "eval": evaluate_form(
                "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
                registry,
            ),
        },
        "master": {
            "name": "Reales Formular: Master-Formular (Campus Management)",
            "file": "data/raw_forms/test/adminformulare/Master-Formular.xfp",
            "eval": evaluate_form("data/raw_forms/test/adminformulare/Master-Formular.xfp", registry),
        },
    }

    registry_json = json.dumps(registry, ensure_ascii=False)
    presets_json = json.dumps(presets, ensure_ascii=False)

    html_content = f"""<!DOCTYPE html>
<html lang="de">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>HWG Ludwigshafen – Formcycle Compliance Checker</title>
    <link rel="preconnect" href="https://fonts.googleapis.com">
    <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
    <link href="https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700;800&family=JetBrains+Mono:wght@400;500&display=swap" rel="stylesheet">
    <script src="vendor/jszip.min.js"></script>
    <script>
        if (typeof JSZip === 'undefined') {{
            document.write('<script src="https://cdnjs.cloudflare.com/ajax/libs/jszip/3.10.1/jszip.min.js"><\\/script>');
        }}
    </script>
    <style>
        :root {{
            --hwg-blue: #003366;
            --hwg-blue-light: #0d4b8f;
            --hwg-blue-subtle: #f0f4f9;
            --hwg-red: #b41414;
            --hwg-red-subtle: #fdf2f2;
            --hwg-gold: #c68a18;
            --hwg-gold-subtle: #fefcf3;
            --hwg-green: #1a7f37;
            --hwg-green-subtle: #f0f9f2;
            --slate-50: #f8fafc;
            --slate-100: #f1f5f9;
            --slate-200: #e2e8f0;
            --slate-300: #cbd5e1;
            --slate-600: #475569;
            --slate-700: #334155;
            --slate-800: #1e293b;
            --slate-900: #0f172a;
            --shadow-sm: 0 1px 2px 0 rgb(0 0 0 / 0.05);
            --shadow: 0 4px 6px -1px rgb(0 0 0 / 0.1), 0 2px 4px -2px rgb(0 0 0 / 0.1);
            --radius-md: 8px;
            --radius-lg: 12px;
            --radius-xl: 16px;
        }}

        * {{
            box-sizing: border-box;
            margin: 0;
            padding: 0;
        }}

        body {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif;
            background-color: var(--slate-50);
            color: var(--slate-800);
            line-height: 1.5;
            min-height: 100vh;
        }}

        header {{
            background: linear-gradient(135deg, var(--hwg-blue) 0%, #001f3f 100%);
            color: white;
            padding: 20px 32px;
            box-shadow: var(--shadow);
            border-bottom: 4px solid var(--hwg-red);
        }}

        .header-container {{
            max-width: 1200px;
            margin: 0 auto;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 16px;
        }}

        .brand-section {{
            display: flex;
            align-items: center;
            gap: 16px;
        }}

        .brand-badge {{
            background: rgba(255, 255, 255, 0.12);
            border: 1px solid rgba(255, 255, 255, 0.2);
            padding: 8px 14px;
            border-radius: var(--radius-md);
            font-weight: 700;
            letter-spacing: 0.5px;
            font-size: 14px;
        }}

        .brand-text h1 {{
            font-size: 21px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}

        .brand-text p {{
            font-size: 13px;
            color: rgba(255, 255, 255, 0.82);
        }}

        .header-actions {{
            display: flex;
            gap: 12px;
        }}

        .btn {{
            display: inline-flex;
            align-items: center;
            gap: 8px;
            padding: 9px 16px;
            border-radius: var(--radius-md);
            font-size: 13px;
            font-weight: 600;
            cursor: pointer;
            transition: all 0.15s ease;
            border: 1px solid transparent;
            text-decoration: none;
        }}

        .btn-light {{
            background: rgba(255, 255, 255, 0.15);
            color: white;
            border-color: rgba(255, 255, 255, 0.3);
        }}

        .btn-light:hover {{ background: rgba(255, 255, 255, 0.25); }}

        .btn-primary {{
            background: var(--hwg-blue);
            color: white;
        }}

        .btn-primary:hover {{ background: var(--hwg-blue-light); }}

        .btn-print {{
            background: white;
            color: var(--hwg-blue);
            font-weight: 600;
        }}

        .btn-print:hover {{ background: var(--slate-100); }}

        main {{
            max-width: 1200px;
            margin: 24px auto;
            padding: 0 24px;
        }}

        .card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            box-shadow: var(--shadow-sm);
            margin-bottom: 20px;
            overflow: hidden;
        }}

        .card-header {{
            padding: 16px 24px;
            border-bottom: 1px solid var(--slate-200);
            background: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
            flex-wrap: wrap;
            gap: 8px;
        }}

        .card-header h2 {{
            font-size: 16px;
            font-weight: 700;
            color: var(--slate-900);
        }}

        .card-body {{ padding: 20px 24px; }}

        .preset-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 16px;
        }}

        .preset-btn {{
            background: var(--slate-50);
            border: 1.5px solid var(--slate-200);
            border-radius: var(--radius-lg);
            padding: 11px 13px;
            text-align: left;
            cursor: pointer;
            transition: all 0.2s ease;
        }}

        .preset-btn:hover {{
            border-color: var(--hwg-blue);
            background: var(--hwg-blue-subtle);
            transform: translateY(-1px);
        }}

        .preset-btn.active {{
            border-color: var(--hwg-blue);
            background: var(--hwg-blue-subtle);
            box-shadow: 0 0 0 2px rgba(0, 51, 102, 0.15);
        }}

        .preset-btn-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--slate-900);
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            justify-content: space-between;
            gap: 6px;
        }}

        .preset-btn-desc {{
            font-size: 11px;
            color: var(--slate-600);
        }}

        .preset-score-pill {{
            font-size: 11px;
            font-weight: 700;
            padding: 2px 7px;
            border-radius: 999px;
            white-space: nowrap;
        }}

        .score-good {{ background: #dcfce7; color: var(--hwg-green); }}
        .score-mid {{ background: #fef9c3; color: #854d0e; }}
        .score-poor {{ background: #fee2e2; color: var(--hwg-red); }}

        .dropzone {{
            border: 2px dashed var(--slate-300);
            border-radius: var(--radius-lg);
            padding: 20px;
            text-align: center;
            background: var(--slate-50);
            transition: all 0.2s ease;
            cursor: pointer;
        }}

        .dropzone:hover, .dropzone.dragover {{
            border-color: var(--hwg-blue);
            background: var(--hwg-blue-subtle);
        }}

        .dropzone p {{
            font-size: 12px;
            color: var(--slate-600);
            margin-top: 4px;
        }}

        /* LLM Config Box */
        details.llm-config-box {{
            margin-top: 14px;
            border: 1px solid var(--slate-200);
            border-radius: var(--radius-md);
            background: var(--slate-50);
            padding: 10px 14px;
        }}

        details.llm-config-box summary {{
            font-size: 13px;
            font-weight: 600;
            color: var(--hwg-blue);
            cursor: pointer;
            user-select: none;
        }}

        .llm-config-grid {{
            display: grid;
            grid-template-columns: 1.4fr 1fr 1.2fr auto;
            gap: 10px;
            margin-top: 12px;
            align-items: end;
        }}

        @media (max-width: 900px) {{
            .llm-config-grid {{ grid-template-columns: 1fr; }}
        }}

        .llm-field label {{
            display: block;
            font-size: 11px;
            font-weight: 600;
            color: var(--slate-700);
            margin-bottom: 4px;
        }}

        .llm-field input {{
            width: 100%;
            padding: 7px 10px;
            font-size: 12px;
            border: 1px solid var(--slate-300);
            border-radius: 6px;
            font-family: 'JetBrains Mono', monospace;
        }}

        /* LLM Warning / Status Banner */
        .llm-banner {{
            border-radius: var(--radius-lg);
            padding: 14px 18px;
            margin-bottom: 20px;
            font-size: 13px;
            line-height: 1.5;
            display: flex;
            align-items: flex-start;
            gap: 12px;
        }}

        .llm-banner-warn {{
            background: #fffbeb;
            border: 1.5px solid #f59e0b;
            color: #78350f;
        }}

        .llm-banner-ok {{
            background: var(--hwg-green-subtle);
            border: 1.5px solid #86efac;
            color: #14532d;
        }}

        .dashboard-grid {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }}

        @media (max-width: 860px) {{
            .dashboard-grid {{ grid-template-columns: 1fr; }}
        }}

        .score-card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            padding: 20px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: var(--shadow-sm);
        }}

        .gauge-container {{
            position: relative;
            width: 160px;
            height: 160px;
            margin-bottom: 12px;
        }}

        .gauge-svg {{
            transform: rotate(-90deg);
            width: 100%;
            height: 100%;
        }}

        .gauge-bg {{
            fill: none;
            stroke: var(--slate-200);
            stroke-width: 12;
        }}

        .gauge-meter {{
            fill: none;
            stroke-width: 12;
            stroke-linecap: round;
            stroke-dasharray: 440;
            stroke-dashoffset: 440;
            transition: stroke-dashoffset 0.8s cubic-bezier(0.4, 0, 0.2, 1), stroke 0.5s ease;
        }}

        .gauge-text {{
            position: absolute;
            top: 50%;
            left: 50%;
            transform: translate(-50%, -50%);
            display: flex;
            flex-direction: column;
            align-items: center;
        }}

        .gauge-value {{
            font-size: 38px;
            font-weight: 800;
            color: var(--slate-900);
            line-height: 1;
            letter-spacing: -1px;
        }}

        .gauge-label {{
            font-size: 12px;
            color: var(--slate-600);
            font-weight: 500;
            margin-top: 4px;
        }}

        .verdict-badge {{
            display: inline-block;
            padding: 6px 14px;
            border-radius: 999px;
            font-size: 12px;
            font-weight: 700;
            margin-top: 6px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(175px, 1fr));
            gap: 14px;
        }}

        .stat-card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            padding: 18px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .stat-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 10px;
        }}

        .stat-title {{
            font-size: 13px;
            font-weight: 600;
            color: var(--slate-600);
        }}

        .stat-icon {{
            width: 28px;
            height: 28px;
            border-radius: 8px;
            display: flex;
            align-items: center;
            justify-content: center;
            font-size: 14px;
            font-weight: 700;
        }}

        .icon-critical {{ background: var(--hwg-red-subtle); color: var(--hwg-red); }}
        .icon-major {{ background: #fff7ed; color: #ea580c; }}
        .icon-minor {{ background: var(--hwg-gold-subtle); color: var(--hwg-gold); }}
        .icon-passed {{ background: var(--hwg-green-subtle); color: var(--hwg-green); }}

        .stat-value {{
            font-size: 32px;
            font-weight: 800;
            color: var(--slate-900);
            line-height: 1;
        }}

        .stat-sub {{
            font-size: 12px;
            color: var(--slate-600);
            margin-top: 6px;
        }}

        .filter-bar {{
            display: flex;
            gap: 8px;
            margin-bottom: 16px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .filter-pill {{
            background: white;
            border: 1px solid var(--slate-300);
            border-radius: 999px;
            padding: 6px 14px;
            font-size: 12px;
            font-weight: 600;
            color: var(--slate-700);
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .filter-pill:hover {{ background: var(--slate-100); }}

        .filter-pill.active {{
            background: var(--hwg-blue);
            color: white;
            border-color: var(--hwg-blue);
        }}

        .rules-list {{
            display: flex;
            flex-direction: column;
            gap: 12px;
        }}

        .rule-card {{
            background: white;
            border-radius: var(--radius-lg);
            border: 1px solid var(--slate-200);
            padding: 18px 22px;
            box-shadow: var(--shadow-sm);
            transition: all 0.15s ease;
        }}

        .rule-card:hover {{
            border-color: var(--slate-300);
            box-shadow: var(--shadow);
        }}

        .rule-card.violation-critical {{ border-left: 5px solid var(--hwg-red); }}
        .rule-card.violation-major {{ border-left: 5px solid #ea580c; }}
        .rule-card.violation-minor {{ border-left: 5px solid var(--hwg-gold); }}
        .rule-card.violation-recommendation {{ border-left: 5px solid var(--hwg-blue); }}
        .rule-card.rule-passed {{ border-left: 5px solid var(--hwg-green); opacity: 0.92; }}
        .rule-card.rule-unverified {{
            border-left: 5px solid #d97706;
            background: #fffdf7;
        }}

        .rule-top {{
            display: flex;
            justify-content: space-between;
            align-items: flex-start;
            gap: 12px;
            margin-bottom: 10px;
        }}

        .rule-id-name {{
            display: flex;
            align-items: center;
            gap: 10px;
            flex-wrap: wrap;
        }}

        .rule-id {{
            font-family: 'JetBrains Mono', monospace;
            font-size: 12px;
            font-weight: 700;
            background: var(--slate-100);
            color: var(--slate-800);
            padding: 3px 8px;
            border-radius: 4px;
        }}

        .rule-stage-tag {{
            font-size: 11px;
            font-weight: 600;
            color: var(--slate-600);
            background: var(--slate-100);
            padding: 2px 7px;
            border-radius: 4px;
        }}

        .rule-name {{
            font-size: 15px;
            font-weight: 700;
            color: var(--slate-900);
        }}

        .badge {{
            display: inline-flex;
            align-items: center;
            padding: 4px 10px;
            border-radius: 999px;
            font-size: 11px;
            font-weight: 700;
            text-transform: uppercase;
            letter-spacing: 0.4px;
            white-space: nowrap;
        }}

        .badge-critical {{ background: var(--hwg-red-subtle); color: var(--hwg-red); }}
        .badge-major {{ background: #fff7ed; color: #ea580c; }}
        .badge-minor {{ background: var(--hwg-gold-subtle); color: #854d0e; }}
        .badge-recommendation {{ background: var(--hwg-blue-subtle); color: var(--hwg-blue); }}
        .badge-passed {{ background: var(--hwg-green-subtle); color: var(--hwg-green); }}
        .badge-unverified {{
            background: #fef3c7;
            color: #92400e;
            border: 1px solid #f59e0b;
        }}

        .rule-message {{
            font-size: 14px;
            color: var(--slate-800);
            margin-bottom: 12px;
            line-height: 1.5;
        }}

        .remediation-box {{
            background: var(--slate-50);
            border: 1px solid var(--slate-200);
            border-radius: var(--radius-md);
            padding: 12px 16px;
            margin-top: 10px;
        }}

        .remediation-title {{
            font-size: 12px;
            font-weight: 700;
            color: var(--hwg-blue);
            text-transform: uppercase;
            letter-spacing: 0.5px;
            margin-bottom: 4px;
            display: flex;
            align-items: center;
            gap: 6px;
        }}

        .remediation-text {{
            font-size: 13px;
            color: var(--slate-700);
            white-space: pre-line;
            line-height: 1.5;
        }}

        .rationale-text {{
            font-size: 12px;
            color: var(--slate-600);
            margin-top: 8px;
            font-style: italic;
        }}

        @media print {{
            header, .card:first-of-type, .filter-bar, .btn-print {{
                display: none !important;
            }}
            body {{ background: white; color: black; }}
            main {{ margin: 0; padding: 0; max-width: 100%; }}
            .rule-card {{
                page-break-inside: avoid;
                border: 1px solid #ccc;
                box-shadow: none;
                margin-bottom: 12px;
            }}
            .print-header {{
                display: block !important;
                margin-bottom: 20px;
                border-bottom: 2px solid #003366;
                padding-bottom: 12px;
            }}
        }}

        .print-header {{ display: none; }}
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <div class="brand-section">
                <div class="brand-badge">HWG LU</div>
                <div class="brand-text">
                    <h1>Formcycle Compliance Checker</h1>
                    <p>Hybrides Governance-, Usability- &amp; Barrierefreiheits-Audit (Registry v1.5.0)</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn btn-print" onclick="window.print()">
                    Prüfbericht drucken / PDF
                </button>
                <button class="btn btn-light" onclick="exportAuditJSON()">
                    JSON-Audit
                </button>
            </div>
        </div>
    </header>

    <main>
        <div class="print-header">
            <h2>Hochschule für Wirtschaft und Gesellschaft Ludwigshafen</h2>
            <h3>Formcycle Compliance- und Barrierefreiheits-Prüfbericht</h3>
            <p id="printMeta">Formular: - | Datum: <span id="printDate"></span> | Registry v1.5.0</p>
        </div>

        <!-- Benchmark Presets & Ingestion -->
        <div class="card">
            <div class="card-header">
                <h2>1. Formular-Auswahl, In-Memory-Ingestion (.xfp / .json) &amp; KI-API</h2>
                <span style="font-size: 12px; font-weight: 600; color: var(--hwg-blue);">22 Governance-Regeln aktiv (15 AST · 7 KI/Hybrid)</span>
            </div>
            <div class="card-body">
                <div style="font-size: 13px; font-weight: 600; color: var(--slate-700); margin-bottom: 8px;">
                    Benchmark-Formulare der HWG Ludwigshafen auswählen:
                </div>
                <div class="preset-grid" id="presetGrid"></div>

                <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
                    <input type="file" id="fileInput" accept=".json,.xfp" style="display: none" onchange="handleFileUpload(event)">
                    <div style="font-size: 14px; font-weight: 600; color: var(--slate-800);">Formcycle-Exportdatei (.xfp oder .json) hier ablegen oder klicken</div>
                    <p>Zero-Disk-Footprint: Verarbeitung im Arbeitsspeicher über Stufe 1 (AST) und optional Stufe 2 (LLM-API)</p>
                </div>

                <details class="llm-config-box">
                    <summary>Optionale KI-API-Anbindung für Stufe 2 (7 semantische/hybride Regeln via GWDG Academic Cloud / OpenAI-kompatibel)</summary>
                    <div class="llm-config-grid">
                        <div class="llm-field">
                            <label for="llmApiBase">API-Base-URL</label>
                            <input type="text" id="llmApiBase" value="https://chat-ai.academiccloud.de/v1" placeholder="https://chat-ai.academiccloud.de/v1">
                        </div>
                        <div class="llm-field">
                            <label for="llmModel">Modell-ID</label>
                            <input type="text" id="llmModel" value="deepseek-v4-flash-0731" placeholder="deepseek-v4-flash-0731">
                        </div>
                        <div class="llm-field">
                            <label for="llmApiKey">API-Schlüssel (nur flüchtig im Browser-Tab)</label>
                            <input type="password" id="llmApiKey" value="" placeholder="Bearer API-Key eingeben...">
                        </div>
                        <button class="btn btn-primary" id="btnReevalLLM" onclick="reevaluateActivePresetWithLLM()">
                            Mit KI-API prüfen
                        </button>
                    </div>
                </details>
            </div>
        </div>

        <!-- LLM Evaluation Transparency Banner -->
        <div id="llmStatusBanner" class="llm-banner llm-banner-warn"></div>

        <!-- Dashboard Summary -->
        <div class="dashboard-grid">
            <div class="score-card">
                <div class="gauge-container">
                    <svg class="gauge-svg" viewBox="0 0 160 160">
                        <circle class="gauge-bg" cx="80" cy="80" r="70" />
                        <circle class="gauge-meter" id="gaugeMeter" cx="80" cy="80" r="70" />
                    </svg>
                    <div class="gauge-text">
                        <span class="gauge-value" id="scoreValue">--</span>
                        <span class="gauge-label">von 100 Pkt.</span>
                    </div>
                </div>
                <div class="verdict-badge" id="verdictBadge">Wird berechnet...</div>
                <p id="currentFormName" style="font-size: 12px; color: var(--slate-600); margin-top: 8px; word-break: break-all;">-</p>
            </div>

            <div class="stats-grid">
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-title">Kritische Mängel</span>
                        <div class="stat-icon icon-critical">!</div>
                    </div>
                    <div class="stat-value" id="countCritical" style="color: var(--hwg-red);">0</div>
                    <div class="stat-sub">Je -15 Pkt. Abzug (Blocker)</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-title">Mittlere Mängel (Major)</span>
                        <div class="stat-icon icon-major">▲</div>
                    </div>
                    <div class="stat-value" id="countMajor" style="color: #ea580c;">0</div>
                    <div class="stat-sub">Je -8 Pkt. Abzug</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-title">Leichte Mängel (Minor)</span>
                        <div class="stat-icon icon-minor">●</div>
                    </div>
                    <div class="stat-value" id="countMinor" style="color: #854d0e;">0</div>
                    <div class="stat-sub">Je -3 Pkt. Abzug</div>
                </div>
                <div class="stat-card">
                    <div class="stat-header">
                        <span class="stat-title">Bestandene Prüfungen</span>
                        <div class="stat-icon icon-passed">✓</div>
                    </div>
                    <div class="stat-value" id="countPassed" style="color: var(--hwg-green);">0</div>
                    <div class="stat-sub" id="passRateSub">von 22 Governance-Regeln</div>
                </div>
            </div>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar" id="filterBar">
            <button class="filter-pill active" onclick="setFilter('all', this)">Alle Regeln (<span id="pillAll">22</span>)</button>
            <button class="filter-pill" onclick="setFilter('critical', this)">Kritisch (<span id="pillCritical">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('major', this)">Major (<span id="pillMajor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('minor', this)">Minor (<span id="pillMinor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('recommendation', this)">Empfehlungen (<span id="pillRec">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('passed', this)">Bestanden (<span id="pillPassed">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('unverified', this)">KI-ungeprüft (<span id="pillUnverified">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('na', this)">Nicht zutreffend (<span id="pillNA">0</span>)</button>
        </div>

        <div class="rules-list" id="rulesList"></div>
    </main>

    <script>
        const registry = {registry_json};
        const presets = {presets_json};
        const SEMANTIC_RULE_IDS = [
            "HWG-STAMM-02", "HWG-BTN-01", "HWG-BTN-02",
            "HWG-UX-02", "HWG-LANG-01", "HWG-LANG-02", "HWG-FEEDBACK-01"
        ];

        let activePresetKey = 'auslagen';
        let currentEval = presets.auslagen.eval;
        let currentFilter = 'all';

        document.getElementById('printDate').innerText = new Date().toLocaleDateString('de-DE');

        function escapeHtml(str) {{
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }}

        function getLlmUiConfig() {{
            const apiKey = (document.getElementById('llmApiKey')?.value || '').trim();
            const apiBase = (document.getElementById('llmApiBase')?.value || 'https://chat-ai.academiccloud.de/v1').trim().replace(/\\/+$/, '');
            const model = (document.getElementById('llmModel')?.value || 'deepseek-v4-flash-0731').trim();
            return {{ apiKey, apiBase, model }};
        }}

        function initPresets() {{
            const grid = document.getElementById('presetGrid');
            grid.innerHTML = '';
            for (const [key, p] of Object.entries(presets)) {{
                const btn = document.createElement('div');
                btn.className = `preset-btn ${{key === activePresetKey ? 'active' : ''}}`;
                btn.id = `preset-${{key}}`;

                const score = p.eval.score;
                let scoreClass = 'score-poor';
                if (score >= 80) scoreClass = 'score-good';
                else if (score >= 50) scoreClass = 'score-mid';

                btn.innerHTML = `
                    <div class="preset-btn-title">
                        <span>${{escapeHtml((p.name.split(':')[1] || p.name).trim())}}</span>
                        <span class="preset-score-pill ${{scoreClass}}">${{score}} P</span>
                    </div>
                    <div class="preset-btn-desc">${{escapeHtml(p.eval.form)}}</div>
                `;
                btn.onclick = () => selectPreset(key);
                grid.appendChild(btn);
            }}
        }}

        function selectPreset(key) {{
            activePresetKey = key;
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            const activeBtn = document.getElementById(`preset-${{key}}`);
            if (activeBtn) activeBtn.classList.add('active');
            currentEval = presets[key].eval;
            renderEvaluation();
        }}

        async function reevaluateActivePresetWithLLM() {{
            if (!activePresetKey) {{
                alert('Bitte wählen Sie ein Preset aus oder laden Sie eine Datei erneut hoch.');
                return;
            }}
            const cfg = getLlmUiConfig();
            const btn = document.getElementById('btnReevalLLM');
            const origText = btn.innerText;
            btn.innerText = 'Prüfe via KI-API...';
            btn.disabled = true;
            try {{
                const headers = {{ 'Content-Type': 'application/json' }};
                if (cfg.apiKey) headers['X-LLM-Api-Key'] = cfg.apiKey;
                if (cfg.apiBase) headers['X-LLM-Api-Base'] = cfg.apiBase;
                if (cfg.model) headers['X-LLM-Model'] = cfg.model;

                const resp = await fetch('/api/evaluate-preset', {{
                    method: 'POST',
                    headers,
                    body: JSON.stringify({{ preset: activePresetKey }})
                }});
                if (!resp.ok) throw new Error('Lokaler Python-Server (/api/evaluate-preset) nicht erreichbar.');
                const res = await resp.json();
                presets[activePresetKey].eval = res;
                currentEval = res;
                initPresets();
                renderEvaluation();
            }} catch (err) {{
                alert('Hinweis: Für Preset-Live-Prüfungen bitte den lokalen Server starten (python web/server.py) oder die .xfp/.json-Datei direkt in das Upload-Feld ziehen. Detail: ' + err.message);
            }} finally {{
                btn.innerText = origText;
                btn.disabled = false;
            }}
        }}

        function renderEvaluation() {{
            const e = currentEval;
            document.getElementById('currentFormName').innerText = e.form;
            document.getElementById('printMeta').innerText = `Formular: ${{e.form}} | Datum: ${{new Date().toLocaleDateString('de-DE')}} | Registry v${{registry.version}}`;

            // KI-Transparenz-Banner aktualisieren
            const banner = document.getElementById('llmStatusBanner');
            const llmInfo = e.llm_evaluation || {{ evaluated: false, status: 'unconfigured', reason: 'Keine LLM-API angebunden.' }};
            const unverifiedList = e.unverified_semantic || [];
            if (llmInfo.evaluated && unverifiedList.length === 0) {{
                banner.className = 'llm-banner llm-banner-ok';
                banner.innerHTML = `
                    <div style="font-size: 18px; font-weight: 800;">✓</div>
                    <div>
                        <strong>Zweistufige Hybrid-Prüfung aktiv (Stufe 1 AST + Stufe 2 KI-API):</strong>
                        Alle 15 deterministischen Regeln sowie alle 7 semantischen/hybriden Regeln wurden erfolgreich ausgewertet
                        (Modell: <code>${{escapeHtml(llmInfo.model || 'LLM')}}</code>).
                    </div>`;
            }} else {{
                banner.className = 'llm-banner llm-banner-warn';
                banner.innerHTML = `
                    <div style="font-size: 18px; font-weight: 800;">⚠</div>
                    <div>
                        <strong>KI-Stufe (Stufe 2) nicht durchgeführt – Semantische Regeln ungeprüft:</strong>
                        ${{escapeHtml(llmInfo.reason || 'Keine aktive LLM-API-Verbindung.')}}
                        Die <strong>${{unverifiedList.length || 7}} semantischen/hybriden Regeln</strong>
                        (<code>${{escapeHtml((unverifiedList.length ? unverifiedList : SEMANTIC_RULE_IDS).join(', '))}}</code>)
                        wurden <strong>nicht von einer KI begutachtet</strong> und sind unten eindeutig als
                        <em>„Nicht zutreffend · Keine KI-Prüfung“</em> gekennzeichnet. Der angezeigte Score basiert ausschließlich auf den 15 deterministischen AST-Regeln (Stufe 1).
                    </div>`;
            }}

            const score = e.score;
            document.getElementById('scoreValue').innerText = score;

            const circumference = 440;
            const offset = circumference - (score / 100) * circumference;
            const meter = document.getElementById('gaugeMeter');
            meter.style.strokeDashoffset = offset;

            const verdict = document.getElementById('verdictBadge');
            if (score >= 80) {{
                meter.style.stroke = 'var(--hwg-green)';
                verdict.innerText = 'Hohe Compliance (Freigabefähig)';
                verdict.style.background = 'var(--hwg-green-subtle)';
                verdict.style.color = 'var(--hwg-green)';
            }} else if (score >= 50) {{
                meter.style.stroke = '#ea580c';
                verdict.innerText = 'Eingeschränkt (Nachbesserung)';
                verdict.style.background = '#fff7ed';
                verdict.style.color = '#ea580c';
            }} else {{
                meter.style.stroke = 'var(--hwg-red)';
                verdict.innerText = 'Kritisch unzureichend (Gesperrt)';
                verdict.style.background = 'var(--hwg-red-subtle)';
                verdict.style.color = 'var(--hwg-red)';
            }}

            let criticals = 0, majors = 0, minors = 0, recs = (e.recommendations || []).length;
            (e.violations || []).forEach(v => {{
                if (v.severity === 'critical') criticals++;
                else if (v.severity === 'major') majors++;
                else if (v.severity === 'minor') minors++;
            }});

            const passedCount = (e.passed || []).length;
            const naCount = Object.keys(e.not_applicable || {{}}).length;
            const unverifiedCount = (e.unverified_semantic || []).length;

            document.getElementById('countCritical').innerText = criticals;
            document.getElementById('countMajor').innerText = majors;
            document.getElementById('countMinor').innerText = minors;
            document.getElementById('countPassed').innerText = passedCount;
            document.getElementById('passRateSub').innerText = unverifiedCount > 0
                ? `von 15 geprüften AST-Regeln (${{unverifiedCount}} KI-offen)`
                : `von 22 Governance-Regeln`;

            document.getElementById('pillAll').innerText = registry.rules.length;
            document.getElementById('pillCritical').innerText = criticals;
            document.getElementById('pillMajor').innerText = majors;
            document.getElementById('pillMinor').innerText = minors;
            document.getElementById('pillRec').innerText = recs;
            document.getElementById('pillPassed').innerText = passedCount;
            document.getElementById('pillUnverified').innerText = unverifiedCount;
            document.getElementById('pillNA').innerText = naCount;

            renderRuleCards();
        }}

        function setFilter(filter, btnEl) {{
            currentFilter = filter;
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            if (btnEl) btnEl.classList.add('active');
            renderRuleCards();
        }}

        function renderRuleCards() {{
            const container = document.getElementById('rulesList');
            container.innerHTML = '';

            const violationsMap = {{}};
            (currentEval.violations || []).forEach(v => {{ violationsMap[v.rule] = v; }});
            const recMap = {{}};
            (currentEval.recommendations || []).forEach(r => {{ recMap[r.rule] = r; }});
            const passedSet = new Set((currentEval.passed || []).map(p => p.split(' ')[0]));
            const unverifiedSet = new Set(currentEval.unverified_semantic || []);

            registry.rules.forEach(rule => {{
                const isViolation = !!violationsMap[rule.id];
                const isRec = !!recMap[rule.id];
                const isPassed = passedSet.has(rule.id);
                const isUnverified = unverifiedSet.has(rule.id);
                const isNotApplicable = !isViolation && !isRec && !isPassed;

                if (currentFilter === 'critical' && (!isViolation || violationsMap[rule.id].severity !== 'critical')) return;
                if (currentFilter === 'major' && (!isViolation || violationsMap[rule.id].severity !== 'major')) return;
                if (currentFilter === 'minor' && (!isViolation || violationsMap[rule.id].severity !== 'minor')) return;
                if (currentFilter === 'recommendation' && !isRec) return;
                if (currentFilter === 'passed' && !isPassed) return;
                if (currentFilter === 'unverified' && !isUnverified) return;
                if (currentFilter === 'na' && !isNotApplicable) return;

                const card = document.createElement('div');
                let cardClass = 'rule-card';
                let badgeHtml = '';
                let messageHtml = '';

                const stageLabel = rule.evaluation_type === 'deterministic'
                    ? 'Stufe 1 · Deterministisch (AST)'
                    : (rule.evaluation_type === 'hybrid' ? 'Stufe 2 · Hybrid (AST + LLM)' : 'Stufe 2 · Semantisch (LLM)');

                if (isViolation) {{
                    const v = violationsMap[rule.id];
                    cardClass += ` violation-${{v.severity}}`;
                    const pts = v.severity === 'critical' ? '-15P' : (v.severity === 'major' ? '-8P' : '-3P');
                    badgeHtml = `<span class="badge badge-${{v.severity}}">${{v.severity.toUpperCase()}} (${{pts}})</span>`;
                    messageHtml = `<div class="rule-message"><strong>Befund:</strong> ${{escapeHtml(v.message)}}</div>`;
                }} else if (isRec) {{
                    const r = recMap[rule.id];
                    cardClass += ' violation-recommendation';
                    badgeHtml = `<span class="badge badge-recommendation">EMPFEHLUNG (0P)</span>`;
                    messageHtml = `<div class="rule-message"><strong>Empfehlung:</strong> ${{escapeHtml(r.message)}}</div>`;
                }} else if (isPassed) {{
                    cardClass += ' rule-passed';
                    badgeHtml = `<span class="badge badge-passed">BESTANDEN (OK)</span>`;
                    messageHtml = `<div class="rule-message" style="color: var(--hwg-green);">✓ Vorgaben erfolgreich eingehalten.</div>`;
                }} else if (isUnverified) {{
                    cardClass += ' rule-unverified';
                    badgeHtml = `<span class="badge badge-unverified">NICHT ZUTREFFEND · KEINE KI-PRÜFUNG</span>`;
                    const naReason = (currentEval.not_applicable && currentEval.not_applicable[rule.id])
                        ? currentEval.not_applicable[rule.id]
                        : 'KI-Prüfung ausstehend: Keine LLM-API angebunden oder API-Ausfall.';
                    messageHtml = `<div class="rule-message" style="color: #92400e;"><strong>Ungeprüft (kein KI-Audit):</strong> ${{escapeHtml(naReason)}}</div>`;
                }} else {{
                    cardClass += ' rule-na';
                    badgeHtml = `<span class="badge" style="background: var(--slate-100); color: var(--slate-600); border: 1px solid var(--slate-300);">NICHT ZUTREFFEND</span>`;
                    const naReason = (currentEval.not_applicable && currentEval.not_applicable[rule.id])
                        ? currentEval.not_applicable[rule.id]
                        : 'Kriterium auf diesen Formularkontext nicht anwendbar.';
                    messageHtml = `<div class="rule-message" style="color: var(--slate-600);">${{escapeHtml(naReason)}}</div>`;
                }}

                let remediationHtml = '';
                if (!isPassed) {{
                    remediationHtml = `
                    <div class="remediation-box">
                        <div class="remediation-title">Klickpfad im XIMA Formcycle Designer (Remediation):</div>
                        <div class="remediation-text">${{escapeHtml(rule.remediation)}}</div>
                    </div>`;
                }}

                card.className = cardClass;
                card.innerHTML = `
                    <div class="rule-top">
                        <div class="rule-id-name">
                            <span class="rule-id">${{escapeHtml(rule.id)}}</span>
                            <span class="rule-stage-tag">${{escapeHtml(stageLabel)}}</span>
                            <span class="rule-name">${{escapeHtml(rule.name)}}</span>
                        </div>
                        ${{badgeHtml}}
                    </div>
                    ${{messageHtml}}
                    ${{remediationHtml}}
                    <div class="rationale-text">Theoretische &amp; regulatorische Fundierung: ${{escapeHtml(rule.rationale)}}</div>
                `;
                container.appendChild(card);
            }});
        }}

        function exportAuditJSON() {{
            const dataStr = "data:text/json;charset=utf-8," + encodeURIComponent(JSON.stringify(currentEval, null, 2));
            const dlAnchor = document.createElement('a');
            dlAnchor.setAttribute("href", dataStr);
            dlAnchor.setAttribute("download", `audit_${{currentEval.form.replace(/[^a-zA-Z0-9_-]/g, '_')}}.json`);
            document.body.appendChild(dlAnchor);
            dlAnchor.click();
            dlAnchor.remove();
        }}

        function decodeHtmlEntities(str) {{
            if (!str) return '';
            const txt = document.createElement('textarea');
            txt.innerHTML = String(str);
            return txt.value;
        }}

        function cleanVisibleText(raw) {{
            if (!raw) return '';
            const unesc = decodeHtmlEntities(raw);
            return unesc.replace(/<[^>]+>/g, ' ').replace(/\\s+/g, ' ').trim();
        }}

        function hasDirtyLabelMarkup(rawLabel) {{
            if (!rawLabel) return false;
            const val = String(rawLabel).trim();
            if (/&amp;[a-zA-Z0-9#]+;/.test(val) || val.toLowerCase().includes('&nbsp;')) return true;
            if (/<\\s*(?:br|span|div|font|table|tr|td|ul|ol|li|h[1-6])\\b/i.test(val)) return true;
            if (/\\bstyle\\s*=/i.test(val)) return true;
            const pMatches = val.match(/<\\s*p\\b/gi);
            if (pMatches && pMatches.length > 1) return true;
            const cleaned = cleanVisibleText(val);
            if (cleaned.includes('|') || cleaned.includes('<') || cleaned.includes('>')) return true;
            return false;
        }}

        function extractWorkflowClient(obj, emails, states) {{
            if (!obj) return;
            if (Array.isArray(obj)) {{
                obj.forEach(item => extractWorkflowClient(item, emails, states));
            }} else if (typeof obj === 'object') {{
                if (obj.type === 'FC_EMAIL') {{
                    let cp = {{}};
                    try {{
                        cp = typeof obj.customParameters === 'string' ? JSON.parse(obj.customParameters) : (obj.customParameters || {{}});
                    }} catch (e) {{}}
                    emails.push({{
                        node_name: obj.name || '',
                        recipient: cp.to || cp.recipients || cp.recipient || '',
                        subject: cp.subject || '',
                        body: cp.body || ''
                    }});
                }} else if (['FC_CHANGE_STATE', 'CUSTOM', 'RECEIVED'].includes(obj.type)) {{
                    const st = String(obj.name || '').trim();
                    if (st && st !== 'FC_CHANGE_STATE' && !states.includes(st)) {{
                        states.push(st);
                    }}
                }}
                for (const k in obj) {{
                    extractWorkflowClient(obj[k], emails, states);
                }}
            }}
        }}

        async function evaluateFormDataClient(formData, filename, workflowEmails, workflowStates) {{
            const results = {{
                form: filename,
                violations: [],
                recommendations: [],
                passed: [],
                not_applicable: {{}},
                unverified_semantic: [],
                llm_evaluation: {{
                    evaluated: false,
                    status: 'unconfigured',
                    model: null,
                    api_base: null,
                    reason: '',
                    unverified_rules: []
                }},
                score: 100
            }};

            const items = formData.items || [];
            const formProps = formData.properties || {{}};
            const penalties = registry.scoring.severity_penalties;
            const inputClasses = new Set([
                "XTextField", "XTextArea", "XSelect", "XCheckbox",
                "XUpload", "XFile", "XRadio", "XDate", "XNumber"
            ]);

            const idToItem = {{}};
            items.forEach(it => {{
                const p = it.properties || {{}};
                const iid = String(p.id || p.name || "");
                if (iid) idToItem[iid] = it;
            }});

            function getAncestors(props) {{
                const chain = [];
                let pid = String(props.parentid || "");
                const visited = new Set();
                for (let i = 0; i < 8; i++) {{
                    if (!pid || visited.has(pid) || !idToItem[pid]) break;
                    visited.add(pid);
                    const parentIt = idToItem[pid];
                    chain.push(parentIt);
                    pid = String((parentIt.properties || {{}}).parentid || "");
                }}
                return chain;
            }}

            function isInHeader(it) {{
                const c = it.className || "";
                const props = it.properties || {{}};
                if (c === "XHeader") return true;
                if (String(props.parentid || "").toLowerCase().includes("header")) return true;
                return getAncestors(props).some(a => a.className === "XHeader");
            }}

            function isApplicantVisible(props) {{
                const vs = props.viewstatus;
                if (Array.isArray(vs) && vs.length > 0 && !vs.map(String).includes("-1")) return false;
                for (const anc of getAncestors(props)) {{
                    const avs = (anc.properties || {{}}).viewstatus;
                    if (Array.isArray(avs) && avs.length > 0 && !avs.map(String).includes("-1")) return false;
                }}
                return true;
            }}

            function getSectionKey(props) {{
                for (const anc of getAncestors(props)) {{
                    if (["XFieldSet", "XContainer", "XContainerInvisible", "XPage"].includes(anc.className)) {{
                        const ap = anc.properties || {{}};
                        return String(ap.id || ap.name || "root");
                    }}
                }}
                return String(props.parentid || "root");
            }}

            const rowCounts = {{}};
            items.forEach(it => {{
                const props = it.properties || {{}};
                if (!isApplicantVisible(props)) return;
                const rid = String(props.rowid || "").trim();
                if (rid) rowCounts[rid] = (rowCounts[rid] || 0) + 1;
            }});

            const containerWidths = [];
            if (formProps.maxwidth) containerWidths.push(String(formProps.maxwidth).trim().toLowerCase());

            const headerImages = [];
            let headerH1Count = 0;
            let headerHasNonH1Title = false;
            let footerShowsLogo = false;
            let headerOrFooterShowsReqHint = false;
            let footerShowsPrivacy = false;

            const fieldsetsAll = [];
            const fieldsetsMissingLegend = [];
            const containerInputChildren = {{}};
            let applicantInputCount = 0;
            let rawXPageCount = 0;

            let requiredFieldsTotal = 0;
            const manualAsterisksInLabels = [];
            const dirtyLabels = [];
            const devNotes = [];
            const sectionPersonalSeq = {{}};

            let hasPersonalData = false;
            let hasTextDsgvoWithLink = false;
            let hasUploadElements = false;
            const deficientUploads = [];
            const structuredFieldsUnvalidated = [];
            let hasCompactFields = false;
            const compactFieldsUnconstrained = [];

            const nonPersonKeywords = [
                "vorname", "antrag", "bank", "kredit", "projekt", "programm",
                "foerder", "förder", "titel", "datei", "forschung", "vorhaben", "institut",
                "organisation", "unternehmen", "thema", "kurs", "modul", "fach",
                "abteilung", "studiengang", "dokument", "bezeichnung", "stelle",
                "einrichtung", "arbeit", "abschlussarbeit", "hochschule", "firma",
                "suche", "praxispartner", "betreuer"
            ];

            items.forEach(it => {{
                const c = it.className || "";
                const props = it.properties || {{}};
                const elemName = String(props.name || "unnamed");
                const nameLow = elemName.toLowerCase();
                const appVis = isApplicantVisible(props);

                if (c === "XPage") rawXPageCount++;

                const rawLbl = String(props.label || props.text || props.heading || "");
                const lblClean = cleanVisibleText(rawLbl);
                const lblLower = lblClean.toLowerCase();
                const helpRaw = String(props.helptext || props.help || props.tooltip || props.description || "");
                const helpClean = cleanVisibleText(helpRaw).toLowerCase();

                if (["XHeader", "XPage", "XFooter"].includes(c) && props.maxwidth) {{
                    containerWidths.push(String(props.maxwidth).trim().toLowerCase());
                }}

                if (isInHeader(it)) {{
                    if (c === "XImage") headerImages.push(props);
                    const combinedH = `${{props.rtevalue || ""}} ${{props.heading || ""}} ${{props.label || ""}} ${{props.text || ""}}`;
                    const h1Matches = combinedH.match(/<\\s*h1\\b/gi);
                    if (h1Matches && h1Matches.length > 0) {{
                        headerH1Count += h1Matches.length;
                    }} else if (String(props.headinglevel || "").trim() === "1" && cleanVisibleText(combinedH)) {{
                        headerH1Count += 1;
                    }} else if (/<\\s*h[2-6]\\b/i.test(combinedH) || (["XSpan", "XHeading", "XText"].includes(c) && cleanVisibleText(combinedH).length >= 5)) {{
                        headerHasNonH1Title = true;
                    }}
                }}

                if (["XHeader", "XFooter"].includes(c)) {{
                    if (["1", "true"].includes(String(props.showrequiredhint || "0").trim().toLowerCase())) {{
                        headerOrFooterShowsReqHint = true;
                    }}
                }}
                if (c === "XFooter") {{
                    if (["1", "true"].includes(String(props.showlogo || "0").trim().toLowerCase())) footerShowsLogo = true;
                    if (["1", "true"].includes(String(props.privacyPolicyShow || "0").trim().toLowerCase())) footerShowsPrivacy = true;
                }}

                if (c === "XFieldSet" && appVis) {{
                    fieldsetsAll.push(elemName);
                    const legTxt = cleanVisibleText(props.legend || props.label || props.heading || "");
                    if (!legTxt) fieldsetsMissingLegend.push(elemName);
                }}

                if (inputClasses.has(c) && appVis) {{
                    applicantInputCount++;
                    const ancs = getAncestors(props);
                    const inFs = ancs.some(a => a.className === "XFieldSet");
                    if (!inFs) {{
                        ancs.forEach(a => {{
                            if (["XContainer", "XContainerInvisible"].includes(a.className) && !isInHeader(a)) {{
                                const cn = String((a.properties || {{}}).name || "container");
                                containerInputChildren[cn] = (containerInputChildren[cn] || 0) + 1;
                            }}
                        }});
                    }}

                    const isReq = ["1", "true"].includes(String(props.required || "0").trim().toLowerCase()) || Boolean(String(props.requiredif || "").trim());
                    if (isReq) requiredFieldsTotal++;
                    else if (/(?:\\*\\s*$|\\(\\*\\)|\\s\\*(?:\\s|$))/.test(lblClean)) manualAsterisksInLabels.push(elemName);
                }}

                if ((inputClasses.has(c) || c === "XFieldSet") && appVis && props.label && hasDirtyLabelMarkup(props.label)) {{
                    dirtyLabels.push(elemName);
                }}

                if (appVis) {{
                    for (const tk of ["label", "text", "heading", "rtevalue", "value"]) {{
                        const tval = String(props[tk] || "");
                        if (!tval) continue;
                        const tClean = cleanVisibleText(tval);
                        const tLow = tClean.toLowerCase();
                        if (["javascript", "shibboleth", "shibboleh", "ldap-member", "forms-admin", "postfach-sb", "display:none", "display: none", "ausgeblendet (hide)", "saml-hslu"].some(p => tLow.includes(p))) {{
                            devNotes.push(`${{elemName}}: '${{tClean.slice(0, 60)}}'`);
                            break;
                        }}
                    }}
                }}

                if (inputClasses.has(c) && c !== "XTextArea" && appVis) {{
                    const secKey = getSectionKey(props);
                    if (!sectionPersonalSeq[secKey]) sectionPersonalSeq[secKey] = [];
                    const seq = sectionPersonalSeq[secKey];
                    const hasNachname = seq.some(f => f[0] === "nachname");
                    const isExplicitLastname = (
                        nameLow.includes("nachname") || lblLower.includes("nachname") ||
                        ["name", "familienname"].includes(lblLower) ||
                        ["name antragstellende", "name antragsteller", "name der antragstellenden"].some(p => lblLower.includes(p))
                    ) && !nameLow.includes("vorname") && !lblLower.includes("vorname") && !nameLow.includes("suche") && !lblLower.includes("suche");
                    const isNonPerson = nonPersonKeywords.some(k => nameLow.includes(k) || lblLower.includes(k));

                    if (["anrede", "salutation"].some(t => nameLow.includes(t) || lblLower.includes(t)) && lblClean.length <= 30) {{
                        seq.push(["anrede", elemName, lblClean || "Anrede", 1]);
                    }} else if ((nameLow.includes("vorname") || lblLower.includes("vorname")) && !nameLow.includes("suche")) {{
                        seq.push(["vorname", elemName, lblClean || "Vorname", 2]);
                    }} else if (isExplicitLastname || (!isNonPerson && !hasNachname && nameLow.includes("name"))) {{
                        seq.push(["nachname", elemName, lblClean || "Nachname", 3]);
                    }} else if (["email", "e-mail", "mail"].some(t => nameLow.includes(t) || lblLower.includes(t)) && c === "XTextField") {{
                        seq.push(["email", elemName, lblClean || "E-Mail-Adresse", 4]);
                    }} else if (["telefon", "telefonnummer", "phone", "mobilfunk"].some(t => nameLow.includes(t) || lblLower.includes(t)) && c === "XTextField") {{
                        seq.push(["telefon", elemName, lblClean || "Telefonnummer", 5]);
                    }}
                }}

                if (inputClasses.has(c) && ["vorname", "nachname", "email", "e-mail", "matrikel", "geburtsdatum", "iban", "anschrift", "telefon"].some(t => nameLow.includes(t) || lblLower.includes(t))) {{
                    hasPersonalData = true;
                }}

                const rawHtmlCtx = `${{rawLbl}} ${{helpRaw}} ${{props.rtevalue || ""}} ${{props.html || ""}}`.toLowerCase();
                if (["datenschutz", "dsgvo", "art. 13", "artikel 13", "datenverarbeitung"].some(t => rawHtmlCtx.includes(t)) &&
                    ["href=", "https://", "http://", "www.hwg-lu.de/datenschutz", "hwg-lu.de/datenschutz"].some(l => rawHtmlCtx.includes(l))) {{
                    hasTextDsgvoWithLink = true;
                }}

                if ((["XUpload", "XFile", "XUploadButton"].includes(c) || nameLow.includes("upload")) && appVis) {{
                    hasUploadElements = true;
                    const visCtx = `${{lblLower}} ${{helpClean}}`;
                    const hasVisFmt = ["pdf", "jpg", "jpeg", "png", "docx", "xlsx", "zip", "dateiformat"].some(f => visCtx.includes(f));
                    const hasVisSize = ["mb", "kb", "maximal", "max.", "dateigröße", "dateigroesse"].some(s => visCtx.includes(s));
                    const fext = String(props.fileextension || "").trim().toLowerCase();
                    const msize = parseInt(String(props.maxfilesize || "0").trim() || "0", 10) || 0;
                    const hasTech = Boolean(fext) && msize > 0;
                    let contradiction = false;
                    if (fext) {{
                        ["docx", "xlsx", "zip"].forEach(pe => {{
                            if (visCtx.includes(pe) && !fext.includes(pe.slice(0, 3))) contradiction = true;
                        }});
                    }}
                    if (!(hasVisFmt && hasVisSize && hasTech) || contradiction) {{
                        deficientUploads.push(elemName);
                    }}
                }}

                if (["XTextField", "XDate", "XNumber"].includes(c) && appVis) {{
                    const dt = String(props.datatype || "").trim();
                    const vrule = String(props.vrule || props.pattern || "").trim();
                    const valDict = (props.validation && typeof props.validation === 'object') ? props.validation : {{}};
                    const hasCustomRegex = (dt === "regexp" && Boolean(vrule)) || Boolean(props.pattern) || Boolean(valDict.regex);

                    const isPlz = /\\b(?:plz|postleitzahl)\\b/.test(lblLower) || nameLow.includes("plz") || nameLow.includes("postleitzahl");
                    const isIban = /\\biban\\b/.test(lblLower) || nameLow.includes("iban");
                    const isPhone = ["telefon", "mobilfunk", "handynummer"].some(t => nameLow.includes(t) || lblLower.includes(t));
                    const isDate = c === "XDate" || nameLow.includes("geburtsdatum") || lblLower.includes("geburtsdatum") || /\\bdatum\\b/.test(lblLower);
                    const isMatrikel = nameLow.includes("matrikel") || lblLower.includes("matrikel");

                    if (isPlz && !(dt === "plzDE" || hasCustomRegex)) structuredFieldsUnvalidated.push(elemName);
                    else if (isIban && !(hasCustomRegex || valDict.type === "iban")) structuredFieldsUnvalidated.push(elemName);
                    else if (isPhone && !(dt === "phone" || hasCustomRegex)) structuredFieldsUnvalidated.push(elemName);
                    else if (isDate && !(c === "XDate" || ["dateDE", "dateISO", "date", "datetime"].includes(dt) || hasCustomRegex)) structuredFieldsUnvalidated.push(elemName);
                    else if (isMatrikel && !hasCustomRegex) structuredFieldsUnvalidated.push(elemName);
                }}

                if (c === "XTextField" && appVis) {{
                    const isCompact = /\\b(?:plz|postleitzahl|hausnummer|hausnr|hnr)\\b/.test(lblLower) || ["plz", "postleitzahl", "hausnummer", "hnr"].some(k => nameLow.includes(k));
                    if (isCompact) {{
                        hasCompactFields = true;
                        const cw = String(props.computedwidth || "").trim();
                        const pct = cw.endsWith("%") ? parseFloat(cw) : 100;
                        const rid = String(props.rowid || "").trim();
                        const colW = props.colwidth || props.width;
                        const isSmall = (pct < 100) || (rid && (rowCounts[rid] || 0) >= 2) || (props.maxwidth && String(props.maxwidth).toLowerCase() !== "100%") || (colW && !["100%", "12"].includes(String(colW)));
                        if (!isSmall) compactFieldsUnconstrained.push(elemName);
                    }}
                }}
            }});

            const unsemanticContainers = Object.entries(containerInputChildren).filter(([, cnt]) => cnt >= 3).map(([k]) => k);
            const distinctWidths = Array.from(new Set(containerWidths.filter(Boolean)));

            if (distinctWidths.length === 0 || !(distinctWidths.length === 1 && distinctWidths[0] === "850px")) {{
                results.violations.push({{ rule: "HWG-CD-01", rule_id: "HWG-CD-01", severity: "major", message: `Layout-Container weichen vom 850px-Standard ab (gefunden: ${{distinctWidths.filter(w => w !== '850px').join(', ') || 'undefiniert'}}).` }});
                results.score -= penalties.major;
            }} else results.passed.push("HWG-CD-01 (Layout-Breite durchgängig 850px)");

            if (headerImages.length === 0) {{
                results.violations.push({{ rule: "HWG-CD-02", rule_id: "HWG-CD-02", severity: "critical", message: "Kein offizielles HWG-Header-Banner (XImage) im Header-Container (XHeader) vorhanden." }});
                results.score -= penalties.critical;
            }} else {{
                const ip = headerImages[0];
                const ih = String(ip.imageheight || ip.height || "").trim().toLowerCase();
                const ia = String(ip.textalign || ip.align || "").trim().toLowerCase();
                const ialt = cleanVisibleText(ip.alt || ip.alttext || ip.title || ip.tooltip || ip.description || ip.label || "").toLowerCase();
                const okH = ["60", "60px"].includes(ih);
                const cssClasses = Array.isArray(ip.cssclasses) ? ip.cssclasses : [String(ip.cssclasses || "")];
                const okA = ["right", "2"].includes(ia) || cssClasses.includes("xm-t-right");
                const okAlt = Boolean(ialt) && (
                    ialt.includes("hochschule für wirtschaft und gesellschaft") ||
                    ialt.includes("hochschule fuer wirtschaft und gesellschaft") ||
                    ialt.includes("hwg ludwigshafen") ||
                    ialt.includes("hwg lu") ||
                    ialt.includes("hwglu") ||
                    ialt.includes("hochschule ludwigshafen") ||
                    ((ialt.includes("hwg") || ialt.includes("hochschule") || ialt.includes("ludwigshafen")) && ialt.includes("logo"))
                );
                if (!(okH && okA && okAlt)) {{
                    const iss = [];
                    if (!okH) iss.push(`Höhe '${{ih || 'undefiniert'}}' statt 60px`);
                    if (!okA) iss.push(`Ausrichtung '${{ia || 'links'}}' statt rechtsbündig`);
                    if (!okAlt) iss.push("Alternativtext (alt) fehlt/unvollständig");
                    results.violations.push({{ rule: "HWG-CD-02", rule_id: "HWG-CD-02", severity: "major", message: `HWG-Header-Logo weicht ab: ${{iss.join(', ')}}.` }});
                    results.score -= penalties.major;
                }} else results.passed.push("HWG-CD-02 (Header-Logo 60px, rechtsbündig, mit Alt-Text)");
            }}

            if (footerShowsLogo) {{
                results.violations.push({{ rule: "HWG-CD-03", rule_id: "HWG-CD-03", severity: "major", message: "Im Footer (XFooter) ist 'Logo anzeigen' (showlogo='1') aktiviert." }});
                results.score -= penalties.major;
            }} else results.passed.push("HWG-CD-03 (XIMA-Logo deaktiviert)");

            if (headerH1Count === 1) results.passed.push("HWG-CD-04 (Formulartitel im Header als H1 ausgezeichnet)");
            else {{
                results.violations.push({{ rule: "HWG-CD-04", rule_id: "HWG-CD-04", severity: "major", message: headerHasNonH1Title ? "Formulartitel im Header ist nicht als <h1> ausgezeichnet." : "Kein Formulartitel als <h1> im Kopfbereich (XHeader) vorhanden." }});
                results.score -= penalties.major;
            }}

            if (applicantInputCount < 4 && fieldsetsAll.length === 0) {{
                results.not_applicable["HWG-A11Y-01"] = "Kleinstformular (< 4 Eingabefelder).";
            }} else if (fieldsetsAll.length === 0 || fieldsetsMissingLegend.length > 0 || unsemanticContainers.length > 0) {{
                results.violations.push({{ rule: "HWG-A11Y-01", rule_id: "HWG-A11Y-01", severity: "critical", message: fieldsetsAll.length === 0 ? `Keine semantischen XFieldSet-Gruppierungen für ${{applicantInputCount}} Eingabefelder vorhanden.` : "Unvollständige Fieldset-Legenden oder unsemantische XContainer-Sektionen gefunden." }});
                results.score -= penalties.critical;
            }} else results.passed.push("HWG-A11Y-01 (Fieldsets mit Legenden vorhanden)");

            if ((requiredFieldsTotal > 0 && !headerOrFooterShowsReqHint) || manualAsterisksInLabels.length > 0) {{
                results.violations.push({{ rule: "HWG-A11Y-02", rule_id: "HWG-A11Y-02", severity: "major", message: "Pflichtfeldlegende (showrequiredhint='1') in Header/Footer deaktiviert oder manuelles Sternchen (*) ohne required='1'." }});
                results.score -= penalties.major;
            }} else if (requiredFieldsTotal > 0) results.passed.push("HWG-A11Y-02 (Pflichtfelder korrekt deklariert)");
            else results.not_applicable["HWG-A11Y-02"] = "Keine Pflichtfelder vorhanden.";

            if (dirtyLabels.length > 0) {{
                results.violations.push({{ rule: "HWG-A11Y-03", rule_id: "HWG-A11Y-03", severity: "minor", message: `HTML-Störfragmente in ${{dirtyLabels.length}} Label(s): [${{dirtyLabels.slice(0, 5).join(', ')}}].` }});
                results.score -= penalties.minor;
            }} else results.passed.push("HWG-A11Y-03 (Saubere Labels)");

            const outOfOrder = [];
            let hasMultiFieldSec = false;
            Object.values(sectionPersonalSeq).forEach(seq => {{
                if (seq.length >= 2) {{
                    hasMultiFieldSec = true;
                    for (let i = 0; i < seq.length - 1; i++) {{
                        if (seq[i][3] > seq[i + 1][3]) outOfOrder.push(`'${{seq[i][2]}}' vor '${{seq[i + 1][2]}}'`);
                    }}
                }}
            }});
            if (!hasMultiFieldSec) results.not_applicable["HWG-STAMM-01"] = "Keine Stammdaten-Sektion mit >= 2 Personenfeldern vorhanden.";
            else if (outOfOrder.length > 0) {{
                results.violations.push({{ rule: "HWG-STAMM-01", rule_id: "HWG-STAMM-01", severity: "major", message: `Inkonsistente Stammdaten-Abfolge: ${{outOfOrder.slice(0, 3).join(', ')}}.` }});
                results.score -= penalties.major;
            }} else results.passed.push("HWG-STAMM-01 (Kanonische Stammdaten-Abfolge)");

            if (devNotes.length > 0) {{
                results.violations.push({{ rule: "HWG-UI-01", rule_id: "HWG-UI-01", severity: "critical", message: `Sichtbare Entwickler-Notizen im Frontend: ${{devNotes.slice(0, 2).join('; ')}}.` }});
                results.score -= penalties.critical;
            }} else results.passed.push("HWG-UI-01 (Keine Entwickler-Notizen)");

            if (!hasPersonalData) results.not_applicable["HWG-DSGVO-01"] = "Keine personenbezogenen Daten erhoben.";
            else if (!(footerShowsPrivacy || hasTextDsgvoWithLink)) {{
                results.violations.push({{ rule: "HWG-DSGVO-01", rule_id: "HWG-DSGVO-01", severity: "critical", message: "Personenbezogene Daten ohne DSGVO-Hinweis / Verlinkung." }});
                results.score -= penalties.critical;
            }} else results.passed.push("HWG-DSGVO-01 (DSGVO-Hinweis vorhanden)");

            if (!hasUploadElements) results.not_applicable["HWG-UPLOAD-01"] = "Keine Dateiupload-Elemente vorhanden.";
            else if (deficientUploads.length > 0) {{
                results.violations.push({{ rule: "HWG-UPLOAD-01", rule_id: "HWG-UPLOAD-01", severity: "major", message: `${{deficientUploads.length}} Upload-Element(e) unvollständig spezifiziert: ${{deficientUploads.slice(0, 3).join(', ')}}.` }});
                results.score -= penalties.major;
            }} else results.passed.push("HWG-UPLOAD-01 (Uploads spezifiziert)");

            if (structuredFieldsUnvalidated.length > 0) {{
                results.violations.push({{ rule: "HWG-VAL-01", rule_id: "HWG-VAL-01", severity: "major", message: `Strukturierte Felder ohne gültigen Validator / Regex: ${{structuredFieldsUnvalidated.slice(0, 4).join(', ')}}.` }});
                results.score -= penalties.major;
            }} else results.passed.push("HWG-VAL-01 (Strukturierte Felder validiert)");

            if (!hasCompactFields) results.not_applicable["HWG-UX-01"] = "Keine Kompaktfelder (PLZ/Hausnummer) vorhanden.";
            else if (compactFieldsUnconstrained.length > 0) {{
                results.violations.push({{ rule: "HWG-UX-01", rule_id: "HWG-UX-01", severity: "minor", message: `Kompakte Felder über 100% Breite gestreckt: ${{compactFieldsUnconstrained.join(', ')}}.` }});
                results.score -= penalties.minor;
            }} else results.passed.push("HWG-UX-01 (Kompakte Feldbreiten eingehalten)");

            if (!workflowStates || workflowStates.length === 0) {{
                results.violations.push({{ rule: "HWG-WF-01", rule_id: "HWG-WF-01", severity: "minor", message: "Keine expliziten Status-Knoten (FC_CHANGE_STATE) im Workflow hinterlegt." }});
                results.score -= penalties.minor;
            }} else {{
                const canonicalRoots = ["eingegangen", "in prüfung", "in bearbeitung", "nachforderung", "genehmigt", "abgelehnt", "archiviert", "abgeschlossen"];
                const nonCan = workflowStates.filter(s => !canonicalRoots.some(r => s.toLowerCase().trim().includes(r)));
                if (nonCan.length > 0) {{
                    results.violations.push({{ rule: "HWG-WF-01", rule_id: "HWG-WF-01", severity: "minor", message: `Ad-hoc-Workflow-Status gefunden: [${{nonCan.join(', ')}}].` }});
                    results.score -= penalties.minor;
                }} else results.passed.push("HWG-WF-01 (Kanonische Workflow-Status)");
            }}

            const aliasToks = ["%$project_alias%", "%$record_id%", "%$vorgang", "[%$id%]"];
            const hasAlias = (workflowEmails || []).some(em => aliasToks.some(t => (`${{em.subject || ""}} ${{em.body || ""}}`).toLowerCase().includes(t)));
            if (!workflowEmails || workflowEmails.length === 0 || !hasAlias) {{
                results.violations.push({{ rule: "HWG-WF-02", rule_id: "HWG-WF-02", severity: "minor", message: "Fehlender dynamischer Vorgangsplatzhalter ([%$PROJECT_ALIAS%]) in Workflow-E-Mails." }});
                results.score -= penalties.minor;
            }} else results.passed.push("HWG-WF-02 (Vorgangsreferenz vorhanden)");

            // Stufe 2: Echte LLM-API-Prüfung (sofern API-Key im UI hinterlegt), sonst explizite Kennzeichnung als KI-ungeprüft!
            const llmCfg = getLlmUiConfig();
            if (!llmCfg.apiKey) {{
                const reason = "Keine LLM-API angebunden (kein API-Schlüssel für Stufe 2 hinterlegt).";
                SEMANTIC_RULE_IDS.forEach(rid => {{
                    results.unverified_semantic.push(rid);
                    results.not_applicable[rid] = `KI-Prüfung ausstehend: Diese semantische Regel wurde NICHT durch ein Sprachmodell geprüft. Grund: ${{reason}}`;
                }});
                results.llm_evaluation = {{
                    evaluated: false,
                    status: 'unconfigured',
                    api_base: llmCfg.apiBase,
                    model: llmCfg.model,
                    reason,
                    unverified_rules: [...SEMANTIC_RULE_IDS]
                }};
            }} else {{
                try {{
                    const semRules = registry.rules.filter(r => ['semantic', 'hybrid'].includes(r.evaluation_type));
                    const uiCompact = items.map(it => {{
                        const p = it.properties || {{}};
                        return {{
                            className: it.className || '',
                            name: p.name || '',
                            label_or_text: cleanVisibleText(p.label || p.text || p.rtevalue || p.heading || p.legend || '').slice(0, 200),
                            helptext: cleanVisibleText(p.helptext || p.help || p.tooltip || '').slice(0, 200)
                        }};
                    }}).filter(x => x.label_or_text || x.helptext);
                    const effPages = Math.max(1, rawXPageCount);
                    const prompt = `Prüfe das Formular '${{filename}}' anhand dieser 7 Regeln: ${{JSON.stringify(semRules)}}. Formular-Extrakt: ${{JSON.stringify({{ metrics: {{ page_count: effPages, input_field_count: applicantInputCount, ux02_complexity_threshold_reached: (effPages >= 3 || applicantInputCount >= 25) }}, ui_elements: uiCompact, workflow_emails: workflowEmails }})}}. Antworte NUR mit JSON: {{"form_name":"${{filename}}","evaluated_rules":[{{"rule_id":"HWG-...","status":"PASS|VIOLATION|RECOMMENDATION|NOT_APPLICABLE","severity":"major|minor|recommendation","affected_elements":[],"finding":"...","remediation_suggestion":"..."}}]}}`;

                    const endpoint = llmCfg.apiBase.endsWith('/chat/completions') ? llmCfg.apiBase : `${{llmCfg.apiBase}}/chat/completions`;
                    const resp = await fetch(endpoint, {{
                        method: 'POST',
                        headers: {{ 'Content-Type': 'application/json', 'Authorization': `Bearer ${{llmCfg.apiKey}}` }},
                        body: JSON.stringify({{ model: llmCfg.model, temperature: 0, messages: [{{ role: 'user', content: prompt }}] }})
                    }});
                    if (!resp.ok) throw new Error(`HTTP ${{resp.status}}`);
                    const rjson = await resp.json();
                    let rawContent = (((rjson.choices || [{{}}])[0].message || {{}}).content || '').replace(/<think>[\\s\\S]*?<\\/think>/gi, '').trim();
                    const sIdx = rawContent.indexOf('{{');
                    const eIdx = rawContent.lastIndexOf('}}');
                    const parsed = JSON.parse(rawContent.slice(sIdx, eIdx + 1));
                    const ruleMap = Object.fromEntries(registry.rules.map(r => [r.id, r]));
                    const seen = new Set();
                    (parsed.evaluated_rules || []).forEach(ent => {{
                        const rid = ent.rule_id || ent.rule;
                        if (!SEMANTIC_RULE_IDS.includes(rid) || seen.has(rid)) return;
                        seen.add(rid);
                        const st = String(ent.status || '').toUpperCase();
                        const sev = ruleMap[rid].severity;
                        const msg = `[KI-Befund · ${{llmCfg.model}}] ${{ent.finding || ''}}`;
                        if (st === 'VIOLATION') {{
                            if (sev === 'recommendation') results.recommendations.push({{ rule: rid, rule_id: rid, severity: 'recommendation', message: msg }});
                            else {{
                                results.violations.push({{ rule: rid, rule_id: rid, severity: sev, message: msg }});
                                results.score -= (penalties[sev] || 0);
                            }}
                        }} else if (st === 'RECOMMENDATION') {{
                            results.recommendations.push({{ rule: rid, rule_id: rid, severity: 'recommendation', message: msg }});
                        }} else if (st === 'PASS') {{
                            results.passed.push(`${{rid}} (${{ent.finding || 'KI-Prüfung bestanden'}})`);
                        }} else {{
                            results.not_applicable[rid] = msg;
                        }}
                    }});
                    SEMANTIC_RULE_IDS.forEach(rid => {{
                        if (!seen.has(rid)) {{
                            results.unverified_semantic.push(rid);
                            results.not_applicable[rid] = `KI-Prüfung unvollständig: Keine Bewertung für ${{rid}} erhalten.`;
                        }}
                    }});
                    results.llm_evaluation = {{
                        evaluated: results.unverified_semantic.length === 0,
                        status: 'ok',
                        api_base: llmCfg.apiBase,
                        model: llmCfg.model,
                        reason: `Semantische Prüfung über ${{llmCfg.model}} abgeschlossen.`,
                        unverified_rules: results.unverified_semantic
                    }};
                }} catch (apiErr) {{
                    const reason = `LLM-API-Aufruf fehlgeschlagen (${{apiErr.message}}).`;
                    SEMANTIC_RULE_IDS.forEach(rid => {{
                        results.unverified_semantic.push(rid);
                        results.not_applicable[rid] = `KI-Prüfung ausgefallen: ${{reason}}`;
                    }});
                    results.llm_evaluation = {{
                        evaluated: false,
                        status: 'error',
                        api_base: llmCfg.apiBase,
                        model: llmCfg.model,
                        reason,
                        unverified_rules: [...SEMANTIC_RULE_IDS]
                    }};
                }}
            }}

            results.score = Math.max(0, results.score);
            return results;
        }}

        async function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;
            activePresetKey = null;
            const llmCfg = getLlmUiConfig();

            try {{
                const headers = {{ 'X-File-Name': encodeURIComponent(file.name) }};
                if (llmCfg.apiKey) headers['X-LLM-Api-Key'] = llmCfg.apiKey;
                if (llmCfg.apiBase) headers['X-LLM-Api-Base'] = llmCfg.apiBase;
                if (llmCfg.model) headers['X-LLM-Model'] = llmCfg.model;

                const response = await fetch('/api/evaluate', {{
                    method: 'POST',
                    headers,
                    body: file
                }});
                if (response.ok) {{
                    currentEval = await response.json();
                    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                    renderEvaluation();
                    return;
                }}
            }} catch (netErr) {{
                console.log("Backend API not reachable, falling back to browser in-memory evaluation:", netErr);
            }}

            try {{
                if (file.name.toLowerCase().endsWith('.xfp')) {{
                    if (typeof JSZip === 'undefined') {{
                        alert("JSZip-Bibliothek nicht geladen.");
                        return;
                    }}
                    const zip = await JSZip.loadAsync(file);
                    let fcpData = null;
                    const emails = [];
                    const states = [];
                    for (const [relPath, zipEntry] of Object.entries(zip.files)) {{
                        if (relPath.endsWith('.fcp') && !fcpData) {{
                            const text = await zipEntry.async('string');
                            fcpData = JSON.parse(text);
                        }} else if (relPath.endsWith('.fcexport') && (relPath.includes('/projects/') || relPath.includes('\\\\projects\\\\')) && !relPath.includes('idcheck') && !relPath.includes('versions')) {{
                            const text = await zipEntry.async('string');
                            try {{ extractWorkflowClient(JSON.parse(text), emails, states); }} catch (e) {{}}
                        }}
                    }}
                    if (fcpData) {{
                        currentEval = await evaluateFormDataClient(fcpData, file.name, emails, states);
                        document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                        renderEvaluation();
                        return;
                    }}
                }} else if (file.name.toLowerCase().endsWith('.json')) {{
                    const text = await file.text();
                    const data = JSON.parse(text);
                    currentEval = await evaluateFormDataClient(data, file.name, data.workflow_emails || [], data.workflow_states || []);
                    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                    renderEvaluation();
                    return;
                }}
            }} catch (err) {{
                console.error("Client parsing error:", err);
                alert("Datei konnte nicht verarbeitet werden: " + err.message);
            }}
        }}

        window.onload = function() {{
            initPresets();
            renderEvaluation();
        }};
    </script>
</body>
</html>
"""

    with open("web/compliance_dashboard.html", "w", encoding="utf-8") as f:
        f.write(html_content)
    print("Dashboard erfolgreich erstellt: web/compliance_dashboard.html")


if __name__ == "__main__":
    generate_dashboard()
