
from pathlib import Path
import chromadb
from pypdf import PdfReader

BASE_DIR = Path(__file__).resolve().parent.parent

client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_db")
)

collection = client.get_or_create_collection(
    name="knowledge_base"
)

def ingest_pdf(pdf_path):

    reader = PdfReader(str(pdf_path))

    all_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            all_text += text + "\n"

    chunk_size = 500

    chunks = []

    for i in range(
        0,
        len(all_text),
        chunk_size
    ):
        chunks.append(
            all_text[i:i + chunk_size]
        )

    for idx, chunk in enumerate(chunks):

        collection.add(
            documents=[chunk],
            ids=[
                f"{Path(pdf_path).stem}_chunk_{idx}"
            ]
        )

    return len(chunks)