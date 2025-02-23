# -- Erweiterungen konfigurieren --------------------------------------------
extensions = [
    'sphinxcontrib.plantuml',
    # ggf. weitere Extensions
]

# -- Pfad zur PlantUML-JAR-Datei (wenn du eine eigene verwenden möchtest) --
# Standardmäßig sollte sphinxcontrib-plantuml eine interne Version verwenden.
# Möchtest du eine lokale Version in /usr/share/plantuml/plantuml.jar nutzen,
# kannst du z. B.:
plantuml = "java -jar /plantuml-1.2025.1.jar"

# Falls du die Graphviz-Diagramme direkt einbinden willst
extensions.append('sphinx.ext.graphviz')

