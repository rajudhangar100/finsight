import sqlite3

DB_PATH = "db/finsight.db"

def get_candidate_faq_ids(intent, law=None, region=None):
    conn = sqlite3.connect(DB_PATH)
    cur = conn.cursor()

    query = "SELECT faq_id FROM faq_metadata WHERE intent = ?"
    params = [intent]

    if law:
        query += " AND law LIKE ?"
        params.append(f"%{law}%")


    cur.execute(query, params)
    rows = cur.fetchall()
    conn.close()

    return [r[0] for r in rows]
