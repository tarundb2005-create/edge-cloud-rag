from pydantic import BaseModel
from fastapi import FastAPI, WebSocket, WebSocketDisconnect
from fastapi.middleware.cors import CORSMiddleware
import asyncio
from fastapi import UploadFile, File
from rag.rag_pipeline import generate_answer
from pathlib import Path

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

    result = generate_answer(
        request.question
    )

    return {
        "question": request.question,
        "answer": result["answer"],
        "sources": result["sources"]
    }

@app.post("/upload")
async def upload_pdf(
    file: UploadFile = File(...)
):

    BASE_DIR = Path(__file__).resolve().parent

    DATA_DIR = BASE_DIR / "data"

    DATA_DIR.mkdir(
        exist_ok=True
    )

    file_path = DATA_DIR / file.filename

    with open(file_path, "wb") as buffer:
        buffer.write(
            await file.read()
        )

    return {
        "message":
            f"{file.filename} uploaded successfully"
    }

@app.websocket("/ws")
async def websocket_endpoint(
    websocket: WebSocket
):

    await websocket.accept()

    try:

        while True:

            question = await websocket.receive_text()

            result = generate_answer(
                question
            )

            answer = result["answer"]
            sources = result["sources"]

            for word in answer.split():

                await websocket.send_text(
                    word + " "
                )

                await asyncio.sleep(0.03)

            await websocket.send_text(
                "[SOURCES]"
            )

            for source in sources:

                await websocket.send_text(
                    source
                )

            await websocket.send_text(
                "[END]"
            )

    except WebSocketDisconnect:
        print("Client disconnected")