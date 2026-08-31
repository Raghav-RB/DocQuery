# DocQuery

> An AI-powered document question-answering system built with FastAPI, Google Gemini, PostgreSQL, and pgvector.

![Python](https://img.shields.io/badge/Python-3.x-3776AB?style=for-the-badge&logo=python&logoColor=white)
![FastAPI](https://img.shields.io/badge/FastAPI-REST%20API-009688?style=for-the-badge&logo=fastapi&logoColor=white)
![Gemini](https://img.shields.io/badge/Google%20Gemini-API-4285F4?style=for-the-badge&logo=google&logoColor=white)
![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-4169E1?style=for-the-badge&logo=postgresql&logoColor=white)
![pgvector](https://img.shields.io/badge/pgvector-Vector%20Search-336791?style=for-the-badge)
![Docker](https://img.shields.io/badge/Docker-Containerized-2496ED?style=for-the-badge&logo=docker&logoColor=white)
![AWS](https://img.shields.io/badge/AWS-EC2-FF9900?style=for-the-badge&logo=amazonaws&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-yellow.svg?style=for-the-badge)

🌐 **Live App:** http://13.232.134.110/ · 🔗 **Repo:** https://github.com/Raghav-RB/DocQuery

---

## Table of Contents

- [Overview](#overview)
- [Key Features](#key-features)
- [Architecture](#architecture)
- [How It Works](#how-it-works)
- [Tech Stack](#tech-stack)
- [Project Structure](#project-structure)
- [Getting Started](#getting-started)
- [API Reference](#api-reference)
- [Testing](#testing)
- [Deployment](#deployment)
- [Security Notes](#security-notes)
- [Limitations & Future Work](#limitations--future-work)
- [Author](#author)

---

## Overview

DocQuery is an end-to-end **Retrieval-Augmented Generation (RAG)** application that lets users upload PDF documents and ask natural-language questions about their content.

Instead of sending an entire document to a language model, DocQuery converts the document into searchable vector embeddings, retrieves only the most relevant chunks for a given question, and passes those chunks to the LLM as grounded context. Every generated answer is returned alongside the exact source (filename, page, and chunk) it was drawn from.

```
PDF → Text Extraction → Chunking → Embeddings → PostgreSQL + pgvector
                                                          │
Question → Question Embedding → Vector Similarity Search │
                                          │                
                                     Top-K Chunks → Context → RAG Prompt → Gemini LLM → Answer + Sources
```

## Key Features

- 📄 PDF upload through a browser interface
- 🔤 Page-by-page text extraction (PyMuPDF)
- 🧩 Sentence-based chunking with overlap
- 🧠 Semantic embeddings via Google Gemini
- 🔎 Vector similarity search with pgvector (Top-K retrieval)
- 🤖 Grounded answer generation with Gemini
- 📚 Source attribution (filename, page, chunk)
- 🐳 Dockerized PostgreSQL + pgvector
- ☁️ Deployed on AWS EC2 with Nginx + systemd

## Architecture

**Application**

```
User Browser → Frontend (HTML/CSS/JS) → FastAPI Backend
                                              │
                          ┌───────────────────┴───────────────────┐
                          ▼                                       ▼
              PostgreSQL + pgvector                       Google Gemini API
           (chunks, embeddings, metadata)             (embeddings, answer generation)
```

**AWS Deployment**

```
Internet → AWS EC2 (Ubuntu)
                │
    ┌───────────┴────────────┐
    ▼                        ▼
  Nginx (Port 80)      systemd → FastAPI + Uvicorn
    │                        │
  Frontend              ┌────┴─────┐
  (HTML/CSS/JS)         ▼          ▼
                  PostgreSQL   Gemini API
                  + pgvector   (embeddings, LLM)
                  (Docker)
```

## How It Works

DocQuery has two workflows: **document ingestion** and **question answering**.

### Document Ingestion

| Step | Description |
|---|---|
| Upload | Frontend sends the PDF to `POST /upload`; FastAPI validates it, stores it temporarily, and removes it after processing. |
| Extraction | PyMuPDF extracts text page by page, preserving page numbers for later source attribution. |
| Chunking | Sentence-based chunking splits text into pieces up to **1000 characters**, carrying **1 sentence of overlap** into the next chunk. |
| Embedding | Each chunk is embedded with Gemini's `gemini-embedding-2` model (**3072 dimensions**). |
| Storage | Chunks are stored in PostgreSQL + pgvector with `text_content`, `embedding`, `filename`, `page`, and `chunk_index`. |

### Question Answering (RAG)

| Step | Description |
|---|---|
| Question Embedding | The question is embedded with the same Gemini model used for document chunks. |
| Similarity Search | pgvector ranks chunks by cosine distance (`embedding <=> query_embedding`). |
| Top-K Retrieval | The **K = 3** closest chunks are retrieved. |
| Context Construction | Retrieved chunks are formatted with their source, page, and content. |
| RAG Prompt | Combines context + question + an instruction to answer only from the provided context, or state that the answer wasn't found. |
| Answer Generation | The prompt is sent to the Gemini LLM, which returns a grounded answer. |
| Source Attribution | The response includes the filename, page, and chunk index for every source used. |

**Example response**

```
Answer:
The role mentioned in the document is "Ace Frontier Engineer".

Sources:
- Student Brochure_2027 Cognizant Ace Team program.pdf — Page 3, Chunk 0
```

## Tech Stack

| Layer | Technology |
|---|---|
| Language | Python |
| Backend | FastAPI + Uvicorn |
| LLM & Embeddings | Google Gemini (`gemini-3.6-flash`, `gemini-embedding-2`) |
| Database | PostgreSQL |
| Vector Search | pgvector |
| PDF Processing | PyMuPDF |
| DB Driver | psycopg |
| Frontend | HTML / CSS / JavaScript |
| Infrastructure | Docker, Nginx, systemd |
| Cloud | AWS EC2 |

## Project Structure

```
DocQuery/
├── app/
│   ├── api/routes/       # health, documents, chat endpoints
│   ├── db/schema.sql      # PostgreSQL + pgvector schema
│   ├── models/schemas.py  # Pydantic request/response models
│   ├── rag/                # embeddings, retrieval, context, prompt, service
│   ├── services/           # database, document_loader, chunker, ingestion, llm
│   └── main.py
├── frontend/
│   └── index.html
├── tests/
├── docker-compose.yml
├── requirements.txt
└── .env
```

## Getting Started

### Prerequisites

- Python 3.x, Docker & Docker Compose, Git, a Google Gemini API key

### 1. Clone & Install

```bash
git clone https://github.com/Raghav-RB/DocQuery.git
cd DocQuery

python -m venv venv
source venv/bin/activate   # venv\Scripts\activate on Windows

pip install -r requirements.txt
pip install python-multipart
```

### 2. Configure Environment

Create a `.env` file in the project root:

```env
GEMINI_API_KEY=your_gemini_api_key

DATABASE_HOST=127.0.0.1
DATABASE_PORT=5433
DATABASE_NAME=docquery
DATABASE_USER=docquery
DATABASE_PASSWORD=docquery_password
```

> ⚠️ Never commit `.env` or expose your Gemini API key.

### 3. Set Up the Database

```bash
docker compose up -d
docker compose exec -T postgres psql -U docquery -d docquery < app/db/schema.sql
```

> PostgreSQL runs on host port `5433`, mapped to the container's `5432`.

### 4. Run the Backend

```bash
uvicorn app.main:app --reload
```

- API: `http://127.0.0.1:8000`
- Interactive docs: `http://127.0.0.1:8000/docs`

### 5. Run the Frontend

```bash
cd frontend
python -m http.server 5500
```

- Frontend: `http://127.0.0.1:5500`

### Usage

1. Open the frontend → select a PDF → click **Upload**
2. Wait for ingestion confirmation
3. Enter a question → click **Ask Question**
4. View the generated answer and its sources

## API Reference

**Health Check**
```http
GET /health
```

**Upload Document**
```http
POST /upload
Content-Type: multipart/form-data

file=<PDF file>
```
```json
{ "message": "Document uploaded and ingested successfully", "filename": "example.pdf" }
```

**Ask a Question**
```http
POST /ask
Content-Type: application/json

{ "question": "What is this document about?" }
```
```json
{
  "question": "What is this document about?",
  "answer": "Generated answer based on the retrieved document context.",
  "sources": [
    { "filename": "example.pdf", "page": 3, "chunk_index": 0 }
  ]
}
```

## Testing

DocQuery includes tests covering the core pipeline — PDF extraction, chunking, embedding generation, vector retrieval, context construction, and RAG generation — plus direct API testing (`/upload`, `/ask`) and end-to-end browser workflow testing.

## Deployment

Deployed on an AWS EC2 Ubuntu instance:

| Component | Purpose |
|---|---|
| AWS EC2 | Hosts the application |
| Nginx | Serves the frontend |
| systemd | Keeps FastAPI + Uvicorn running |
| Docker | Runs PostgreSQL + pgvector |
| Gemini API | Embeddings + answer generation |

**Live:** http://13.232.134.110/

## Security Notes

This deployment is for demonstration and portfolio purposes only.

- `.env` and the Gemini API key are never committed or exposed
- SSH access is restricted to trusted IPs
- PostgreSQL (port `5433`) is not publicly exposed
- Current deployment uses HTTP, not HTTPS — avoid uploading confidential documents

## Limitations & Future Work

**Current limitations**
- PDF is the only supported upload format
- Retrieval uses Top-K similarity search with K = 3
- No HTTPS or authentication yet
- Answer quality depends on extraction, chunking, and retrieval quality; RAG does not guarantee factual correctness

**Planned improvements**
- HTTPS, custom domain, authentication & authorization
- Support for additional document formats
- Hybrid search and retrieval reranking
- RAG evaluation framework and observability/logging
- Production-grade error handling and a more scalable deployment

## Author

**Raghav Bharadwaj**
GitHub: [@Raghav-RB](https://github.com/Raghav-RB)

## License

Released under the [MIT License](LICENSE).
