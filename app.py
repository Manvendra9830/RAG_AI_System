import faiss
import json
from sentence_transformers import SentenceTransformer
from google import genai
import os
from dotenv import load_dotenv

load_dotenv()
client = genai.Client(api_key=os.getenv("GEMINI_API_KEY"))

model = SentenceTransformer('all-MiniLM-L6-v2')

index = faiss.read_index("vector_store/faiss_index.bin")

with open("processed/chunks.json", "r") as f:
    texts = json.load(f)

query = input("Ask: ")
query_vec = model.encode([query]).astype('float32')

D, I = index.search(query_vec, 3)

context = "\n".join([texts[i] for i in I[0]])

prompt = f"""
Use the context below and your knowledge to answer:

Context:
{context}

Question: {query}
"""

response = client.models.generate_content(
    model="models/gemini-2.5-flash",
    contents=prompt
)

print("\nAnswer:\n", response.text)
