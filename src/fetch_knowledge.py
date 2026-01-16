import sqlite3
import json

def fetch_by_intent(intent):
    conn = sqlite3.connect("db/finsight.db")
    cursor = conn.cursor()

    cursor.execute("""
    SELECT law, section, summary, chunk_file
    FROM legal_knowledge
    WHERE intent = ?
    """, (intent,))

    results = cursor.fetchall()
    conn.close()
    return results

records = fetch_by_intent("REGISTRATION")

for law, section, summary, chunk_file in records:
    print("Law:", law)
    print("Section:", section)
    print("Summary:", summary)

    with open(chunk_file, "r", encoding="utf-8") as f:
        chunks = json.load(f)

    for c in chunks:
        print("-", c["text"])
