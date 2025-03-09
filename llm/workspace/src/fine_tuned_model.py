import torch
from datasets import Dataset
from transformers import AutoTokenizer,  AutoModelForSequenceClassification, TrainingArguments, Trainer
import numpy as np
import evaluate 


# Unser Beispiel-Datensatz
texts = [
    "Eine Klage ist die formelle Einreichung einer Beschwerde vor Gericht.",
    "Ein Vertrag ist eine rechtsverbindliche Vereinbarung zwischen zwei Parteien.",
    "Das Strafrecht befasst sich mit Verbrechen und deren Bestrafung."
]
labels = [0, 1, 2]  # Zivilrecht (0), Vertragsrecht (1), Strafrecht (2)

# Erstelle den Dataset
dataset = Dataset.from_dict({"text": texts, "label": labels})

# Train-Test-Split
dataset = dataset.train_test_split(test_size=0.3)

# Tokenizer laden
model_checkpoint = "bert-base-german-cased"
tokenizer = AutoTokenizer.from_pretrained(model_checkpoint)

# Tokenisierung der Texte
def preprocess_function(examples):
    return tokenizer(examples["text"], truncation=True, padding="max_length", max_length=128)

tokenized_datasets = dataset.map(preprocess_function, batched=True)


num_labels = 3  # Drei Klassen: Zivilrecht, Vertragsrecht, Strafrecht

model = AutoModelForSequenceClassification.from_pretrained(
    model_checkpoint, num_labels=num_labels
)


# Genauigkeitsmetrik
metric = evaluate.load("accuracy")

def compute_metrics(eval_pred):
    logits, labels = eval_pred
    predictions = np.argmax(logits, axis=-1)
    return metric.compute(predictions=predictions, references=labels)

# Trainingsargumente
training_args = TrainingArguments(
    output_dir="./results",
    evaluation_strategy="epoch",
    save_strategy="epoch",
    learning_rate=2e-5,
    per_device_train_batch_size=4,
    per_device_eval_batch_size=4,
    num_train_epochs=5,
    weight_decay=0.01,
    logging_dir="./logs",
    logging_steps=10,
)

# Trainer-Objekt
trainer = Trainer(
    model=model,
    args=training_args,
    train_dataset=tokenized_datasets["train"],
    eval_dataset=tokenized_datasets["test"],
    tokenizer=tokenizer,
    compute_metrics=compute_metrics,
)

# Modell trainieren
trainer.train()


# Modell speichern
trainer.save_model("fine-tuned-bert-law")
tokenizer.save_pretrained("fine-tuned-bert-law")

# Test mit einer neuen Eingabe
test_text = "Ein Vertrag verpflichtet beide Parteien zur Erfüllung ihrer Pflichten."
inputs = tokenizer(test_text, return_tensors="pt", truncation=True, padding="max_length", max_length=128)

# Vorhersage
model.eval()
with torch.no_grad():
    outputs = model(**inputs)
    logits = outputs.logits
    predicted_class = torch.argmax(logits, dim=-1).item()

# Rechtsgebiet ausgeben
labels_map = {0: "Zivilrecht", 1: "Vertragsrecht", 2: "Strafrecht"}
print(f"Das Modell sagt: {labels_map[predicted_class]}")
