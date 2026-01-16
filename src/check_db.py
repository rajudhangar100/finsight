# # import sqlite3

# # conn = sqlite3.connect("db/finsight.db")
# # cur = conn.cursor()

# # cur.execute("SELECT COUNT(*) FROM faq_metadata")
# # print("Total FAQs:", cur.fetchone()[0])

# # cur.execute("""
# # SELECT question, answer
# # FROM faq_metadata
# # LIMIT 2
# # """)

# # for q, a in cur.fetchall():
# #     print("\nQ:", q)
# #     print("A:", a)

# # conn.close()
# import sqlite3

# conn = sqlite3.connect("db/finsight.db")
# cur = conn.cursor()

# cur.execute("SELECT COUNT(*) FROM faq_metadata")
# print("Total FAQs:", cur.fetchone()[0])

# cur.execute("SELECT DISTINCT law FROM faq_metadata")
# print("Laws:", cur.fetchall())

# conn.close()
from sentence_transformers import SentenceTransformer
import faiss, pickle

index = faiss.read_index("vector_store/faq_index.faiss")
ids = pickle.load(open("vector_store/faq_ids.pkl","rb"))

model = SentenceTransformer("sentence-transformers/all-MiniLM-L6-v2")
q = model.encode(["Is authorised representative mandatory for GST?"]).astype("float32")

D, I = index.search(q, 3)
print([ids[i] for i in I[0]])
