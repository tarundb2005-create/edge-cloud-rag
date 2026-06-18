
import chromadb
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_db")
)

collection = client.get_collection(
    "knowledge_base"
)


def retrieve(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )

    return results["documents"][0]


if __name__ == "__main__":
    query = input("Ask: ")

    docs = retrieve(query)

    print("\nRetrieved Context:\n")

    for doc in docs:
        print("-", doc)