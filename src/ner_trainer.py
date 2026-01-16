import json
import random
import spacy
from spacy.training import Example
from spacy.training.iob_utils import offsets_to_biluo_tags
from pathlib import Path

# -------------------------------
# Load dataset
# -------------------------------
DATA_PATH = "training_data.json"

with open(DATA_PATH, "r", encoding="utf-8") as f:
    RAW_DATA = json.load(f)

print(f"Loaded {len(RAW_DATA)} raw samples")

# -------------------------------
# Create blank model
# -------------------------------
nlp = spacy.blank("en")
ner = nlp.add_pipe("ner")

LABELS = ["LAW", "BUSINESS_TYPE", "LOCATION", "EMPLOYEE_COUNT", "INDUSTRY"]
for label in LABELS:
    ner.add_label(label)

# -------------------------------
# CLEAN DATA FUNCTION
# -------------------------------
def clean_entities(nlp, text, entities):
    """
    - removes misaligned entities
    - removes overlapping entities
    """
    doc = nlp.make_doc(text)

    # 1. remove misaligned entities
    try:
        biluo = offsets_to_biluo_tags(doc, entities)
    except ValueError:
        return None  # completely broken example

    if "-" in biluo:
        return None

    # 2. remove overlapping entities
    cleaned = []
    occupied = set()

    for start, end, label in sorted(entities, key=lambda x: (x[0], -x[1])):
        overlap = False
        for i in range(start, end):
            if i in occupied:
                overlap = True
                break

        if not overlap:
            cleaned.append((start, end, label))
            for i in range(start, end):
                occupied.add(i)

    return cleaned if cleaned else None


# -------------------------------
# Build clean TRAIN_DATA
# -------------------------------
TRAIN_DATA = []

for text, ann in RAW_DATA:
    cleaned_entities = clean_entities(nlp, text, ann["entities"])
    if cleaned_entities:
        TRAIN_DATA.append((text, {"entities": cleaned_entities}))

print(f"Usable samples after cleaning: {len(TRAIN_DATA)}")

# -------------------------------
# Training
# -------------------------------
optimizer = nlp.begin_training()
N_EPOCHS = 20

for epoch in range(N_EPOCHS):
    random.shuffle(TRAIN_DATA)
    losses = {}

    for text, annotations in TRAIN_DATA:
        doc = nlp.make_doc(text)
        example = Example.from_dict(doc, annotations)
        nlp.update([example], drop=0.3, losses=losses)

    print(f"Epoch {epoch+1}/{N_EPOCHS} | Losses: {losses}")

# -------------------------------
# Save model
# -------------------------------
output_dir = Path("models/ner_model")
output_dir.mkdir(parents=True, exist_ok=True)
nlp.to_disk(output_dir)

print("✅ NER model trained successfully")
