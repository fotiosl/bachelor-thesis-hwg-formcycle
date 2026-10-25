import http.server
import socketserver
import os
import json
import sys
import tempfile

# Add parent directory to path so we can import test_rule_engine
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..", "scripts")))
from test_rule_engine import evaluate_form, load_rules

PORT = int(os.environ.get("PORT", 8080))
DIRECTORY = os.path.dirname(os.path.abspath(__file__))

class ComplianceHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def do_GET(self):
        if self.path in ["/", "/index.html", "/dashboard"]:
            self.path = "/compliance_dashboard.html"
            return super().do_GET()
        elif self.path == "/api/rules":
            rules_path = os.path.abspath(os.path.join(DIRECTORY, "..", "data", "rules", "rules_registry.json"))
            with open(rules_path, "r", encoding="utf-8") as f:
                data = json.load(f)
            self.send_response(200)
            self.send_header("Content-Type", "application/json; charset=utf-8")
            self.end_headers()
            self.wfile.write(json.dumps(data, ensure_ascii=False).encode("utf-8"))
            return
        return super().do_GET()

    def do_POST(self):
        if self.path == "/api/evaluate":
            content_length = int(self.headers.get("Content-Length", 0))
            post_body = self.rfile.read(content_length)
            
            # Save uploaded content to temp file
            filename = self.headers.get("X-File-Name", "uploaded_form.json")
            suffix = ".xfp" if filename.endswith(".xfp") else ".json"
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=suffix) as tmp:
                tmp.write(post_body)
                tmp_path = tmp.name
                
            try:
                registry_path = os.path.abspath(os.path.join(DIRECTORY, "..", "data", "rules", "rules_registry.json"))
                reg = load_rules(registry_path)
                result = evaluate_form(tmp_path, reg)
                result["form"] = filename
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps(result, ensure_ascii=False).encode("utf-8"))
            except Exception as e:
                self.send_response(500)
                self.send_header("Content-Type", "application/json; charset=utf-8")
                self.end_headers()
                self.wfile.write(json.dumps({"error": str(e)}).encode("utf-8"))
            finally:
                if os.path.exists(tmp_path):
                    os.remove(tmp_path)
            return

def run_server():
    with socketserver.TCPServer(("", PORT), ComplianceHandler) as httpd:
        print(f"HWG Compliance Dashboard Server läuft unter: http://localhost:{PORT}")
        print("Beenden mit Strg+C.")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nServer gestoppt.")

if __name__ == "__main__":
    run_server()
