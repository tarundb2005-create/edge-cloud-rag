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

DATA_DIR = BASE_DIR / "data"

pdf_files = list(DATA_DIR.glob("*.pdf"))

chunk_size = 500

collection.delete(
    ids=collection.get()["ids"]
)

for pdf_file in pdf_files:

    print(f"\nProcessing: {pdf_file.name}")

    reader = PdfReader(str(pdf_file))

    all_text = ""

    for page in reader.pages:
        text = page.extract_text()

        if text:
            all_text += text + "\n"

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
                f"{pdf_file.stem}_chunk_{idx}"
            ]
        )

    print(
        f"Stored {len(chunks)} chunks from {pdf_file.name}"
    )

print("\nAll PDFs ingested successfully!")