# RAG-
Local RAG (FAISS + Ollama) — A local retrieval-augmented generation app that lets you upload documents, embed them using FAISS, and query them via a local LLM.

# Local RAG (FAISS + Ollama) — Quickstart

## Overview
This app allows you to upload documents, automatically chunk and embed them (local), store vectors in FAISS, and ask queries answered by a local LLM (Ollama).
This project implements a **Retrieval-Augmented Generation (RAG)** system that allows users to:
- Upload documents (PDFs or text)
- Automatically extract, chunk, and embed content locally
- Store document vectors using **FAISS**
- Ask questions answered by a **local LLM (Ollama)** or other LLMs like OpenAI or Gemini

Built using **FastAPI**, this project runs fully offline and can be deployed locally or via Docker.

## 🧩 Features
✅ Upload multiple PDF/Text files  
✅ Automatic text extraction, chunking, and embedding  
✅ FAISS-based vector search  
✅ Querying via local or external LLMs (Ollama, OpenAI, Gemini)  
✅ REST API endpoints for upload and query  
✅ Dockerized for easy deployment  
✅ Includes metadata storage and testing support  


## ⚙️ Project Structure
app/
├── api/
│ ├── upload.py # Handles document uploads
│ ├── query.py # Handles user queries
│
├── ingest/
│ ├── processor.py # Extracts, chunks, and embeds documents
│
├── db/
│ ├── vector_store.py # FAISS vector database
│ ├── init_db.py # Initializes FAISS index
│
├── utils/
│ ├── file_parsers.py # PDF/Text parsing helpers
│
├── main.py # FastAPI main entry point
├── config.py # Configuration and API keys
├── requirements.txt
├── Dockerfile
├── docker-compose.yml
└── tests/ # Unit and integration tests


---

## 🧰 Prerequisites
- Python **3.10+**
- **pip**
- **Git** (optional)
- **Ollama** installed → [https://ollama.ai/download](https://ollama.ai/download)

> 💡 Alternatively, you can use Docker (see below).

---


## Option A — Run locally (recommended for development)

1. Create & activate venv:
   ```bash
   python -m venv .venv
   source .venv/bin/activate   # Linux / macOS
   .venv\\Scripts\\activate    # Windows PowerShell

2️⃣ Install dependencies

      pip install -r requirements.txt

3️⃣ Run the FastAPI server

      uvicorn app.main:app --reload

🐳Option B — Run with Docker

Make sure Docker is installed and running.

docker-compose up --build
