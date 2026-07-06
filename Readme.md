# 🌿 Enterprise RAG Chatbot

::: {align="center"}
### Enterprise Retrieval-Augmented Generation (RAG) Chatbot

**Angular • FastAPI • FAISS • Sentence Transformers • Google Gemini**

Prototype developed during the **Tech Mahindra Internship Program**.

![Status](https://img.shields.io/badge/Status-Working-success)
![Python](https://img.shields.io/badge/Python-3.11-blue)
![Angular](https://img.shields.io/badge/Angular-19-red)
![FastAPI](https://img.shields.io/badge/FastAPI-Latest-009688)
:::

------------------------------------------------------------------------

# 📖 Overview

This project is an enterprise-style Retrieval-Augmented Generation (RAG)
chatbot that enables users to upload organizational documents and ask
natural-language questions grounded in those documents.

Unlike a traditional chatbot, answers are generated only after
retrieving semantically relevant document chunks, improving factual
accuracy and reducing hallucinations.

------------------------------------------------------------------------

# ✨ Features

-   Multi-format document upload (PDF, DOCX, TXT, JSON)
-   Intelligent document parsing
-   Semantic chunking
-   Sentence Transformer embeddings (BAAI/bge-small-en-v1.5)
-   FAISS vector database
-   Google Gemini answer generation
-   Angular Material frontend
-   FastAPI REST backend
-   Source attribution for every answer
-   Modular architecture ready for future Azure migration

------------------------------------------------------------------------

# 🏗️ System Architecture

``` text
                Angular Frontend
                       │
                 HTTP REST APIs
                       │
                  FastAPI Backend
         ┌─────────────┴─────────────┐
         │                           │
   Upload Pipeline             Chat Pipeline
         │                           │
     Document Parser          Query Embedding
         │                           │
     Smart Chunking         Semantic Retrieval
         │                           │
Sentence Embeddings         Prompt Construction
         │                           │
      FAISS Index ─────────► Google Gemini
                       │
                 Final Answer + Sources
```

------------------------------------------------------------------------

# ⚙️ Technology Stack

  Layer             Technology
  ----------------- ------------------------------
  Frontend          Angular 19, Angular Material
  Backend           FastAPI
  Language          Python
  Vector Store      FAISS
  Embeddings        BAAI/bge-small-en-v1.5
  LLM               Google Gemini
  Version Control   Git & GitHub

------------------------------------------------------------------------

# 📁 Project Structure

``` text
ragbot_project/
│
├── backend/
│   ├── api/
│   ├── indexing/
│   ├── models/
│   ├── prompts/
│   ├── services/
│   ├── utils/
│   ├── data/
│   ├── app.py
│   └── requirements.txt
│
├── frontend/
│   └── ui/
│       ├── src/
│       ├── angular.json
│       ├── package.json
│       └── ...
│
└── README.md
```

------------------------------------------------------------------------

# 🚀 Getting Started

## 1. Clone

``` bash
git clone <repository-url>
cd ragbot_project
```

## 2. Backend

``` powershell
cd backend
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

Create `.env`

``` env
GOOGLE_API_KEY=YOUR_GEMINI_API_KEY
```

Run backend

``` powershell
uvicorn app:app --reload
```

Swagger:

http://127.0.0.1:8000/docs

------------------------------------------------------------------------

## 3. Frontend

``` powershell
cd frontend/ui
npm install
ng serve
```

Open:

http://localhost:4200

------------------------------------------------------------------------

# ▶️ Running the Project

Backend terminal

``` powershell
cd backend
venv\Scripts\activate
uvicorn app:app --reload
```

Frontend terminal

``` powershell
cd frontend/ui
ng serve
```

------------------------------------------------------------------------

# 🔌 REST APIs

## GET /health

Health check endpoint.

## POST /api/upload

Uploads and indexes supported documents.

Supported:

-   PDF
-   DOCX
-   TXT
-   JSON

## POST /api/chat

Example request

``` json
{
  "question":"What is the attendance policy?"
}
```

Returns

-   Generated answer
-   Source documents
-   Similarity scores

------------------------------------------------------------------------

# 🧠 RAG Workflow

1.  Upload document
2.  Parse content
3.  Chunk text
4.  Generate embeddings
5.  Store vectors in FAISS
6.  Embed user query
7.  Retrieve relevant chunks
8.  Build prompt
9.  Generate grounded answer using Gemini
10. Return answer with sources

------------------------------------------------------------------------

# 📸 Suggested Screenshots

-   Home Page
-   Upload Success
-   Chat Response
-   Swagger API
-   Folder Structure

------------------------------------------------------------------------

# 🛣️ Future Enhancements

-   Azure Blob Storage
-   Azure AI Search
-   Azure OpenAI
-   Authentication
-   Chat History
-   Streaming Responses
-   Docker
-   CI/CD
-   Kubernetes

------------------------------------------------------------------------

# 🐞 Troubleshooting

**Frontend cannot reach backend**

-   Verify backend is running on port 8000.
-   Verify Angular runs on port 4200.
-   Verify CORS configuration.

**Gemini API errors**

-   Check `.env`.
-   Ensure the API key is valid.

------------------------------------------------------------------------

# 👩‍💻 Author

**Mahi Upadhyay**

Enterprise RAG Chatbot Prototype

Tech Mahindra Internship

------------------------------------------------------------------------

# 📄 License

Educational and internship prototype.
