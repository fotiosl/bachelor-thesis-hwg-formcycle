# ==============================================================================
# HWG Ludwigshafen - Formcycle Compliance Checker
# Minimales, produktionsreifes Dockerfile (Vanilla Python 3.11 Alpine)
# Keine externen Pip-Abhängigkeiten erforderlich (100% Standardbibliothek)
# Image-Größe: ca. 55 MB
# ==============================================================================

FROM python:3.11-alpine

# Metadaten
LABEL maintainer="HWG Ludwigshafen"
LABEL description="HWG Ludwigshafen Formcycle Compliance Dashboard & Engine"

WORKDIR /app

# Erforderliche Verzeichnisse und Dateien kopieren
COPY data/ /app/data/
COPY scripts/test_rule_engine.py /app/scripts/test_rule_engine.py
COPY web/ /app/web/

# Sicherheitsbest-Practice: Als nicht-privilegierter Benutzer ausführen
RUN addgroup -S appgroup && adduser -S appuser -G appgroup
USER appuser

EXPOSE 8080

HEALTHCHECK --interval=30s --timeout=5s --start-period=5s --retries=3 \
  CMD python -c "import urllib.request; urllib.request.urlopen('http://localhost:8080/').read()" || exit 1

CMD ["python", "web/server.py"]
