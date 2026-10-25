# Bereitstellungsanleitung: HWG Formcycle Compliance Dashboard

Diese Anleitung richtet sich an das Hochschul-Rechenzentrum / die IT-Administration der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen zur schnellen und sicheren Bereitstellung des Formcycle Compliance Dashboards im Hochschul-Intranet.

---

## Übersicht der Bereitstellungsoptionen

Das Dashboard wurde so konzipiert, dass die IT zwischen **drei extrem schlanken Wegen** wählen kann:

1. **Option 1 (Docker / Container – Empfohlen):** Vollständiger Microservice inklusive Python-Auswertungs-API.
2. **Option 2 (Nginx / Apache – Rein statisch):** Einfachste Bereitstellung ohne Server-Laufzeit (Standalone).
3. **Option 3 (Reverse Proxy vor Container):** Standard-Enterprise-Setup mit SSL/TLS.

---

## Option 1: Docker / Docker Compose (Empfohlen)

### Eigenschaften:
* **Image-Basis:** `python:3.11-alpine` (Größe: ca. 55 MB).
* **Abhängigkeiten:** **Keine externen Pip-Pakete** erforderlich (verwendet ausschließlich die Python-Standardbibliothek).
* **Sicherheit:** Läuft als nicht-privilegierter Benutzer (`appuser`), `no-new-privileges: true`.

### Startbefehl:
Im Projektverzeichnis ausführen:
```bash
docker compose -f deploy/docker-compose.yml up -d
```

Das Dashboard und die Prüf-API sind nun sofort erreichbar unter:
`http://<SERVER-IP-ODER-HOSTNAME>:8080/`

---

## Option 2: Reines Nginx oder Apache (Statische Bereitstellung)

Da das Dashboard clientseitige Prüflogik und die Archiv-Dekompression (JSZip) direkt im Browser mitbringt, genügt für den Basisbetrieb eine einzige HTML-Datei:

### Schritte für Nginx / Apache:
1. Kopieren Sie die Datei `web/compliance_dashboard.html` sowie den Ordner `web/vendor/` (enthält `jszip.min.js`) in das Web-Verzeichnis des Webservers (z. B. `/var/www/compliance_dashboard/`).
   *Hinweis für Air-Gapped-Umgebungen:* Das Mitkopieren von `web/vendor/jszip.min.js` stellt sicher, dass das Client-seitige ZIP-Parsing ohne Internetverbindung und ohne Rückgriff auf externe CDNs vollständig lokal funktioniert.
2. Konfiguration anlegen (eine Vorlage befindet sich in `deploy/nginx.conf`).
3. Webserver neu laden (`systemctl reload nginx`).

---

## Option 3: Nginx als Reverse Proxy mit HTTPS

Zur Absicherung im Hochschulnetz hinter einem zentralen Nginx mit Hochschulzertifikat:

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
| **Datenbank erforderlich?** | **Nein.** Das System arbeitet zustandslos (*stateless*). Es wird keine SQL/NoSQL-Datenbank benötigt. |
| **Dateispeicherung?** | **Nein.** Hochgeladene Formulare werden nur im Arbeitsspeicher/flüchtigen Temp-Dateien analysiert und sofort verworfen. Keine Persistierung von Antragsdaten. |
| **Internet-Verbindung?** | **Nein.** Das System kann vollständig isoliert (*Air-Gapped*) im Intranet ohne ausgehende Internet-Verbindungen betrieben werden. |
| **Ressourcenbedarf:** | Minimal: 1 vCPU, 512 MB RAM genügen für Hunderte gleichzeitige Prüfungen. |
| **Wartungsaufwand:** | Nahezu null, da keine externen Python-Bibliotheken aktualisiert werden müssen. |

---

## Air-Gapped-Betrieb mit KI / LLM-Anbindung

Ein zentraler Vorteil der Architektur ist die vollständige Unabhängigkeit von externen Cloud-Diensten:
1. **Deterministische Prüfung (Stufe 1):** Die AST-Strukturprüfung (15 von 22 Regeln) läuft vollständig lokal und offline in unter 20 ms.
2. **Semantische Prüfung (Stufe 2 mit Open-Source-LLM):** 
   * Auch die semantische Sprachmodell-Inferenz kann **zu 100 % Air-Gapped** im Hochschulnetz betrieben werden.
   * Hierzu wird ein quelloffenes Open-Weight-Modell (z. B. *Qwen 3 30B* oder *Llama 3.1 8B*) auf einem internen Server des Hochschul-Rechenzentrums oder der *Academic Cloud* (GWDG) über Inferenz-Server wie **vLLM** oder **Ollama** gehostet.
   * Das Dashboard bzw. die Python-Middleware sendet den kompakten JSON-Payload ausschließlich an die interne Netzwerkadresse (z. B. `http://llm-service.intern.hwg-lu.de/v1/chat/completions`).
   * **Ergebnis:** Zu keinem Zeitpunkt verlassen Formulardaten das interne Hochschulnetzwerk. Die Anforderungen nach Art. 9 und Art. 44 ff. DSGVO bezüglich Datensouveränität werden vollständig erfüllt.
