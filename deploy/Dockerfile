# ==============================================================================
# HWG Ludwigshafen - Formcycle Compliance Checker
# Minimales, produktionsreifes Dockerfile (Vanilla Python 3.11 Alpine)
# Keine externen Pip-Abhängigkeiten erforderlich (100% Standardbibliothek)
# Zero-Disk-Footprint (reine In-Memory-Verarbeitung via io.BytesIO)
# ==============================================================================

FROM python:3.11-alpine

# Metadaten
LABEL maintainer="HWG Ludwigshafen"
LABEL description="HWG Ludwigshafen Formcycle Compliance Dashboard & Hybrid Engine"

# Python-Optimierungen für Read-Only-Container (keine .pyc Schreibversuche)
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1

WORKDIR /app

# Erforderliche Verzeichnisse und Dateien kopieren
COPY data/ /app/data/
COPY scripts/test_rule_engine.py /app/scripts/test_rule_engine.py
COPY scripts/generate_chat_ai_prompt.py /app/scripts/generate_chat_ai_prompt.py
COPY web/ /app/web/

# Sicherheitsbest-Practice: Als nicht-privilegierter Benutzer ausführen
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

CMD ["python", "web/server.py"]
