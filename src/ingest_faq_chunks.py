import os
import json
import sqlite3

DB_PATH = "db/finsight.db"

CHUNK_DIRS = [
    "data/knowledge/chunks/gst_registration",
    "data/knowledge/chunks/msme",
    "data/knowledge/chunks/labour"
]

RAW_LABOUR_DIR = "data/knowledge/raw_docs/labour"

conn = sqlite3.connect(DB_PATH)
cur = conn.cursor()

inserted = 0

# ===============================
# 1️⃣ INGEST CHUNKED FAQ FILES
# ===============================
for dir_path in CHUNK_DIRS:
    if not os.path.exists(dir_path):
        continue

    for file in os.listdir(dir_path):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(dir_path, file), "r", encoding="utf-8") as f:
            chunks = json.load(f)

        for c in chunks:
            cur.execute("""
            INSERT OR IGNORE INTO faq_metadata
            (faq_id, title, law, intent, region, question, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                c["chunk_id"],
                c["title"],
                c["law"],
                c["intent"],
                c["region"],
                c["question"],
                c.get("answer")
            ))
            inserted += 1

# ===============================
# 2️⃣ INGEST EPF / ESIC RAW FAQs
# ===============================
if os.path.exists(RAW_LABOUR_DIR):
    for file in os.listdir(RAW_LABOUR_DIR):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(RAW_LABOUR_DIR, file), "r", encoding="utf-8") as f:
            doc = json.load(f)

        if "faqs" not in doc:
            continue

        for i, faq in enumerate(doc["faqs"], start=1):
            faq_id = f"{file.replace('.json','')}_Q{i}"

            cur.execute("""
            INSERT OR IGNORE INTO faq_metadata
            (faq_id, title, law, intent, region, question, answer)
            VALUES (?, ?, ?, ?, ?, ?, ?)
            """, (
                faq_id,
                doc["title"],
                doc["law"],
                doc["intent"],
                doc["region"],
                faq["question"],
                faq["answer"]
            ))
            inserted += 1

# ===============================
# ✅ COMMIT & CLOSE ONCE
# ===============================
conn.commit()
conn.close()

print(f"✅ Successfully ingested {inserted} FAQ records into SQLite")
