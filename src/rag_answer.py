import os
import faiss
import pickle
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer
from groq import Groq

# ================= CONFIG =================
DB_PATH = "db/finsight.db"
FAISS_INDEX = "vector_store/faq_index.faiss"
FAQ_IDS = "vector_store/faq_ids.pkl"
TOP_K = 4

# ================= SAFETY CHECK =================
if not os.getenv("GROQ_API_KEY"):
    raise RuntimeError("❌ GROQ_API_KEY not found in environment variables")

# ================= INITIALIZE =================
embedder = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
client = Groq()

index = faiss.read_index(FAISS_INDEX)
with open(FAQ_IDS, "rb") as f:
    faq_ids = pickle.load(f)

# ================= RETRIEVAL =================
def retrieve_context(question):
    q_emb = embedder.encode([question]).astype("float32")
    _, I = index.search(q_emb, TOP_K)

    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    contexts = []
    for idx in I[0]:
        faq_id = faq_ids[idx]
        cur.execute(
            "SELECT question, answer FROM faq_metadata WHERE faq_id = ?",
            (faq_id,)
        )
        row = cur.fetchone()
        if row:
            q, a = row
            contexts.append(f"Q: {q}\nA: {a}")

    conn.close()
    return "\n\n".join(contexts)

# ================= GENERATION =================
def generate_answer(user_question):
    context = retrieve_context(user_question)

    if not context.strip():
        return "No relevant information found in the knowledge base."

    system_prompt = (
        "You are FinSight, a legal compliance assistant for Indian businesses. "
        "Answer ONLY using the provided context. "
        "Do NOT add new information. "
        "If the answer is not present, say: "
        "'Based on the available information, this cannot be determined.'"
    )

    user_prompt = f"""
Context:
{context}

User Question:
{user_question}

Answer clearly and concisely.
"""

    try:
        response = client.chat.completions.create(
            model="llama-3.3-70b-versatile",
            messages=[
                {"role": "system", "content": system_prompt},
                {"role": "user", "content": user_prompt},
            ],
            temperature=0.0,
            max_tokens=400,
        )

        return response.choices[0].message.content.strip()

    except Exception as e:
        return f"❌ Groq API error: {e}"

# ================= TEST =================
if __name__ == "__main__":
    question = "If an worker is paid wages on daily basis, then how the contribution is determined?"
    print("\nUser Question:", question)

    answer = generate_answer(question)
    print("\nFinSight Answer:\n", answer)
