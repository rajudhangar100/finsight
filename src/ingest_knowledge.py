import sqlite3

conn = sqlite3.connect("db/finsight.db")
cursor = conn.cursor()

cursor.execute("""
INSERT INTO legal_knowledge (
    intent, law, section, region, industry, summary, chunk_file
)
VALUES (?, ?, ?, ?, ?, ?, ?)
""", (
    "REGISTRATION",
    "GST Act",
    "Section 22",
    "India",
    "All",
    "GST registration requirements for suppliers",
    "data/knowledge/chunks/gst_registration_chunks.json"
))

conn.commit()
conn.close()

print("Knowledge ingested successfully")
