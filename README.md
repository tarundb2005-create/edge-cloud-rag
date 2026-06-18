# edge-cloud-rag
# Edge-to-Cloud Distributed RAG Infrastructure

## Overview

A distributed Retrieval-Augmented Generation (RAG) system
that routes AI workloads between local inference and cloud-based
semantic retrieval.

## Features

- FastAPI Backend
- ChromaDB Vector Store
- PDF Ingestion Pipeline
- Semantic Retrieval
- Ollama + Qwen3 Local LLM
- REST API
- Persistent Knowledge Base

## Architecture

User
 ↓
FastAPI
 ↓
Retriever
 ↓
ChromaDB
 ↓
Qwen3
 ↓
Answer

## Tech Stack

Python
FastAPI
ChromaDB
Ollama
Qwen3
PyPDF

## Future Roadmap

- WebSocket Streaming
- Flutter Frontend
- Edge Routing
- Semantic Cache
- LangChain Agents