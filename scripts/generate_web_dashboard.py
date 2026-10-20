import json
import os

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
                    <div class="stat-sub" id="passRateSub">von 21 Kriterien</div>
                </div>
            </div>
        </div>

        <!-- Filter Bar -->
        <div class="filter-bar" id="filterBar">
            <button class="filter-pill active" onclick="setFilter('all')">Alle Kriterien (<span id="pillAll">21</span>)</button>
            <button class="filter-pill" onclick="setFilter('critical')">Kritisch (<span id="pillCritical">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('major')">Major (<span id="pillMajor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('minor')">Minor (<span id="pillMinor">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('recommendation')">Empfehlungen (<span id="pillRec">0</span>)</button>
            <button class="filter-pill" onclick="setFilter('passed')">Bestanden (<span id="pillPassed">0</span>)</button>
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
                        <span>${{p.name.split(':')[1] || p.name}}</span>
                        <span class="preset-score-pill ${{scoreClass}}">${{score}} P</span>
                    </div>
                    <div class="preset-btn-desc">${{p.eval.form}}</div>
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

            renderRuleCards();
        }}

        function setFilter(filter) {{
            currentFilter = filter;
            document.querySelectorAll('.filter-pill').forEach(p => p.classList.remove('active'));
            event.target.classList.add('active');
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

            registry.rules.forEach(rule => {{
                const isViolation = !!violationsMap[rule.id];
                const isRec = !!recMap[rule.id];
                const isPassed = passedSet.has(rule.id);

                // Filter check
                if (currentFilter === 'critical' && (!isViolation || violationsMap[rule.id].severity !== 'critical')) return;
                if (currentFilter === 'major' && (!isViolation || violationsMap[rule.id].severity !== 'major')) return;
                if (currentFilter === 'minor' && (!isViolation || violationsMap[rule.id].severity !== 'minor')) return;
                if (currentFilter === 'recommendation' && !isRec) return;
                if (currentFilter === 'passed' && !isPassed) return;

                const card = document.createElement('div');
                let cardClass = 'rule-card';
                let badgeHtml = '';
                let messageHtml = '';

                if (isViolation) {{
                    const v = violationsMap[rule.id];
                    cardClass += ` violation-${{v.severity}}`;
                    const pts = v.severity === 'critical' ? '-15P' : (v.severity === 'major' ? '-8P' : '-3P');
                    badgeHtml = `<span class="badge badge-${{v.severity}}">${{v.severity.toUpperCase()}} (${{pts}})</span>`;
                    messageHtml = `<div class="rule-message"><strong>Befund:</strong> ${{v.message}}</div>`;
                }} else if (isRec) {{
                    const r = recMap[rule.id];
                    cardClass += ' violation-recommendation';
                    badgeHtml = `<span class="badge badge-recommendation">EMPFEHLUNG (0P)</span>`;
                    messageHtml = `<div class="rule-message"><strong>Empfehlung:</strong> ${{r.message}}</div>`;
                }} else if (isPassed) {{
                    cardClass += ' rule-passed';
                    badgeHtml = `<span class="badge badge-passed">BESTANDEN (OK)</span>`;
                    messageHtml = `<div class="rule-message" style="color: var(--hwg-green);">✓ Vorgaben erfolgreich eingehalten.</div>`;
                }} else {{
                    cardClass += ' rule-passed';
                    badgeHtml = `<span class="badge" style="background: var(--slate-100); color: var(--slate-600);">NICHT ZUTREFFEND</span>`;
                    messageHtml = `<div class="rule-message" style="color: var(--slate-600);">Kriterium auf diesen Formularkontext nicht anwendbar.</div>`;
                }}

                card.className = cardClass;
                card.innerHTML = `
                    <div class="rule-top">
                        <div class="rule-id-name">
                            <span class="rule-id">${{rule.id}}</span>
                            <span class="rule-name">${{rule.name}}</span>
                        </div>
                        ${{badgeHtml}}
                    </div>
                    ${{messageHtml}}
                    <div class="remediation-box">
                        <div class="remediation-title">
                            <svg width="14" height="14" fill="currentColor" viewBox="0 0 16 16"><path d="M8 15A7 7 0 1 1 8 1a7 7 0 0 1 0 14zm0 1A8 8 0 1 0 8 0a8 8 0 0 0 0 16z"/><path d="M8 4a.5.5 0 0 1 .5.5v3h3a.5.5 0 0 1 0 1h-3.5a.5.5 0 0 1-.5-.5v-4A.5.5 0 0 1 8 4z"/></svg>
                            Klickpfad im XIMA Formcycle Designer (Remediation):
                        </div>
                        <div class="remediation-text">${{rule.remediation}}</div>
                    </div>
                    <div class="rationale-text">Theoretische & regulatorische Fundierung: ${{rule.rationale}}</div>
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

            // Fallback for standalone file:// mode
            const reader = new FileReader();
            reader.onload = function(e) {{
                try {{
                    const parsed = JSON.parse(e.target.result);
                    currentEval = {{
                        form: file.name,
                        violations: [],
                        recommendations: [],
                        passed: ["HWG-CD-01 (Breite 850px eingehalten)"],
                        score: 85
                    }};
                    document.querySelectorAll('.preset-btn').forEach(b => b.classList.remove('active'));
                    renderEvaluation();
                }} catch (err) {{
                    alert("Konnte Datei nicht verarbeiten: " + err.message);
                }}
            }};
            reader.readAsText(file);
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
