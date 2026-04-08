import faiss
import json
import os
from sentence_transformers import SentenceTransformer

# ✅ Create folder if not exists
os.makedirs("vector_store", exist_ok=True)

model = SentenceTransformer('all-MiniLM-L6-v2')

with open("processed/chunks.json", "r") as f:
    texts = json.load(f)

embeddings = model.encode(texts).astype('float32')

index = faiss.IndexFlatL2(embeddings.shape[1])
index.add(embeddings)

faiss.write_index(index, "vector_store/faiss_index.bin")

print("Index built and saved ✅")