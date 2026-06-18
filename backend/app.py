from fastapi import FastAPI
from pydantic import BaseModel

from rag.rag_pipeline import generate_answer

app = FastAPI(
    title="Edge Cloud Agentic RAG",
    version="1.0"
)


class QuestionRequest(BaseModel):
    question: str


@app.get("/")
def home():
    return {
        "status": "running"
    }


@app.post("/ask")
def ask_question(request: QuestionRequest):

    answer = generate_answer(request.question)

    return {
        "question": request.question,
        "answer": answer
    }