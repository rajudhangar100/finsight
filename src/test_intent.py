import torch
from transformers import AutoTokenizer, AutoModelForSequenceClassification

MODEL_PATH = "src/models/intent_model"

tokenizer = AutoTokenizer.from_pretrained(MODEL_PATH)
model = AutoModelForSequenceClassification.from_pretrained(MODEL_PATH)

labels = ["TAXATION", "REGISTRATION", "LABOUR_LAW", "COMPLIANCE"]

def predict_intent(text):
    inputs = tokenizer(text, return_tensors="pt", truncation=True, padding=True)
    with torch.no_grad():
        outputs = model(**inputs)
    probs = torch.softmax(outputs.logits, dim=1)
    predicted_class = torch.argmax(probs).item()
    return labels[predicted_class], probs[0][predicted_class].item()

# Test
query = "How often should ROC filings be done?"
intent, confidence = predict_intent(query)

print("Intent:", intent)
print("Confidence:", round(confidence, 2))
