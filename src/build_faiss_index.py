import sqlite3
import faiss
import numpy as np
import pickle
from sentence_transformers import SentenceTransformer

DB_PATH = "db/finsight.db"
INDEX_PATH = "vector_store/faq_index.faiss"
ID_PATH = "vector_store/faq_ids.pkl"

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

cur.execute("""
SELECT faq_id, question, COALESCE(answer, '')
FROM faq_metadata
""")

rows = cur.fetchall()
conn.close()

texts = [f"Q: {q}\nA: {a}" for _, q, a in rows]
faq_ids = [fid for fid, _, _ in rows]

embeddings = model.encode(texts, show_progress_bar=True)
embeddings = np.array(embeddings).astype("float32")

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, INDEX_PATH)
with open(ID_PATH, "wb") as f:
    pickle.dump(faq_ids, f)

print(f"✅ FAISS index rebuilt with {len(faq_ids)} FAQs")
