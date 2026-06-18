
from pydantic import BaseModel
from fastapi.middleware.cors import CORSMiddleware

import asyncio
from fastapi import FastAPI, WebSocket, WebSocketDisconnect

from rag.rag_pipeline import generate_answer

app = FastAPI(
    title="Edge Cloud Agentic RAG",
    version="1.0"
)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
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
from fastapi import WebSocket, WebSocketDisconnect

@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):

    await websocket.accept()

    try:
        while True:

            question = await websocket.receive_text()

            answer = generate_answer(question)

            await websocket.send_text(answer)

    except WebSocketDisconnect:
        print("Client disconnected")