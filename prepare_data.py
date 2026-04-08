import os
import json
from src.loader import load_pdf
from src.chunker import chunk_text

# ✅ Create folder if not exists
os.makedirs("processed", exist_ok=True)

all_chunks = []

for file in os.listdir("data/pdfs"):
    if file.endswith(".pdf"):
        text = load_pdf(f"data/pdfs/{file}")
        chunks = chunk_text(text)
        all_chunks.extend(chunks)

with open("processed/chunks.json", "w") as f:
    json.dump(all_chunks, f)

print("Chunks created ✅")