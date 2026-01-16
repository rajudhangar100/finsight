import json
import os
import re

RAW_DIR = "data/knowledge/raw_docs"
OUT_DIR = "data/knowledge/chunks"

os.makedirs(OUT_DIR, exist_ok=True)

def clean_text(text):
    remove_phrases = [
        "Goods and Services Tax",
        "Click here to see this page in full context",
        "FAQs >"
    ]
    for p in remove_phrases:
        text = text.replace(p, "")
    text = re.sub(r"\s+", " ", text)
    return text.strip()

def is_epf_style(text):
    """
    EPF pages contain patterns like:
    190 - Question
    191 - Question
    """
    return bool(re.search(r"\d+\s*-\s*[A-Z]", text))

def chunk_epf_style(text):
    """
    Each numbered item is a QUESTION ONLY.
    """
    chunks = []
    matches = re.findall(r"(\d+)\s*-\s*(.+?)(?=\s\d+\s*-\s|$)", text)

    for q_no, question in matches:
        chunks.append({
            "question": question.strip(),
            "answer": None
        })

    return chunks

def chunk_faq_style(text):
    """
    Handles:
    1. Question Answer...
    """
    chunks = []
    parts = re.split(r"\s(?=\d+\.\s)", text)

    for part in parts:
        m = re.match(r"(\d+)\.\s*(.+)", part.strip())
        if not m:
            continue

        qa_text = m.group(2)
        sentences = re.split(r"(?<=[.?])\s+", qa_text)

        question = sentences[0].strip()
        answer = " ".join(sentences[1:]).strip()

        if question:
            chunks.append({
                "question": question,
                "answer": answer if answer else None
            })

    return chunks

# ================= MAIN =================
for category in os.listdir(RAW_DIR):
    raw_cat_dir = os.path.join(RAW_DIR, category)
    out_cat_dir = os.path.join(OUT_DIR, category)

    if not os.path.isdir(raw_cat_dir):
        continue

    os.makedirs(out_cat_dir, exist_ok=True)

    for file in os.listdir(raw_cat_dir):
        if not file.endswith(".json"):
            continue

        with open(os.path.join(raw_cat_dir, file), "r", encoding="utf-8") as f:
            doc = json.load(f)

        text = clean_text(doc["text"])

        # Decide chunking strategy
        if is_epf_style(text):
            faq_chunks = chunk_epf_style(text)
        else:
            faq_chunks = chunk_faq_style(text)

        structured_chunks = []
        for i, c in enumerate(faq_chunks, start=1):
            structured_chunks.append({
                "chunk_id": f"{file.replace('.json','')}_Q{i}",
                "title": doc["title"],
                "question": c["question"],
                "answer": c["answer"],
                "law": doc["law"],
                "intent": doc["intent"],
                "region": doc["region"]
            })

        with open(os.path.join(out_cat_dir, file), "w", encoding="utf-8") as f:
            json.dump(structured_chunks, f, indent=2, ensure_ascii=False)

        print(f"✅ Chunked {category}/{file}: {len(structured_chunks)} chunks")
