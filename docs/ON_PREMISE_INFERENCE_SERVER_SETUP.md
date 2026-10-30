# On-Premise GPU Inferenz-Server Setup (Debian 13 + NVIDIA RTX 4090)

**Dokumentation der praktischen Produktiv- und Benchmark-Bereitstellung für die Bachelor-Thesis:**  
*Formcycle Usability- und Governance-Compliance-Prüfung via Self-Hosted Open-Weight LLMs*  
**Host:** `srv-foti-01` (IP: `143.93.216.223` / Hochschulnetz HWG Ludwigshafen)

---

## 1. Relevanz für die Bachelor-Thesis & Datenschutz (DSGVO)

In Kapitel 6 der Arbeit wird die zweistufige hybride Prüfpipeline (Stufe 1 AST + Stufe 2 semantische LLM-Prüfung) empirisch evaluiert. Neben dem Betrieb über die *Academic Cloud* (GWDG) wurde mit dieser Server-Installation die **vollständige On-Premise-Inferenzfähigkeit im Intranet der Hochschule für Wirtschaft und Gesellschaft Ludwigshafen** nachgewiesen:

1. **100 % DSGVO-Konformität (Art. 44 ff. DSGVO):** Zu keinem Zeitpunkt verlassen Formulardaten, vertrauliche Antragsstrukturen oder personenbezogene Stammdaten das Hochschulnetz oder den Arbeitsspeicher der Maschine.
2. **Zero-Cloud-Dependency:** Die Inferenz wird vollständig lokal über die dedizierte GPU-Hardware realisiert.
3. **Modell-Agnostik & Validierte Treue:** Mit dem Open-Weight-Modell `Qwen 3.8 27B` werden alle semantischen Regeln mit **0 False Positives und 100 % validem JSON** auditiert.

---

## 2. Hardware- und Systemumgebung

| Komponente | Spezifikation | Bewertung für LLM-Hosting |
| :--- | :--- | :--- |
| **Betriebssystem** | Debian GNU/Linux 13 (*Trixie*), Kernel 6.12+ | Minimales, stabiles Linux-Fundament |
| **Grafikkarte (GPU)** | NVIDIA GeForce RTX 4090 (AD102, 24 GB VRAM) | Führt Modelle bis 30B (4-Bit) vollständig im VRAM aus |
| **Arbeitsspeicher** | 128 GB DDR5 RAM | Erlaubt Hybrid-Offloading selbst für 70B-Modelle |
| **Prozessor (CPU)** | Intel Core i9-13900K (32 logische Kerne) | Hoher Durchsatz bei Preprocessing & AST-Analyse |
| **Speicher** | 1,7 TB NVMe SSD | Schnelles Caching großer Model Weights |

---

## 3. Durchgeführte Installationsschritte (Chronologisches Protokoll)

### 3.1 Freischaltung der Debian-Paketquellen (deb822)
Debian 13 aktiviert standardmäßig nur `main`. Für den proprietären NVIDIA-Treiber wurden `contrib` und `non-free` freigeschaltet:
```bash
sudo sed -i 's/Components: main non-free-firmware/Components: main contrib non-free non-free-firmware/g' /etc/apt/sources.list /etc/apt/sources.list.d/*.sources 2>/dev/null
sudo apt update
```

### 3.2 NVIDIA-Treiber & Kernel-Module
Installation des offiziellen Treibers und Header-Dateien:
```bash
sudo apt install -y linux-headers-$(uname -r) build-essential nvidia-driver firmware-misc-nonfree
sudo reboot
# Verifikation nach Neustart:
nvidia-smi
```

### 3.3 NVIDIA Container Toolkit für Docker
Ermöglicht Docker-Containern den direkten Zugriff auf die RTX 4090 via `--gpus all`:
```bash
sudo apt install -y gnupg curl

curl -fsSL https://nvidia.github.io/libnvidia-container/gpgkey | sudo gpg --dearmor --yes -o /usr/share/keyrings/nvidia-container-toolkit-keyring.gpg

curl -s -L https://nvidia.github.io/libnvidia-container/stable/deb/nvidia-container-toolkit.list | \
  sed 's#deb https://#deb [signed-by=/usr/share/keyrings/nvidia-container-toolkit-keyring.gpg] https://#g' | \
  sudo tee /etc/apt/sources.list.d/nvidia-container-toolkit.list

sudo apt update
sudo apt install -y nvidia-container-toolkit
sudo nvidia-ctk runtime configure --runtime=docker
sudo systemctl restart docker

# GPU-Passthrough-Test:
docker run --rm --gpus all ubuntu nvidia-smi
```

