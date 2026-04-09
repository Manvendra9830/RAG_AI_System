# 🚀 RAG AI System

## 📌 Project Overview
This project is a Retrieval-Augmented Generation (RAG) system that allows users to:
- Upload PDF documents
- Convert them into embeddings
- Store them in FAISS (vector DB)
- Ask questions based on uploaded data using Gemini LLM

---

## 📂 Project Structure
LLM_advance_RAG_system/
│
├── data/pdfs/              # Uploaded PDFs
├── processed/chunks.json   # Chunked text
├── vector_store/faiss_index.bin
│
├── src/
│   ├── loader.py           # PDF text extraction
│   ├── chunker.py          # Text chunking
│
├── api.py                  # Main FastAPI backend
├── prepare_data.py         # Initial data processing
├── build_index.py          # FAISS index creation
├── .env                    # API keys
├── requirements.txt

---

## ⚙️ Setup & Installation

### 1. Create Conda Environment
conda create -n faiss-gpu python=3.10
conda activate faiss-gpu

### 2. Install Libraries
pip install -r requirements.txt

### 3. Add API Key
Create .env file:
GEMINI_API_KEY=your_key_here

---

## ▶️ Run Project

python -m uvicorn api:app --reload

Open:
http://127.0.0.1:8000/docs

---

## 🧪 Testing

Upload → /upload  
Ask → /ask

---

## ⚠️ Common Errors & Learnings

- ModuleNotFound → install in correct env  
- Folder missing → create directories  
- API key leak → use .env  
- 503 error → retry logic  
- Swagger bug → use single file upload  

---

## 🚀 Future Roadmap

1. Multi-file upload  
2. Metadata tracking  
3. Database (PostgreSQL)  
4. User system  
5. Chat history  
6. Voice integration  
7. Frontend  
8. use django framework instead of fastAPI
9. use webhooks and other tools to make it good and scalable

---

## 🔥 System Flow

Upload → Process → Store → Query → Retrieve → LLM → Answer

---

## 💡 Key Takeaways

- Chunking is critical  
- Retrieval > model  
- Always handle API failures  
- Structure = scalability  

