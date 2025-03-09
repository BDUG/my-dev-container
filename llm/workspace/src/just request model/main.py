from transformers import pipeline

# Lade ein vortrainiertes Modell für die Textgenerierung
generator = pipeline("text-generation", model="gpt2")

# Generiere einen Text
result = generator("Once upon a time,", max_length=50)

# Ausgabe des generierten Textes
print(result[0]["generated_text"])
