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

    return {
        "documents": results["documents"][0],
        "ids": results["ids"][0]
    }


if __name__ == "__main__":

    query = input("Ask: ")

    results = retrieve(query)

    print("\nRetrieved Context:\n")

    for i, doc in enumerate(results["documents"]):
        print(f"\nChunk {i+1}")
        print("-" * 50)
        print(doc)

    print("\nSources:\n")

    for source_id in results["ids"]:
        print(source_id)