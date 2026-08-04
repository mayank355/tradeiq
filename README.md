# TradeIQ — AI-Powered Trading Intelligence Platform

TradeIQ lets users upload financial documents (earnings reports, SEC filings, analyst notes) and ask natural-language questions about them. Answers are grounded in the actual document content — with source citations — and will eventually be fused with live market data.

## Problem It Solves

LLMs hallucinate confidently when asked about content they haven't actually read. In finance, a hallucinated number can lead to a real bad decision. TradeIQ uses Retrieval-Augmented Generation (RAG) so every answer is grounded in a retrieved, citable chunk of the source document rather than the model's memory.

## Architecture

Upload PDF leads to text extraction, then chunking, then embedding, then storage in ChromaDB.
A user question is embedded the same way, top-k similar chunks are retrieved, a grounded answer is generated via Groq Llama 3, and the answer plus source citations are returned.

Planned but not yet built: live stock data fusion, LangGraph orchestration, Redis caching, PostgreSQL query history logging.

## Tech Stack

Backend: FastAPI
Relational DB: PostgreSQL for document metadata and query history
Cache: Redis, planned for stock price caching
ORM and Validation: SQLAlchemy and Pydantic
Vector DB: ChromaDB
Embeddings: HuggingFace sentence-transformers, model all-MiniLM-L6-v2
LLM: Groq API running Llama 3
Orchestration: LangGraph, planned
Live market data: not yet decided, options are Yahoo Finance, Alpha Vantage, or Finnhub
Infra: Docker and Docker Compose
Deployment target: Railway

## Current Status

Phase 0, Infrastructure setup with FastAPI, Postgres, and Redis via Docker Compose: Done
Phase 1, Document ingestion with PDF extraction, chunking, embeddings, and ChromaDB storage: Done
Phase 2, Retrieval and RAG question answering with Groq: In progress
Phase 3, Live market data fusion: Planned
Phase 4, LangGraph pipeline: Planned
Phase 5, Redis caching: Planned
Phase 6, Query history logging: Planned
Phase 7, Deployment and polish: Planned

## Running Locally

Requires Docker and Docker Compose installed.

Clone the repo, then create a .env file with your own GROQ_API_KEY based on .env.example.

Start all services with docker compose up --build

Check health at http://localhost:8001/health

View interactive API docs at http://localhost:8001/docs

## API Endpoints (current)

GET /health, verifies Postgres and Redis connectivity
POST /documents/, uploads a PDF for ingestion, extraction, chunking, embedding, and storage
GET /documents/, lists all uploaded documents

## Key Engineering Decisions

RAG over fine-tuning: documents update frequently with new filings each quarter, so RAG allows instant updates without retraining, and grounds every answer in a citable source.

Chunking with overlap: 800 character chunks with 150 character overlap balance retrieval precision against losing context at chunk boundaries.

Separate Postgres and ChromaDB: Postgres handles structured metadata and auditability, ChromaDB handles high dimensional similarity search, each database used for what it is actually good at.

Host port remapping to 5433, 6380, and 8001: allows this project to run alongside other Dockerized projects on the same machine without port conflicts, while internal container to container networking remains untouched.
