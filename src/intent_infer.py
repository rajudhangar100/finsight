import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "models/intent_model"
LABELS = ["TAXATION", "REGISTRATION", "LABOUR_LAW", "COMPLIANCE"]

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    idx = torch.argmax(probs).item()
    return LABELS[idx], float(probs[0][idx])
