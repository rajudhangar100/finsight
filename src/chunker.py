import json
import os

RAW_FILE = "data/knowledge/raw_docs/gst_registration.txt"
CHUNK_FILE = "data/knowledge/chunks/gst_registration_chunks.json"

os.makedirs("data/knowledge/chunks", exist_ok=True)

with open(RAW_FILE, "r", encoding="utf-8") as f:
    text = f.read()

sentences = text.split(".")
chunks = []
chunk_id = 1

for i in range(0, len(sentences), 2):
    chunk_text = ".".join(sentences[i:i+2]).strip()
    if chunk_text:
        chunks.append({
            "chunk_id": chunk_id,
            "text": chunk_text
        })
        chunk_id += 1

with open(CHUNK_FILE, "w", encoding="utf-8") as f:
    json.dump(chunks, f, indent=2)

print("Chunks created:", len(chunks))
