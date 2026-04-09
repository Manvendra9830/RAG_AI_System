# 🚀 RAG AI System
- https://chatgpt.com/share/69d789af-3f00-8324-b2d7-4abcec340561
## 📌 Project Overview
This project is a Retrieval-Augmented Generation (RAG) system that allows users to:
- Upload PDF documents
- Convert them into embeddings
- Store them in FAISS (vector DB)
- Ask questions based on uploaded data using Gemini LLM

---

## 📂 Project Structure
```bash
LLM_advance_RAG_system/
│
├── data/
│   └── pdfs/                  # Uploaded PDF files
│
├── processed/
│   └── chunks.json            # Chunked text data
│
├── vector_store/
│   └── faiss_index.bin        # FAISS vector index
│
├── src/
│   ├── loader.py              # PDF text extraction
│   ├── chunker.py             # Text chunking logic
│
├── api.py                     # FastAPI backend (main app)
├── prepare_data.py            # PDF → text → chunks
├── build_index.py             # FAISS index builder
│
├── .env                       # Environment variables (API keys)
├── requirements.txt           # Dependencies
└── README.md
```
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

📁 Multi-document support
🧾 Metadata filtering & ranking
🗄️ PostgreSQL / MongoDB integration
👤 Authentication system
💬 Chat history memory
🌐 Frontend (React / Next.js)
🎙️ Voice-based querying
🔄 Streaming responses
⚙️ Migration to Django for large-scale systems
☁️ Deployment (AWS / GCP / Azure)

---

## 🔥 System Flow

Upload → Process → Store → Query → Retrieve → LLM → Answer

---

## 💡 Key Takeaways

- Chunking is critical  
- Retrieval > model  
- Always handle API failures  
- Structure = scalability  

