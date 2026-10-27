# Bereitstellungsanleitung: HWG Formcycle Compliance Dashboard

Diese Anleitung richtet sich an das Hochschul-Rechenzentrum / die IT-Administration der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen zur schnellen und sicheren Bereitstellung des Formcycle Compliance Dashboards im Hochschul-Intranet.

---

## Übersicht der Bereitstellungsoptionen

Das Dashboard unterstützt **drei schlanke Bereitstellungswege**:

1. **Option 1 (Docker / Container – Empfohlen):** Vollständiger Microservice inklusive hybrider Python-Auswertungs-API (Stufe 1 AST + optionale Stufe 2 LLM-API).
2. **Option 2 (Nginx / Apache – Rein statisch):** Bereitstellung ohne Server-Laufzeit (Client-seitiger AST-Audit via JSZip; semantische KI-Regeln transparent als ungeprüft markiert).
3. **Option 3 (Reverse Proxy vor Container):** Standard-Enterprise-Setup mit SSL/TLS im Hochschulnetz.

---

## Option 1: Docker / Docker Compose (Empfohlen)

### Eigenschaften:
* **Image-Basis:** `python:3.11-alpine` (Größe: ca. 55 MB).
* **Abhängigkeiten:** **Keine externen Pip-Pakete** erforderlich (100 % Python-Standardbibliothek).
* **Sicherheit & Zero-Disk-Footprint:** Läuft als nicht-privilegierter Benutzer (`appuser`), `no-new-privileges: true` und `read_only: true`, da hochgeladene Archive ausschließlich im Arbeitsspeicher (`io.BytesIO`) verarbeitet werden.

### Startbefehl (mit optionaler GWDG Academic Cloud / OpenAI-kompatibler KI-API):
Im Projektverzeichnis ausführen:
```bash
export LLM_API_BASE="https://chat-ai.academiccloud.de/v1"
export LLM_MODEL="qwen3-30b-a3b-instruct-2507"
export LLM_API_KEY="<IHR-GWDG-API-KEY>"
docker compose -f deploy/docker-compose.yml up -d
```
*(Wird kein `LLM_API_KEY` gesetzt oder ist die API nicht erreichbar, greift automatisch der transparente Fail-Safe: Die 15 deterministischen AST-Regeln werden regulär geprüft, während die 7 semantischen/hybriden Regeln eindeutig als „Nicht zutreffend · Keine KI-Prüfung“ gekennzeichnet werden.)*

Das Dashboard und die Prüf-API sind erreichbar unter:
`http://<SERVER-IP-ODER-HOSTNAME>:8080/`

---

## Option 2: Reines Nginx oder Apache (Statische Bereitstellung)

Da das Dashboard die deterministische Stufe-1-Prüflogik und die Archiv-Dekompression (`JSZip`) direkt im Browser mitbringt, genügt für den reinen Offline-Strukturaudit eine statische Bereitstellung:

1. Kopieren Sie `web/compliance_dashboard.html` sowie den Ordner `web/vendor/` (enthält `jszip.min.js`) in das Web-Verzeichnis (z. B. `/var/www/compliance_dashboard/`).
2. Konfiguration anlegen (Vorlage in `deploy/nginx.conf`).
3. Webserver neu laden (`systemctl reload nginx`).

---

## Option 3: Nginx als Reverse Proxy mit HTTPS

```nginx
server {
    listen 443 ssl http2;
    server_name formulare-check.intern.hwg-lu.de;

    ssl_certificate     /etc/ssl/certs/hwg-lu-wildcard.crt;
    ssl_certificate_key /etc/ssl/private/hwg-lu-wildcard.key;

    client_max_body_size 50M;

    location / {
        proxy_pass http://127.0.0.1:8080;
        proxy_set_header Host $host;
        proxy_set_header X-Real-IP $remote_addr;
        proxy_set_header X-Forwarded-For $proxy_add_x_forwarded_for;
        proxy_set_header X-Forwarded-Proto $scheme;
    }
}
```

---

## IT-Sicherheits- & Architektur-Fakten für die Administration

| Kriterium | Status / Nachweis |
| :--- | :--- |
| **Datenbank erforderlich?** | **Nein.** Das System arbeitet vollständig zustandslos (*stateless*). |
| **Dateispeicherung?** | **Nein (Zero-Disk-Footprint).** Hochgeladene `.xfp`-Formulare werden ausschließlich im Arbeitsspeicher (`io.BytesIO`) entpackt und unmittelbar nach Antwortversand verworfen; keine Temp-Dateien auf der Festplatte. |
| **Internet-Verbindung?** | **Optional.** Stufe 1 läuft zu 100 % offline; Stufe 2 nutzt einen internen oder akademischen Endpunkt (`Academic Cloud` GWDG). |
| **Ressourcenbedarf:** | Minimal: 1 vCPU, 512 MB RAM. |

---

## Souveräner Betrieb mit Open-Weight-LLMs (Stufe 2)

1. **Deterministische Prüfung (Stufe 1):** Die AST-Strukturprüfung (15 von 22 Governance-Regeln) läuft lokal im Arbeitsspeicher in unter 20 ms.
2. **Semantische Prüfung (Stufe 2):**
   * Empfohlene Open-Weight-Modelle ab der 27B/MoE-Klasse (z. B. *Qwen 3 30B A3B*, *Qwen 3.8 27B*, *GLM 5.3 Flash* oder *DeepSeek V4 Flash*) werden über die *Academic Cloud* (GWDG) oder einen internen Inferenz-Server (**vLLM** / **Ollama**) via `/v1/chat/completions` angesprochen.
   * Zu keinem Zeitpunkt müssen Formulardaten an außereuropäische Cloud-Anbieter übermittelt werden (Art. 44 ff. DSGVO).
