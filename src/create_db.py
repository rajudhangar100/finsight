import sqlite3
import os

os.makedirs("db", exist_ok=True)

conn = sqlite3.connect("db/finsight.db")
cur = conn.cursor()

cur.execute("""
CREATE TABLE IF NOT EXISTS faq_metadata (
    faq_id TEXT PRIMARY KEY,
    title TEXT,
    law TEXT,
    intent TEXT,
    region TEXT,
    question TEXT,
    answer TEXT
)
""")

cur.execute("""
CREATE TABLE IF NOT EXISTS faq_embeddings (
    faq_id TEXT,
    vector_id INTEGER
)
""")

conn.commit()
conn.close()

print("✅ Database initialized")
