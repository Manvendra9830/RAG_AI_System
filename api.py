from fastapi import FastAPI, HTTPException, UploadFile, File
from pydantic import BaseModel
import faiss
import json
from sentence_transformers import SentenceTransformer
from google import genai
import os
from dotenv import load_dotenv
import time
from src.loader import load_pdf
from src.chunker import chunk_text

# ===============================
# LOAD ENV
# ===============================
load_dotenv()

app = FastAPI()

# ===============================
# LOAD MODELS
# ===============================
model = SentenceTransformer('all-MiniLM-L6-v2')
index = faiss.read_index("vector_store/faiss_index.bin")

with open("processed/chunks.json", "r", encoding="utf-8") as f:
    texts = json.load(f)

# 🔥 FIX: Normalize old + new data
normalized_texts = []
for item in texts:
    if isinstance(item, str):
        normalized_texts.append({"text": item, "source": "old_data"})
    else:
        normalized_texts.append(item)

texts = normalized_texts

client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

# ===============================
# REQUEST SCHEMA
# ===============================
class QueryRequest(BaseModel):
    query: str

# ===============================
# HOME
# ===============================
@app.get("/")
def home():
    return {"message": "RAG API running 🚀"}

# ===============================
# LLM CALL (IMPROVED)
# ===============================
def call_llm(prompt):
    models = [
        "models/gemini-2.5-flash",
        "models/gemini-1.5-flash",
        "models/gemini-flash-latest"
    ]

    generation_config = {
        "temperature": 0.3,          # less randomness → more accuracy
        "max_output_tokens": 800     # longer answers
    }

    for model_name in models:
        for _ in range(2):
            try:
                response = client.models.generate_content(
                    model=model_name,
                    contents=prompt,
                    config=generation_config
                )
                return response.text
            except Exception as e:
                print(f"Retrying {model_name}...", e)
                time.sleep(2)

    return "LLM busy, try again"

# ===============================
# ASK (IMPROVED)
# ===============================
@app.post("/ask")
def ask_question(req: QueryRequest):
    try:
        query = req.query

        # 🔹 Query embedding
        query_vec = model.encode([query]).astype('float32')

        # 🔹 Retrieve more candidates
        D, I = index.search(query_vec, 10)

        # 🔹 Remove duplicate chunks
        seen = set()
        context_list = []

        for i in I[0]:
            item = texts[i]

            chunk_text_value = item["text"] if isinstance(item, dict) else str(item)

            if chunk_text_value not in seen:
                context_list.append(chunk_text_value)
                seen.add(chunk_text_value)

        context = "\n".join(context_list[:8])  # limit size

        print("\n===== CONTEXT =====\n", context)

        # 🔥 IMPROVED PROMPT
        prompt = f"""
You are an intelligent assistant.

Use BOTH:
1. The provided context (PRIMARY source)
2. Your general knowledge (SECONDARY, only if needed)

Instructions:
- Prioritize context first
- If context is incomplete, enhance with your knowledge
- Be detailed and structured
- Do NOT hallucinate unknown facts
- If unsure, say "Not clearly mentioned"

Context:
{context}

Question:
{query}

Answer in a clear and structured way:
"""

        answer = call_llm(prompt)

        return {
            "query": query,
            "context": context,
            "answer": answer
        }

    except Exception as e:
        print("ERROR:", e)
        raise HTTPException(status_code=500, detail="Query failed")
# ===============================
# UPLOAD
# ===============================
@app.post("/upload")
async def upload_file(file: UploadFile = File(...)):
    try:
        if not file.filename.endswith(".pdf"):
            raise HTTPException(status_code=400, detail="Only PDF allowed")

        os.makedirs("data/pdfs", exist_ok=True)

        file_path = f"data/pdfs/{file.filename}"

        if os.path.exists(file_path):
            return {"message": "File already exists"}

        # Save file
        with open(file_path, "wb") as f:
            f.write(await file.read())

        # Extract text
        text = load_pdf(file_path)

        if not text.strip():
            raise HTTPException(status_code=400, detail="Empty PDF")

        # Chunk
        chunks = chunk_text(text, chunk_size=300, overlap=50)

        # Embeddings
        embeddings = model.encode(chunks).astype('float32')

        index.add(embeddings)

        # Store with metadata
        global texts
        new_data = [
            {"text": chunk, "source": file.filename}
            for chunk in chunks
        ]

        texts.extend(new_data)

        # Save updated
        with open("processed/chunks.json", "w", encoding="utf-8") as f:
            json.dump(texts, f)

        faiss.write_index(index, "vector_store/faiss_index.bin")

        return {
            "message": f"{file.filename} uploaded successfully 🚀",
            "chunks_added": len(chunks)
        }

    except Exception as e:
        print("UPLOAD ERROR:", e)
        raise HTTPException(status_code=500, detail="Upload failed")