import json
import os
import sys

sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def generate_dashboard():
    with open("data/rules/rules_registry.json", "r", encoding="utf-8") as f:
        registry = json.load(f)
        
    with open("data/test_forms/synthetic_compliant_form.json", "r", encoding="utf-8") as f:
        synth_comp = json.load(f)
        
    with open("data/test_forms/synthetic_noncompliant_form.json", "r", encoding="utf-8") as f:
        synth_noncomp = json.load(f)

    # We also run test_rule_engine to get cached results for the 5 forms
    from test_rule_engine import evaluate_form
    
    presets = {
        "synth_comp": {
            "name": "Synthetisches Referenzformular (Best-Practice)",
            "file": "data/test_forms/synthetic_compliant_form.json",
            "eval": evaluate_form("data/test_forms/synthetic_compliant_form.json", registry)
        },
        "synth_noncomp": {
            "name": "Synthetisches Negativformular (Worst-Case)",
            "file": "data/test_forms/synthetic_noncompliant_form.json",
            "eval": evaluate_form("data/test_forms/synthetic_noncompliant_form.json", registry)
        },
        "auslagen": {
            "name": "Reales Formular: Auslagenerstattung (Finanzen)",
            "file": "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
            "eval": evaluate_form("data/raw_forms/prod/Auslagenerstattung _20260929.xfp", registry)
        },
        "sprints": {
            "name": "Reales Formular: Antrag-Sprints Drittmittel (ZFK)",
            "file": "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
            "eval": evaluate_form("data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp", registry)
        },
        "master": {
            "name": "Reales Formular: Master-Formular (Campus Management)",
            "file": "data/raw_forms/test/adminformulare/Master-Formular.xfp",
            "eval": evaluate_form("data/raw_forms/test/adminformulare/Master-Formular.xfp", registry)
        }
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
            --shadow-lg: 0 10px 15px -3px rgb(0 0 0 / 0.1), 0 4px 6px -4px rgb(0 0 0 / 0.1);
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
            padding: 24px 32px;
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
            font-size: 22px;
            font-weight: 700;
            letter-spacing: -0.3px;
        }}

        .brand-text p {{
            font-size: 13px;
            color: rgba(255, 255, 255, 0.8);
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

        .btn-light:hover {{
            background: rgba(255, 255, 255, 0.25);
        }}

        .btn-primary {{
            background: var(--hwg-blue);
            color: white;
        }}

        .btn-primary:hover {{
            background: var(--hwg-blue-light);
        }}

        .btn-print {{
            background: white;
            color: var(--hwg-blue);
            font-weight: 600;
        }}

        .btn-print:hover {{
            background: var(--slate-100);
        }}

        main {{
            max-width: 1200px;
            margin: 32px auto;
            padding: 0 24px;
        }}

        /* Control Panel */
        .card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            box-shadow: var(--shadow-sm);
            margin-bottom: 24px;
            overflow: hidden;
        }}

        .card-header {{
            padding: 18px 24px;
            border-bottom: 1px solid var(--slate-200);
            background: white;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }}

        .card-header h2 {{
            font-size: 16px;
            font-weight: 700;
            color: var(--slate-900);
        }}

        .card-body {{
            padding: 24px;
        }}

        /* Preset selector */
        .preset-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fill, minmax(210px, 1fr));
            gap: 12px;
            margin-bottom: 20px;
        }}

        .preset-btn {{
            background: var(--slate-50);
            border: 1.5px solid var(--slate-200);
            border-radius: var(--radius-lg);
            padding: 12px 14px;
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
        }}

        .score-good {{ background: #dcfce7; color: var(--hwg-green); }}
        .score-mid {{ background: #fef9c3; color: #854d0e; }}
        .score-poor {{ background: #fee2e2; color: var(--hwg-red); }}

        /* Drag & Drop Area */
        .dropzone {{
            border: 2px dashed var(--slate-300);
            border-radius: var(--radius-lg);
            padding: 24px;
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
            font-size: 13px;
            color: var(--slate-600);
            margin-top: 6px;
        }}

        /* Summary Dashboard */
        .dashboard-grid {{
            display: grid;
            grid-template-columns: 280px 1fr;
            gap: 24px;
            margin-bottom: 24px;
        }}

        @media (max-width: 860px) {{
            .dashboard-grid {{
                grid-template-columns: 1fr;
            }}
        }}

        .score-card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            padding: 24px;
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            text-align: center;
            box-shadow: var(--shadow-sm);
        }}

        .gauge-container {{
            position: relative;
            width: 170px;
            height: 170px;
            margin-bottom: 16px;
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
            font-size: 40px;
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
            font-size: 13px;
            font-weight: 700;
            margin-top: 8px;
        }}

        .stats-grid {{
            display: grid;
            grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
            gap: 16px;
        }}

        .stat-card {{
            background: white;
            border-radius: var(--radius-xl);
            border: 1px solid var(--slate-200);
            padding: 20px;
            box-shadow: var(--shadow-sm);
            display: flex;
            flex-direction: column;
            justify-content: space-between;
        }}

        .stat-header {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            margin-bottom: 12px;
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

        /* Filter Pills */
        .filter-bar {{
            display: flex;
            gap: 8px;
            margin-bottom: 18px;
            overflow-x: auto;
            padding-bottom: 4px;
        }}

        .filter-pill {{
            background: white;
            border: 1px solid var(--slate-300);
            border-radius: 999px;
            padding: 6px 16px;
            font-size: 13px;
            font-weight: 600;
            color: var(--slate-700);
            cursor: pointer;
            transition: all 0.15s ease;
            white-space: nowrap;
        }}

        .filter-pill:hover {{
            background: var(--slate-100);
        }}

        .filter-pill.active {{
            background: var(--hwg-blue);
            color: white;
            border-color: var(--hwg-blue);
        }}

        /* Rule Cards */
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
        .rule-card.rule-passed {{ border-left: 5px solid var(--hwg-green); opacity: 0.9; }}

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
        }}

        .badge-critical {{ background: var(--hwg-red-subtle); color: var(--hwg-red); }}
        .badge-major {{ background: #fff7ed; color: #ea580c; }}
        .badge-minor {{ background: var(--hwg-gold-subtle); color: #854d0e; }}
        .badge-recommendation {{ background: var(--hwg-blue-subtle); color: var(--hwg-blue); }}
        .badge-passed {{ background: var(--hwg-green-subtle); color: var(--hwg-green); }}

        .rule-message {{
            font-size: 14px;
            color: var(--slate-800);
            margin-bottom: 14px;
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

        /* Print styles */
        @media print {{
            header, .card:first-child, .filter-bar, .btn-print {{
                display: none !important;
            }}
            body {{
                background: white;
                color: black;
            }}
            main {{
                margin: 0;
                padding: 0;
                max-width: 100%;
            }}
            .card {{
                box-shadow: none;
                border: none;
            }}
            .rule-card {{
                page-break-inside: avoid;
                border: 1px solid #ccc;
                box-shadow: none;
                margin-bottom: 12px;
            }}
            .print-header {{
                display: block !important;
                margin-bottom: 24px;
                border-bottom: 2px solid #003366;
                padding-bottom: 12px;
            }}
        }}

        .print-header {{
            display: none;
        }}
    </style>
</head>
<body>

    <header>
        <div class="header-container">
            <div class="brand-section">
                <div class="brand-badge">HWG LU</div>
                <div class="brand-text">
                    <h1>Formcycle Compliance Checker</h1>
                    <p>Wissenschaftliches Governance-, Usability- & Barrierefreiheits-Audit (v1.5.0)</p>
                </div>
            </div>
            <div class="header-actions">
                <button class="btn btn-print" onclick="window.print()">
                    <svg width="16" height="16" fill="currentColor" viewBox="0 0 16 16"><path d="M2.5 8a.5.5 0 1 0 0-1 .5.5 0 0 0 0 1z"/><path d="M5 1a2 2 0 0 0-2 2v2H2a2 2 0 0 0-2 2v3a2 2 0 0 0 2 2h1v1a2 2 0 0 0 2 2h6a2 2 0 0 0 2-2v-1h1a2 2 0 0 0 2-2V7a2 2 0 0 0-2-2h-1V3a2 2 0 0 0-2-2H5zM4 3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1v2H4V3zm1 5a2 2 0 0 0-2 2v1H2a1 1 0 0 1-1-1V7a1 1 0 0 1 1-1h12a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v-1a2 2 0 0 0-2-2H5zm7 2v3a1 1 0 0 1-1 1H5a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h6a1 1 0 0 1 1 1z"/></svg>
                    Prüfbericht drucken / PDF
                </button>
                <button class="btn btn-light" onclick="exportAuditJSON()">
                    JSON-Audit
                </button>
            </div>
        </div>
    </header>

    <main>
        <!-- Print Header -->
        <div class="print-header">
            <h2>Hochschule für Wirtschaft und Gesellschaft Ludwigshafen</h2>
            <h3>Formcycle Compliance- und Barrierefreiheits-Prüfbericht</h3>
            <p id="printMeta">Formular: - | Datum: <span id="printDate"></span> | Registry v1.5.0</p>
        </div>

        <!-- Benchmark Presets & Ingestion -->
        <div class="card">
            <div class="card-header">
                <h2>1. Formular-Auswahl & Ingestion (.xfp / .json)</h2>
                <span style="font-size: 12px; color: var(--slate-600);">21 Governance-Regeln aktiv</span>
            </div>
            <div class="card-body">
                <div style="font-size: 13px; font-weight: 600; color: var(--slate-700); margin-bottom: 8px;">
                    Benchmark-Formulare der HWG Ludwigshafen testen:
                </div>
                <div class="preset-grid" id="presetGrid">
                    <!-- populated by JS -->
                </div>

                <div class="dropzone" id="dropzone" onclick="document.getElementById('fileInput').click()">
                    <input type="file" id="fileInput" accept=".json,.xfp" style="display: none" onchange="handleFileUpload(event)">
                    <svg width="32" height="32" fill="none" stroke="currentColor" stroke-width="2" viewBox="0 0 24 24" style="color: var(--hwg-blue); margin-bottom: 6px;"><path stroke-linecap="round" stroke-linejoin="round" d="M7 16a4 4 0 01-.88-7.903A5 5 0 1115.9 6L16 6a5 5 0 011 9.9M15 13l-3-3m0 0l-3 3m3-3v12"/></svg>
                    <div style="font-size: 14px; font-weight: 600; color: var(--slate-800);">Formcycle-Exportdatei hier ablegen oder klicken</div>
                    <p>Unterstützt extrahierte Formular-JSONs oder XFP-Archivdaten</p>
                </div>
            </div>
        </div>

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
                <p id="currentFormName" style="font-size: 12px; color: var(--slate-600); margin-top: 10px; word-break: break-all;">-</p>
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
                    <div class="stat-sub" id="passRateSub">von 22 Kriterien</div>
                </div>
            </div>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar" id="filterBar">
            <button class="filter-pill active" onclick="setFilter('all')">Alle Kriterien (<span id="pillAll">22</span>)</button>
            <button class="filter-pill" onclick="setFilter('critical')">Kritisch (<span id="pillCritical">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('major')">Major (<span id="pillMajor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('minor')">Minor (<span id="pillMinor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('recommendation')">Empfehlungen (<span id="pillRec">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('passed')">Bestanden (<span id="pillPassed">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('na')">Nicht zutreffend (<span id="pillNA">0</span>)</button>
        </div>

        <!-- Rule Details List -->
        <div class="rules-list" id="rulesList">
            <!-- populated by JS -->
        </div>
    </main>

    <script>
        const registry = {registry_json};
        const presets = {presets_json};

        let currentEval = presets.auslagen.eval;
        let currentFilter = 'all';

        document.getElementById('printDate').innerText = new Date().toLocaleDateString('de-DE');

        function initPresets() {{
            const grid = document.getElementById('presetGrid');
            grid.innerHTML = '';
            for (const [key, p] of Object.entries(presets)) {{
                const btn = document.createElement('div');
                btn.className = `preset-btn ${{key === 'auslagen' ? 'active' : ''}}`;
                btn.id = `preset-${{key}}`;
                
                const score = p.eval.score;
                let scoreClass = 'score-poor';
                if (score >= 80) scoreClass = 'score-good';
                else if (score >= 50) scoreClass = 'score-mid';

                btn.innerHTML = `
                    <div class="preset-btn-title">
                        <span>${{escapeHtml(p.name.split(':')[1] || p.name)}}</span>
                        <span class="preset-score-pill ${{scoreClass}}">${{score}} P</span>
                    </div>
                    <div class="preset-btn-desc">${{escapeHtml(p.eval.form)}}</div>
                `;
                btn.onclick = () => selectPreset(key);
                grid.appendChild(btn);
            }}
        }}

        function selectPreset(key) {{
            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
            const activeBtn = document.getElementById(`preset-${{key}}`);
            if (activeBtn) activeBtn.classList.add('active');
            
            currentEval = presets[key].eval;
            renderEvaluation();
        }}

        function renderEvaluation() {{
            const e = currentEval;
            document.getElementById('currentFormName').innerText = e.form;
            document.getElementById('printMeta').innerText = `Formular: ${{e.form}} | Datum: ${{new Date().toLocaleDateString('de-DE')}} | Registry v${{registry.version}}`;

            // Score gauge
            const score = e.score;
            document.getElementById('scoreValue').innerText = score;
            
            // Circle radius = 70 => circumference = 2 * PI * 70 = 439.82
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

            // Count severities
            let criticals = 0, majors = 0, minors = 0, recs = (e.recommendations || []).length;
            (e.violations || []).forEach(v => {{
                if (v.severity === 'critical') criticals++;
                else if (v.severity === 'major') majors++;
                else if (v.severity === 'minor') minors++;
            }});

            const passedCount = (e.passed || []).length;
            const naCount = Object.keys(e.not_applicable || {{}}).length;
            document.getElementById('countCritical').innerText = criticals;
            document.getElementById('countMajor').innerText = majors;
            document.getElementById('countMinor').innerText = minors;
            document.getElementById('countPassed').innerText = passedCount;

            document.getElementById('pillAll').innerText = registry.rules.length;
            document.getElementById('pillCritical').innerText = criticals;
            document.getElementById('pillMajor').innerText = majors;
            document.getElementById('pillMinor').innerText = minors;
            document.getElementById('pillRec').innerText = recs;
            document.getElementById('pillPassed').innerText = passedCount;
            const pillNA = document.getElementById('pillNA');
            if (pillNA) pillNA.innerText = naCount;

            renderRuleCards();
        }}

        function setFilter(filter) {{
            currentFilter = filter;
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            if (event && event.target) event.target.classList.add('active');
            renderRuleCards();
        }}

        function escapeHtml(str) {{
            if (!str) return '';
            return String(str)
                .replace(/&/g, '&amp;')
                .replace(/</g, '&lt;')
                .replace(/>/g, '&gt;')
                .replace(/"/g, '&quot;')
                .replace(/'/g, '&#039;');
        }}

        function renderRuleCards() {{
            const container = document.getElementById('rulesList');
            container.innerHTML = '';

            const violationsMap = {{}};
            (currentEval.violations || []).forEach(v => {{ violationsMap[v.rule] = v; }});
            const recMap = {{}};
            (currentEval.recommendations || []).forEach(r => {{ recMap[r.rule] = r; }});
            
            const passedSet = new Set((currentEval.passed || []).map(p => p.split(' ')[0]));

            registry.rules.forEach(rule => {{
                const isViolation = !!violationsMap[rule.id];
                const isRec = !!recMap[rule.id];
                const isPassed = passedSet.has(rule.id);
                const isNotApplicable = !isViolation && !isRec && !isPassed;

                // Filter check
                if (currentFilter === 'critical' && (!isViolation || violationsMap[rule.id].severity !== 'critical')) return;
                if (currentFilter === 'major' && (!isViolation || violationsMap[rule.id].severity !== 'major')) return;
                if (currentFilter === 'minor' && (!isViolation || violationsMap[rule.id].severity !== 'minor')) return;
                if (currentFilter === 'recommendation' && !isRec) return;
                if (currentFilter === 'passed' && !isPassed) return;
                if (currentFilter === 'na' && !isNotApplicable) return;

                const card = document.createElement('div');
                let cardClass = 'rule-card';
                let badgeHtml = '';
                let messageHtml = '';

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
                }} else {{
                    cardClass += ' rule-na';
                    badgeHtml = `<span class="badge" style="background: var(--slate-100); color: var(--slate-600); border: 1px solid var(--slate-300);">NICHT ZUTREFFEND</span>`;
                    const naReason = (currentEval.not_applicable && currentEval.not_applicable[rule.id])
                        ? currentEval.not_applicable[rule.id]
                        : 'Kriterium auf diesen Formularkontext nicht anwendbar.';
                    messageHtml = `<div class="rule-message" style="color: var(--slate-600);">${{escapeHtml(naReason)}}</div>`;
                }}

                card.className = cardClass;
                card.innerHTML = `
                    <div class="rule-top">
                        <div class="rule-id-name">
                            <span class="rule-id">${{escapeHtml(rule.id)}}</span>
                            <span class="rule-name">${{escapeHtml(rule.name)}}</span>
                        </div>
                        ${{badgeHtml}}
                    </div>
                    ${{messageHtml}}
                    <div class="remediation-box">
                        <div class="remediation-title">
                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3.5a.5.5 0 0 1-.5-.5v-4A.5.5 0 0 1 8 4z"/></svg>
                            Klickpfad im XIMA Formcycle Designer (Remediation):
                        </div>
                        <div class="remediation-text">${{escapeHtml(rule.remediation)}}</div>
                    </div>
                    <div class="rationale-text">Theoretische & regulatorische Fundierung: ${{escapeHtml(rule.rationale)}}</div>
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
                        name: obj.name || '',
                        subject: cp.subject || '',
                        body: cp.body || ''
                    }});
                }} else if (['FC_CHANGE_STATE', 'CUSTOM', 'RECEIVED'].includes(obj.type)) {{
                    const st = obj.name || '';
                    if (st && st !== 'FC_CHANGE_STATE' && !states.includes(st)) {{
                        states.push(st);
                    }}
                }}
                for (const k in obj) {{
                    extractWorkflowClient(obj[k], emails, states);
                }}
            }}
        }}

        function evaluateFormDataClient(formData, filename, workflowEmails, workflowStates) {{
            const results = {{
                form: filename,
                violations: [],
                recommendations: [],
                passed: [],
                not_applicable: {{}},
                score: 100
            }};

            const items = formData.items || [];
            const formProps = formData.properties || {{}};
            const penalties = registry.scoring.severity_penalties;

            const widths = new Set();
            if (formProps.maxwidth) widths.add(String(formProps.maxwidth));

            let hasImage = false;
            let imageProps = {{}};
            let hasHeaderTitleH1 = false;
            let headerTitleDetails = null;
            let hasFieldset = false;
            let footerShowsLogo = false;

            let requiredFieldsTotal = 0;
            const missingRequiredHints = [];
            const manualAsterisksInLabels = [];
            const htmlInLabels = [];
            const devNotes = [];
            const buttonLabels = [];
            const navButtonLabels = [];
            let hasSaveButton = false;

            let pageCount = 0;
            let inputFieldCount = 0;
            const inputClasses = new Set([
                "XTextField", "XTextArea", "XSelect", "XCheckbox", 
                "XUpload", "XFile", "XRadio", "XDate", "XNumber"
            ]);

            const personalFieldsSequence = [];
            let hasPersonalData = false;
            let hasDsgvoNotice = false;
            const uploadElements = [];
            let hasUploadElements = false;
            const structuredFieldsUnvalidated = [];
            const compactFieldsUnconstrained = [];
            let hasCompactFields = false;
            const jargonWithoutHelp = [];
            const longSentences = [];

            const jargonCatalog = [
                "gstb", "kostenstelle", "vergabevermerk", "remonstration", 
                "promotionsausschuss", "exmatrikulation", "shibboleth", "ldap",
                "kap", "mittelbewirtschafter", "mittelgeber", "verausgabt", 
                "verausgabung", "zfk", "haushaltsstelle", "bewilligungszeitraum", 
                "titelgruppe", "drittmittel"
            ];

            items.forEach(it => {{
                const c = it.className || "";
                const props = it.properties || {{}};
                const name = String(props.name || "").toLowerCase();
                const rawLbl = String(props.label || props.text || props.heading || "");
                const lblClean = rawLbl.replace(/<[^>]+>/g, " ").trim();
                const lblLower = lblClean.toLowerCase();
                const helpText = String(props.help || props.tooltip || props.description || "").toLowerCase();

                if (c === "XPage") pageCount++;
                if (inputClasses.has(c)) inputFieldCount++;

                if (props.maxwidth) widths.add(String(props.maxwidth));

                if (c === "XImage") {{
                    hasImage = true;
                    imageProps = props;
                }}

                const parentId = String(props.parentid || "").toLowerCase();
                const rte = String(props.rtevalue || "");
                const heading = String(props.heading || "");
                const label = String(props.label || "");
                const text = String(props.text || "");
                const lvl = String(props.headinglevel || "");
                const isHeader = parentId.includes("header") || c === "XHeader" || name.includes("header");
                const allHeading = `${{rte}} ${{heading}} ${{label}} ${{text}}`.toLowerCase();

                if (isHeader || name.includes("header") || name.includes("titel") || name.includes("title")) {{
                    if (allHeading.includes("<h1") || lvl === "1") {{
                        hasHeaderTitleH1 = true;
                    }} else if (allHeading.includes("<h2") || allHeading.includes("<h3") || allHeading.includes("antrag") || name.includes("title") || name.includes("titel")) {{
                        if (!hasHeaderTitleH1) headerTitleDetails = "h2_or_text";
                    }}
                }}

                if (c === "XFooter") {{
                    if (String(props.showlogo || "0") === "1") footerShowsLogo = true;
                }}

                if (c === "XFieldSet") hasFieldset = true;

                if (inputClasses.has(c)) {{
                    const isReq = String(props.required || "0") === "1";
                    const showHint = String(props.showrequiredhint || "1");
                    if (isReq) {{
                        requiredFieldsTotal++;
                        if (showHint === "0") missingRequiredHints.push(props.name || "unnamed");
                    }} else if (lblClean.includes("*")) {{
                        manualAsterisksInLabels.push(props.name || "unnamed");
                    }}
                }}

                ["label", "text", "heading"].forEach(lk => {{
                    if (props[lk]) {{
                        const val = String(props[lk]);
                        const cleanVal = val.replace(/\\s+/g, " ").trim();
                        if (/<[^>]+>/.test(val) || /&[a-zA-Z0-9#]+;/.test(val) || val.includes("|")) {{
                            htmlInLabels.push([props.name || "unnamed", cleanVal.slice(0, 35)]);
                        }}
                        if (["JavaScript", "Shibboleth", "LDAP-Member", "Postfach-SB"].some(t => val.includes(t))) {{
                            devNotes.push([props.name || "unnamed", cleanVal.slice(0, 40)]);
                        }}
                    }}
                }});

                if (c.includes("Button") || c === "XButtonList") {{
                    if (Array.isArray(props.buttons)) {{
                        props.buttons.forEach(b => {{
                            const val = b.value || b.text || b.title || "";
                            if (val) {{
                                buttonLabels.push([props.name || "btn", val]);
                                if ((b.action && ["next", "prev"].includes(b.action.page)) || ["weiter", "zurück", "zurueck"].some(s => val.toLowerCase().includes(s))) {{
                                    navButtonLabels.push(val);
                                }}
                            }}
                        }});
                    }}
                    const btnLbl = props.text || props.label || props.value || "";
                    if (btnLbl) {{
                        buttonLabels.push([props.name || "btn", btnLbl]);
                        if (["weiter", "zurück", "zurueck"].some(s => btnLbl.toLowerCase().includes(s))) {{
                            navButtonLabels.push(btnLbl);
                        }}
                    }}
                    if (Array.isArray(props.items)) {{
                        props.items.forEach(b => {{
                            const val = (typeof b === "object" ? (b.text || b.value || b.title) : b) || "";
                            if (val) buttonLabels.push([props.name || "btn", val]);
                        }});
                    }}
                }}

                if (inputClasses.has(c)) {{
                    const elemName = props.name || "unnamed";
                    if (["anrede", "salutation"].some(t => name.includes(t) || lblLower.includes(t))) {{
                        personalFieldsSequence.push(["anrede", elemName, lblClean || "Anrede", 1]);
                    }} else if (name.includes("vorname") || lblLower.includes("vorname")) {{
                        personalFieldsSequence.push(["vorname", elemName, lblClean || "Vorname", 2]);
                    }} else if (name.includes("nachname") || lblLower.includes("nachname") || (name.includes("name") && !["vorname", "antrag", "bank", "kredit", "projekt", "programm", "foerder", "titel", "datei"].some(t => name.includes(t)))) {{
                        personalFieldsSequence.push(["nachname", elemName, lblClean || "Nachname", 3]);
                    }} else if (lblClean.toLowerCase() === "name" || lblLower.includes("name antragstellende") || lblLower.includes("name antragsteller")) {{
                        personalFieldsSequence.push(["nachname", elemName, lblClean || "Nachname", 3]);
                    }} else if (["email", "e-mail", "mail"].some(t => name.includes(t) || lblLower.includes(t))) {{
                        personalFieldsSequence.push(["email", elemName, lblClean || "E-Mail-Adresse", 4]);
                    }} else if (["telefon", "telefonnummer", "phone", "mobil"].some(t => name.includes(t) || lblLower.includes(t))) {{
                        personalFieldsSequence.push(["telefon", elemName, lblClean || "Telefonnummer", 5]);
                    }}
                }}

                if (["vorname", "nachname", "name", "email", "e-mail", "matrikel", "geburtsdatum", "iban", "anschrift"].some(t => name.includes(t) || lblLower.includes(t))) {{
                    hasPersonalData = true;
                }}
                const rawDsgvoCtx = (lblLower + " " + helpText + " " + String(props.rtevalue || "").toLowerCase() + " " + String(props.html || "").toLowerCase());
                if (["datenschutz", "dsgvo", "datenverarbeitung", "datenschutzerklärung", "hwg-lu.de"].some(t => rawDsgvoCtx.includes(t))) {{
                    hasDsgvoNotice = true;
                }}
                if (c === "XFooter" && String(props.privacyPolicyShow || "0") === "1") {{
                    hasDsgvoNotice = true;
                }}

                if (["XUpload", "XFile", "XUploadButton"].includes(c) || name.includes("upload")) {{
                    hasUploadElements = true;
                    const hasFormats = ["pdf", "jpg", "png", "zip", "format", "dateiformat"].some(fmt => lblLower.includes(fmt) || helpText.includes(fmt));
                    const hasSize = ["mb", "kb", "maximal", "größe", "dateigröße"].some(sz => lblLower.includes(sz) || helpText.includes(sz));
                    if (!hasFormats || !hasSize) {{
                        uploadElements.push({{ name: props.name || "upload", hasFormats, hasSize }});
                    }}
                }}

                if (["iban", "plz", "postleitzahl", "telefon", "geburtsdatum"].some(t => name.includes(t) || lblLower.includes(t))) {{
                    const valRule = props.validation || {{}};
                    const hasRegex = Boolean(props.pattern || valRule.regex || valRule.type);
                    if (!hasRegex) structuredFieldsUnvalidated.push(props.name || lblClean.slice(0, 15));
                }}

                if (["plz", "postleitzahl", "hausnummer", "hnr"].some(t => name.includes(t) || lblLower.includes(t))) {{
                    hasCompactFields = true;
                    const colWidth = props.colwidth || props.width;
                    if (["100%", "12", undefined, null].includes(colWidth) && !props.maxwidth) {{
                        compactFieldsUnconstrained.push(props.name || lblClean.slice(0, 15));
                    }}
                }}

                jargonCatalog.forEach(jg => {{
                    const matched = (jg.length <= 4) ? new RegExp('\\\\b' + jg + '\\\\b', 'i').test(lblLower) : lblLower.includes(jg);
                    if (matched && (!helpText || helpText.trim().length < 5)) {{
                        jargonWithoutHelp.push([jg, props.name || lblClean.slice(0, 15)]);
                    }}
                }});

                ["text", "help", "tooltip", "description", "rtevalue"].forEach(k => {{
                    const val = String(props[k] || "");
                    if (val) {{
                        const cleanT = val.replace(/<[^>]+>/g, " ");
                        cleanT.split(/[.!?]+/).forEach(sent => {{
                            const words = sent.trim().split(/\\s+/).filter(w => w.length > 1);
                            if (words.length > 25) {{
                                longSentences.push([props.name || "unnamed", words.length, words.slice(0, 8).join(" ") + "..."]);
                            }}
                        }});
                    }}
                }});
            }});

            buttonLabels.forEach(([bSource, bl]) => {{
                const lower = bl.toLowerCase();
                if (["zwischenspeichern", "speichern", "fortsetzen"].some(s => lower.includes(s))) {{
                    hasSaveButton = true;
                }}
            }});

            let hasWorkflowFeedback = false;
            (workflowEmails || []).forEach(em => {{
                const text = `${{em.subject || ""}} ${{em.body || ""}}`.toLowerCase();
                if (["vielen dank", "eingegangen", "geprüft", "prüfung", "entscheidung", "folgeschritte", "bearbeit", "rückmeldung", "vorgangsnummer", "project_alias"].some(t => text.includes(t))) {{
                    hasWorkflowFeedback = true;
                }}
            }});

            // 1. HWG-CD-01
            if (widths.has("700px") && !widths.has("850px")) {{
                results.violations.push({{ rule: "HWG-CD-01", severity: "major", message: "Formular verwendet veraltete 700px-Breite statt dem 850px-Standard." }});
                results.score -= penalties.major;
            }} else {{
                results.passed.push("HWG-CD-01 (Breite 850px eingehalten)");
            }}

            // 2. HWG-CD-02
            if (!hasImage) {{
                results.violations.push({{ rule: "HWG-CD-02", severity: "critical", message: "Kein offizielles HWG-Header-Banner (XImage) im Kopfbereich vorhanden." }});
                results.score -= penalties.critical;
            }} else {{
                const imgH = String(imageProps.imageheight || imageProps.height || "").trim().toLowerCase();
                const imgAlign = String(imageProps.textalign || imageProps.align || "").trim().toLowerCase();
                const isHeight60 = imgH === "60" || imgH === "60px";
                const isRight = imgAlign === "right" || imgAlign === "2";
                if (!isHeight60 || !isRight) {{
                    const issues = [];
                    if (!isHeight60) issues.push(`Höhe (in px) ist '${{imgH || "undefiniert"}}' statt 60px`);
                    if (!isRight) issues.push(`Ausrichtung ist '${{imgAlign || "links"}}' statt rechtsbündig`);
                    results.violations.push({{ rule: "HWG-CD-02", severity: "major", message: `HWG-Header-Logo weicht von den Formatvorgaben ab: ${{issues.join(", ")}}.` }});
                    results.score -= penalties.major;
                }} else {{
                    results.passed.push("HWG-CD-02 (Header-Logo mit 60px Höhe, rechtsbündig vorhanden)");
                }}
            }}

            // 3. HWG-CD-03
            if (footerShowsLogo) {{
                results.violations.push({{ rule: "HWG-CD-03", severity: "major", message: "Im Footer (XFooter) ist 'Logo anzeigen' (showlogo='1') aktiviert ('Powered by XIMA Formcycle')." }});
                results.score -= penalties.major;
            }} else {{
                results.passed.push("HWG-CD-03 (XIMA-Logo im Footer deaktiviert)");
            }}

            // 4. HWG-CD-04
            if (hasHeaderTitleH1) {{
                results.passed.push("HWG-CD-04 (Formulartitel im Header als H1 vorhanden)");
            }} else {{
                const msg = headerTitleDetails === "h2_or_text"
                    ? "Formulartitel im Header ist nicht als Überschrift erster Ordnung (H1) ausgezeichnet (gefunden: H2 oder Fließtext statt <h1>)."
                    : "Kein Formulartitel im Kopfbereich (Header) vorhanden. Der Antragstitel muss im Header als H1 deklariert werden.";
                results.violations.push({{ rule: "HWG-CD-04", severity: "major", message: msg }});
                results.score -= penalties.major;
            }}

            // 5. HWG-A11Y-01
            if (hasFieldset) {{
                results.passed.push("HWG-A11Y-01 (Fieldsets vorhanden: Semantische Gruppenbildung erfüllt)");
            }} else if (items.length > 20) {{
                results.violations.push({{ rule: "HWG-A11Y-01", severity: "critical", message: "Keine semantischen XFieldSet-Gruppierungen für Formularabschnitte vorhanden." }});
                results.score -= penalties.critical;
            }} else {{
                results.passed.push("HWG-A11Y-01 (Kompaktformular <= 20 Elemente: Keine Abschnittsbildung per Fieldset erforderlich)");
            }}

            // 6. HWG-A11Y-02
            if (missingRequiredHints.length > 0 || manualAsterisksInLabels.length > 0) {{
                const issues = [];
                if (missingRequiredHints.length > 0) issues.push(`Optischer Hinweis deaktiviert (showrequiredhint='0') in [${{missingRequiredHints.join(", ")}}]`);
                if (manualAsterisksInLabels.length > 0) issues.push(`Manuelles Sternchen (*) im Label ohne native Pflichtfeldfunktion in [${{manualAsterisksInLabels.join(", ")}}]`);
                results.violations.push({{ rule: "HWG-A11Y-02", severity: "major", message: `Pflichtfeld-Deklaration verletzt: ${{issues.join("; ")}}.` }});
                results.score -= penalties.major;
            }} else if (requiredFieldsTotal > 0) {{
                results.passed.push(`HWG-A11Y-02 (Pflichtfeld-Deklaration: ${{requiredFieldsTotal}} Pflichtfelder mit optischem Hinweis und barrierefreiem aria-required deklariert)`);
            }} else {{
                results.not_applicable["HWG-A11Y-02"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Pflichtfelder im Formular deklariert.";
            }}

            // 7. HWG-A11Y-03
            if (htmlInLabels.length > 0) {{
                const affected = htmlInLabels.map(h => h[0]);
                const preview = affected.slice(0, 6).join(", ") + (affected.length > 6 ? ` und ${{affected.length - 6}} weitere` : "");
                results.violations.push({{ rule: "HWG-A11Y-03", severity: "minor", message: `HTML-Fragmente oder Entities in ${{htmlInLabels.length}} Label(s) gefunden: [${{preview}}].` }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push("HWG-A11Y-03 (Saubere Labels ohne HTML-Fragmente und Entities)");
            }}

            // 8. HWG-STAMM-01
            if (personalFieldsSequence.length >= 2) {{
                const outOfOrder = [];
                for (let i = 0; i < personalFieldsSequence.length - 1; i++) {{
                    const curr = personalFieldsSequence[i];
                    const nxt = personalFieldsSequence[i + 1];
                    if (nxt[0] === "anrede" && (curr[0] === "email" || curr[0] === "telefon")) continue;
                    if (curr[3] > nxt[3]) {{
                        outOfOrder.push(`'${{curr[2]}}' (${{curr[0]}}) vor '${{nxt[2]}}' (${{nxt[0]}})`);
                    }}
                }}
                if (outOfOrder.length > 0) {{
                    results.violations.push({{ rule: "HWG-STAMM-01", severity: "major", message: `Inkonsistente Abfolge persönlicher Stammdaten: ${{outOfOrder.join(", ")}}. Erwartete Reihenfolge: Anrede -> Vorname -> Nachname -> E-Mail-Adresse -> Telefonnummer.` }});
                    results.score -= penalties.major;
                }} else {{
                    results.passed.push("HWG-STAMM-01 (Kanonische Stammdaten-Abfolge eingehalten)");
                }}
            }} else {{
                results.not_applicable["HWG-STAMM-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine oder weniger als 2 persönliche Stammdatenfelder vorhanden. Hinweis: Achten Sie bei der Erhebung von Stammdaten stets auf die kanonische Abfolge: Anrede -> Vorname -> Nachname -> E-Mail-Adresse -> Telefonnummer.";
            }}

            // 9. HWG-STAMM-02
            const nonCanonical = [];
            items.forEach(it => {{
                const props = it.properties || {{}};
                const rawLbl = String(props.label || "").trim();
                const lbl = rawLbl.replace(/<[^>]+>/g, "").trim();
                const name = String(props.name || "").toLowerCase();
                if ((name.includes("email") || name.includes("mail")) && lbl && !["E-Mail-Adresse", "E-Mail", "Hochschul-E-Mail"].includes(lbl)) {{
                    nonCanonical.push([lbl, "Erwartet: E-Mail-Adresse oder Hochschul-E-Mail"]);
                }}
                if (name.includes("nachname") || (name.includes("name") && !["vorname", "antrag", "bank", "kredit", "projekt", "programm", "foerder"].some(t => name.includes(t)))) {{
                    if (lbl.toLowerCase().includes("antragstellende") || lbl === "Name") {{
                        nonCanonical.push([lbl, "Erwartet: Nachname"]);
                    }}
                }}
            }});
            if (nonCanonical.length > 0) {{
                results.violations.push({{ rule: "HWG-STAMM-02", severity: "minor", message: `Nicht-standardisierte Stammdaten-Bezeichnungen gefunden: ${{nonCanonical.map(nc => `['${{nc[0]}}', '${{nc[1]}}']`).slice(0, 2).join(", ")}}` }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push("HWG-STAMM-02 (Kanonische Stammdaten-Labels)");
            }}

            // 10. HWG-UI-01
            if (devNotes.length > 0) {{
                results.violations.push({{ rule: "HWG-UI-01", severity: "critical", message: `Sichtbare Entwickler-Notizen / Skript-Reste im Frontend: ${{devNotes.map(dn => `['${{dn[0]}}', '${{dn[1]}}']`).join(", ")}}` }});
                results.score -= penalties.critical;
            }} else {{
                results.passed.push("HWG-UI-01 (Keine Entwickler-Notizen)");
            }}

            // 11. HWG-BTN-01
            const invalidButtons = [];
            buttonLabels.forEach(([bSource, b]) => {{
                const bClean = b.trim();
                const bLower = bClean.toLowerCase();
                if (["Kritischer Fall", "Status", "Genehmigung", "Fehler", "Rückmeldung", "Abgelehnt", "Angenommen"].includes(bClean)) {{
                    invalidButtons.push(`'${{bClean}}' (Reine Status-/Zustandsbezeichnung ohne Handlungsverb)`);
                }} else if (["senden", "submit", "ok", "abschicken"].includes(bLower)) {{
                    invalidButtons.push(`'${{bClean}}' (Generisches Minimal-Label ohne Zielobjekt)`);
                }}
            }});
            if (invalidButtons.length > 0) {{
                const dedup = Array.from(new Set(invalidButtons));
                results.violations.push({{ rule: "HWG-BTN-01", severity: "major", message: `Schaltflächen verletzen das Action-Verb-Muster: ${{dedup.join(", ")}}` }});
                results.score -= penalties.major;
            }} else if (buttonLabels.length > 0) {{
                results.passed.push("HWG-BTN-01 (Aktionsorientierte Schaltflächen: Action-Verb-Muster erfüllt)");
            }} else {{
                results.not_applicable["HWG-BTN-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Aktionsschaltflächen im Formular vorhanden.";
            }}

            // 12. HWG-BTN-02
            if (pageCount > 1) {{
                const invalidNav = navButtonLabels.filter(nb => !["weiter", "zurück", "zurueck"].includes(nb.trim().toLowerCase()));
                if (invalidNav.length > 0) {{
                    results.violations.push({{ rule: "HWG-BTN-02", severity: "minor", message: `Nicht-standardisierte Navigations-Schaltflächen in mehrseitigem Formular gefunden: [${{invalidNav.join(", ")}}]. Erwartet: 'Weiter' und 'Zurück'.` }});
                    results.score -= penalties.minor;
                }} else {{
                    results.passed.push("HWG-BTN-02 (Einheitliche Navigations-Schaltflächen 'Weiter'/'Zurück' vorhanden)");
                }}
            }} else {{
                results.not_applicable["HWG-BTN-02"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Einseitiges Formular ohne Seitenwechsel (keine Pagination erforderlich).";
            }}

            // 13. HWG-DSGVO-01
            if (hasPersonalData && !hasDsgvoNotice) {{
                results.violations.push({{ rule: "HWG-DSGVO-01", severity: "critical", message: "Personenbezogene Daten werden erhoben, aber es fehlt ein Datenschutz-Hinweis / DSGVO-Link." }});
                results.score -= penalties.critical;
            }} else {{
                results.passed.push("HWG-DSGVO-01 (Datenschutz-Hinweis vorhanden oder keine Personendaten)");
            }}

            // 14. HWG-UPLOAD-01
            if (!hasUploadElements) {{
                results.not_applicable["HWG-UPLOAD-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine Dateiupload-Elemente im Formular vorhanden.";
            }} else if (uploadElements.length > 0) {{
                results.violations.push({{ rule: "HWG-UPLOAD-01", severity: "major", message: `${{uploadElements.length}} Dateiupload-Element(e) ohne transparente Angabe von Dateiformat und/oder Maximalgröße.` }});
                results.score -= penalties.major;
            }} else {{
                results.passed.push("HWG-UPLOAD-01 (Dateiuploads mit Formaten und Maximalgröße spezifiziert)");
            }}

            // 15. HWG-VAL-01
            if (structuredFieldsUnvalidated.length > 0) {{
                results.violations.push({{ rule: "HWG-VAL-01", severity: "major", message: `Strukturierte Felder ohne Validierungsregel gefunden: [${{structuredFieldsUnvalidated.slice(0, 3).join(", ")}}]` }});
                results.score -= penalties.major;
            }} else {{
                results.passed.push("HWG-VAL-01 (Strukturierte Felder validiert)");
            }}

            // 16. HWG-UX-01
            if (!hasCompactFields) {{
                results.not_applicable["HWG-UX-01"] = "Kriterium auf diesen Formularkontext nicht anwendbar: Keine typischen Kompaktfelder (wie PLZ oder Hausnummer) vorhanden.";
            }} else if (compactFieldsUnconstrained.length > 0) {{
                results.violations.push({{ rule: "HWG-UX-01", severity: "minor", message: `Kompakte Felder (PLZ/Hausnummer) ohne Breitenbegrenzung über volle Breite gestreckt: [${{compactFieldsUnconstrained.slice(0, 2).join(", ")}}]` }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push("HWG-UX-01 (Affordanzgerechte Feldbreiten für Kompaktfelder eingehalten)");
            }}

            // 17. HWG-UX-02
            if ((pageCount >= 3 || inputFieldCount >= 25) && !hasSaveButton) {{
                results.recommendations.push({{
                    rule: "HWG-UX-02",
                    severity: "recommendation",
                    message: `Formularumfang (${{pageCount}} Seiten, ${{inputFieldCount}} Eingabefelder) überschreitet den Komplexitätsschwellenwert. Empfehlung (0 Pkt. Abzug): Einen 'Zwischenspeichern'-Button ergänzen, der das Formular speichert und einen Fortsetzungs-Link per E-Mail an die Nutzenden versendet.`
                }});
            }}

            // 18. HWG-LANG-01
            if (jargonWithoutHelp.length > 0) {{
                const dedupJargon = Array.from(new Set(jargonWithoutHelp.map(j => `'${{j[0]}}' in ${{j[1]}}`)));
                results.violations.push({{ rule: "HWG-LANG-01", severity: "major", message: `Hochschul- und Verwaltungs-Jargon ohne erläuternden Hilfetext gefunden: ${{dedupJargon.slice(0, 3).join(", ")}}` }});
                results.score -= penalties.major;
            }} else {{
                results.passed.push("HWG-LANG-01 (Verständlicher Wortschatz: Kein unerklärter Jargon)");
            }}

            // 19. HWG-LANG-02
            if (longSentences.length > 0) {{
                results.violations.push({{ rule: "HWG-LANG-02", severity: "minor", message: `Überlange Schachtelsätze (> 25 Wörter) gefunden: [${{longSentences.map(ls => `['${{ls[0]}}', ${{ls[1]}}, '${{ls[2]}}']`).slice(0, 2).join(", ")}}].` }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push("HWG-LANG-02 (Prägnante Formulierungen: Alle Sätze unter 25 Wörtern)");
            }}

            // 20. HWG-FEEDBACK-01
            if (!hasWorkflowFeedback) {{
                results.violations.push({{ rule: "HWG-FEEDBACK-01", severity: "minor", message: "Keine Eingangsbestätigungs-E-Mail mit Prozess-/Bearbeitungsinformationen in den Workflow-E-Mail-Knoten (FC_EMAIL) gefunden." }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push(`HWG-FEEDBACK-01 (Workflow-E-Mail-Transparenz in ${{workflowEmails.length}} FC_EMAIL-Knoten bestätigt)`);
            }}

            // 21. HWG-WF-01
            if (!workflowStates || workflowStates.length === 0) {{
                results.violations.push({{ rule: "HWG-WF-01", severity: "minor", message: "Keine expliziten Status-Knoten (FC_CHANGE_STATE) im Workflow hinterlegt. Kanonischer Lebenszyklus erforderlich." }});
                results.score -= penalties.minor;
            }} else {{
                const canonicalStates = new Set(["eingegangen", "in prüfung", "in bearbeitung", "nachforderung ausstehend", "genehmigt", "abgelehnt", "archiviert", "abgeschlossen"]);
                const nonCanonical = workflowStates.filter(s => !canonicalStates.has(s.toLowerCase()));
                if (nonCanonical.length > 0) {{
                    results.violations.push({{ rule: "HWG-WF-01", severity: "minor", message: `Nicht-standardisierte Ad-hoc-Statusnamen im Workflow gefunden: [${{nonCanonical.join(", ")}}]. Erwartet: kanonische Zustände ('Eingegangen', 'In Prüfung', 'Genehmigt', 'Abgelehnt').` }});
                    results.score -= penalties.minor;
                }} else {{
                    results.passed.push(`HWG-WF-01 (Kanonischer Workflow-Lebenszyklus eingehalten: ${{workflowStates.join(", ")}})`);
                }}
            }}

            // 22. HWG-WF-02
            let hasProjectAlias = false;
            (workflowEmails || []).forEach(em => {{
                const s = String(em.subject || "").toLowerCase();
                const b = String(em.body || "").toLowerCase();
                if (s.includes("%$project_alias%") || b.includes("%$project_alias%") || s.includes("vorgangsnummer") || s.includes("vorgang")) {{
                    hasProjectAlias = true;
                }}
            }});
            if (!hasProjectAlias) {{
                results.violations.push({{ rule: "HWG-WF-02", severity: "minor", message: "Fehlende Vorgangsnummer ([%$PROJECT_ALIAS%]) in Workflow-E-Mail-Betreffzeilen." }});
                results.score -= penalties.minor;
            }} else {{
                results.passed.push("HWG-WF-02 (Vorgangsnummern-Referenz in Workflow-E-Mail vorhanden)");
            }}

            results.score = Math.max(0, results.score);
            return results;
        }}

        async function handleFileUpload(event) {{
            const file = event.target.files[0];
            if (!file) return;

            // Try backend API first
            try {{
                const response = await fetch('/api/evaluate', {{
                    method: 'POST',
                    headers: {{
                        'X-File-Name': file.name
                    }},
                    body: file
                }});
                if (response.ok) {{
                    const result = await response.json();
                    currentEval = result;
                    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                    renderEvaluation();
                    return;
                }}
            }} catch (netErr) {{
                console.log("Backend API not reachable, falling back to local client parsing:", netErr);
            }}

            // Client-side fallback (runs in browser on Vercel or local file://)
            try {{
                if (file.name.endsWith('.xfp')) {{
                    if (typeof JSZip !== 'undefined') {{
                        const zip = await JSZip.loadAsync(file);
                        let fcpData = null;
                        const emails = [];
                        const states = [];
                        for (const [relPath, zipEntry] of Object.entries(zip.files)) {{
                            if (relPath.endsWith('.fcp')) {{
                                const text = await zipEntry.async('string');
                                fcpData = JSON.parse(text);
                            }} else if (relPath.endsWith('.fcexport') && relPath.includes('/projects/') && !relPath.includes('idcheck') && !relPath.includes('versions')) {{
                                const text = await zipEntry.async('string');
                                try {{
                                    const proj = JSON.parse(text);
                                    extractWorkflowClient(proj, emails, states);
                                }} catch (e) {{}}
                            }}
                        }}
                        if (fcpData) {{
                            currentEval = evaluateFormDataClient(fcpData, file.name, emails, states);
                            document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                            renderEvaluation();
                            return;
                        }}
                    }} else {{
                        alert("JSZip-Bibliothek wird geladen... Bitte versuchen Sie es in wenigen Sekunden erneut.");
                        return;
                    }}
                }} else if (file.name.endsWith('.json')) {{
                    const text = await file.text();
                    const data = JSON.parse(text);
                    currentEval = evaluateFormDataClient(data, file.name, data.workflow_emails || [], data.workflow_states || []);
                    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                    renderEvaluation();
                    return;
                }}
            }} catch (err) {{
                console.error("Client parsing error:", err);
                alert("Konnte Datei im Browser nicht verarbeiten: " + err.message);
            }}
        }}

        // Initialize on load
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