### 3.4 Ollama GPU-Container bereitstellen
Dauerhafter Dienst mit automatischem Neustartverhalten und Volume-Persistenz:
```bash
docker run -d --name ollama --restart always --gpus all -v ollama:/root/.ollama -p 11434:11434 ollama/ollama
```

### 3.5 Herunterladen und Validierung des Benchmark-Modells
Auswahl des fehlerfreien Modells aus der Benchmark-Evaluation der Thesis:
```bash
docker exec -it ollama ollama pull qwen3.8:27b

# VRAM-Allokation prüfen (muss 100% GPU auf RTX 4090 ausweisen):
docker exec ollama ollama ps
```

### 3.6 HWG Formcycle Compliance Dashboard Deployment
Bereitstellung des Dashboards als Docker-Container mit Host-Networking zur direkten Kommunikation mit Ollama:
```bash
git clone https://github.com/fotiosl/bachelor-thesis-hwg-formcycle.git
cd bachelor-thesis-hwg-formcycle

docker run -d \
  --name hwg-formcycle-checker \
  --restart unless-stopped \
  --network host \
  -e PORT=8080 \
  -e LLM_API_BASE="http://localhost:11434/v1" \
  -e LLM_MODEL="qwen3.8:27b" \
  -e LLM_API_KEY="ollama" \
  -e LLM_ALLOW_NO_KEY="1" \
  $(docker build -q -f deploy/Dockerfile .)
```

### 3.7 Netzwerkzugriff & Firewall (UFW / SSH-Tunneling)
Da Port 8080 durch Hochschul-Firewalls geschützt ist, erfolgt der Zugriff entweder über Freigabe oder SSH-Port-Forwarding:
```bash
# Auf dem Server (falls UFW aktiv):
sudo ufw allow 8080/tcp

# Vom Client-Laptop (gesicherter SSH-Tunnel):
ssh -L 8080:localhost:8080 foti@143.93.216.223
```
Dashboard-Aufruf im Webbrowser: `http://localhost:8080` (mit API-Base `http://localhost:11434/v1`).

---

## 4. Betriebs- und Lifecycle-Handbuch

### 4.1 Regulärer Zustand (Feierabend / Standby)
Die Container `ollama` und `hwg-formcycle-checker` sind so konfiguriert, dass sie dauerhaft als Hintergrunddienste laufen (`--restart always` / `unless-stopped`). Im Leerlauf verbrauchen sie nahezu **0 % CPU** und halten das Modell im VRAM bereit.
* Es muss **nichts manuell beendet** werden.
* Auf dem Arbeits-Laptop einfach das Terminalfenster (bzw. den SSH-Tunnel) schließen.

### 4.2 Manuelles Beenden der Dienste (z. B. für Wartung)
Falls die Container gestoppt werden sollen:
```bash
# Stoppt das Dashboard und den Ollama-Inferenz-Server:
docker stop hwg-formcycle-checker ollama
```

Falls der Server komplett heruntergefahren werden muss:
```bash
sudo shutdown -h now
```

### 4.3 Wiederaufnahme / Start beim nächsten Mal
1. Mit dem Hochschulnetzwerk verbinden (vor Ort oder via VPN).
2. SSH-Tunnel auf dem Laptop öffnen:
   ```bash
   ssh -L 8080:localhost:8080 foti@143.93.216.223
   ```
3. Falls die Container zuvor manuell gestoppt wurden, einfach starten:
   ```bash
   docker start ollama hwg-formcycle-checker
   ```
   *(Wurde der Server neu gebootet, starten beide Container durch die Docker-Restart-Policy vollautomatisch).*
4. Im Browser aufrufen:
   **`http://localhost:8080`**
