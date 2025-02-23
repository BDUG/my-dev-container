# Minimales Python-Image als Basis
FROM python:3.9-slim

# Benötigte Systempakete installieren:
#   - graphviz: für Diagramme
#   - default-jre: für PlantUML (Java benötigt)
RUN apt-get update && apt-get install -y \
    graphviz \
    wget \
    default-jre \
    && rm -rf /var/lib/apt/lists/*

# Installiere Sphinx und die PlantUML-Erweiterung
RUN pip install --upgrade pip
RUN pip install --no-cache-dir sphinx sphinxcontrib-plantuml
RUN wget \
    "https://github.com/plantuml/plantuml/releases/download/v1.2025.1/plantuml-1.2025.1.jar" -o ./plantuml.lock

# Arbeitsverzeichnis für die Dokumentation
WORKDIR /docs

# Standardbefehl: Shell starten
CMD ["/bin/bash"]

