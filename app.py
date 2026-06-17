
from fastapi import FastAPI

app = FastAPI(
    title="Edge Cloud Agentic RAG",
    version="1.0"
)

@app.get("/")
def home():
    return {
        "status": "running",
        "project": "Edge-to-Cloud Agentic RAG"
    }

@app.get("/health")
def health():
    return {
        "server": "healthy"
    }