import http.server
import json
import os
import socketserver
import sys
import urllib.parse

# Add scripts directory to path so we can import test_rule_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from test_rule_engine import evaluate_form, evaluate_form_bytes, load_rules

PORT = int(os.environ.get("PORT", 8080))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))
REPO_ROOT = os.path.abspath(os.path.join(DIRECTORY, ".."))

PRESET_PATHS = {
    "synth_comp": "data/test_forms/synthetic_compliant_form.json",
    "synth_noncomp": "data/test_forms/synthetic_noncompliant_form.json",
    "auslagen": "data/raw_forms/prod/Auslagenerstattung _20260929.xfp",
    "sprints": "data/raw_forms/test/unfertige und vielleicht fertige formulare/AFörderung Antrag-Sprints für Drittmittelanträge.xfp",
    "master": "data/raw_forms/test/adminformulare/Master-Formular.xfp",
}


class ComplianceHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def _extract_llm_config(self):
        cfg = {}
        api_key = self.headers.get("X-LLM-Api-Key", "").strip()
        api_base = self.headers.get("X-LLM-Api-Base", "").strip()
        model = self.headers.get("X-LLM-Model", "").strip()
        if api_key:
            cfg["api_key"] = api_key
        if api_base:
            cfg["api_base"] = api_base
        if model:
            cfg["model"] = model
        return cfg or None

    def _send_json(self, status_code: int, payload: dict):
        body = json.dumps(payload, ensure_ascii=False).encode("utf-8")
        self.send_response(status_code)
        self.send_header("Content-Type", "application/json; charset=utf-8")
        self.send_header("Content-Length", str(len(body)))
        self.end_headers()
        self.wfile.write(body)

    def do_GET(self):
        if self.path in ["/", "/index.html", "/dashboard"]:
            self.path = "/compliance_dashboard.html"
            return super().do_GET()
        if self.path == "/api/rules":
            rules_path = os.path.join(REPO_ROOT, "data", "rules", "rules_registry.json")
            with open(rules_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self._send_json(200, data)
            return
        return super().do_GET()

    def do_POST(self):
        rules_path = os.path.join(REPO_ROOT, "data", "rules", "rules_registry.json")
        if self.path == "/api/evaluate":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                post_body = self.rfile.read(content_length)
                raw_header_name = self.headers.get("X-File-Name", "uploaded_form.json")
                filename = urllib.parse.unquote(raw_header_name)
                llm_cfg = self._extract_llm_config()
                reg = load_rules(rules_path)
                # Reine In-Memory-Verarbeitung (Zero-Disk-Footprint via io.BytesIO)
                result = evaluate_form_bytes(post_body, filename, reg, llm_config=llm_cfg)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        if self.path == "/api/evaluate-preset":
            try:
                content_length = int(self.headers.get("Content-Length", 0))
                body_raw = self.rfile.read(content_length).decode("utf-8", errors="replace")
                req_obj = json.loads(body_raw or "{}")
                preset_key = req_obj.get("preset", "")
                if preset_key not in PRESET_PATHS:
                    self._send_json(400, {"error": f"Unbekanntes Preset: {preset_key}"})
                    return
                full_path = os.path.join(REPO_ROOT, PRESET_PATHS[preset_key])
                llm_cfg = self._extract_llm_config()
                reg = load_rules(rules_path)
                result = evaluate_form(full_path, reg, llm_config=llm_cfg)
                self._send_json(200, result)
            except Exception as e:
                self._send_json(500, {"error": str(e)})
            return

        self._send_json(404, {"error": "Unbekannter Endpunkt"})


def run_server():
    with socketserver.TCPServer(("", PORT), ComplianceHandler) as httpd:
        print(f"HWG Compliance Dashboard Server läuft unter: http://localhost:{PORT} (Zero-Disk-Footprint In-Memory)")
        print("Beenden mit Strg+C.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer gestoppt.")


if __name__ == "__main__":
    run_server()
