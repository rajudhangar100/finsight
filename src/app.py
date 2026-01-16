from fastapi import FastAPI
from pydantic import BaseModel

from intent_infer import predict_intent
from simple_ner import extract_entities
from rag_answer import generate_answer  # your Groq RAG

app = FastAPI(title="FinSight API")

class QueryRequest(BaseModel):
    query: str

@app.post("/chat")
def chat(req: QueryRequest):
    intent, confidence = predict_intent(req.query)
    entities = extract_entities(req.query)

    answer = generate_answer(req.query)

    return {
        "intent": intent,
        "confidence": round(confidence, 2),
        "entities": entities,
        "answer": answer
    }
