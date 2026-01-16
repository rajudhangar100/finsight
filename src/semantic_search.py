import faiss
import pickle
import sqlite3
import numpy as np
from sentence_transformers import SentenceTransformer

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

index = faiss.read_index("vector_store/faq_index.faiss")
with open("vector_store/faq_ids.pkl", "rb") as f:
    faq_ids = pickle.load(f)

query = "What document can I upload as a supporting document for proof of bank account?"

q_emb = model.encode([query]).astype("float32")
D, I = index.search(q_emb, k=3)

conn = sqlite3.connect("db/finsight.db")
cur = conn.cursor()

for idx in I[0]:
    faq_id = faq_ids[idx]
    cur.execute("""
    SELECT question, answer
    FROM faq_metadata
    WHERE faq_id = ?
    """, (faq_id,))
    q, a = cur.fetchone()
    print("\nQ:", q)
    print("A:", a)

conn.close()
