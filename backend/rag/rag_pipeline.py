import chromadb
import ollama
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


def generate_answer(query):

    print("1. Retrieving context...")

    retrieval_results = retrieve(query)

    context = "\n".join(
        retrieval_results["documents"]
    )

    print("2. Context retrieved:")
    print(context)

    prompt = f"""
Context:
{context}

Question:
{query}

Answer only using the provided context.
"""

    print("3. Calling Ollama...")

    response = ollama.chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("4. Ollama responded")

    return {
        "answer": response["message"]["content"],
        "sources": retrieval_results["ids"]
    }


if __name__ == "__main__":

    query = input("Ask: ")

    result = generate_answer(query)

    print("\nAnswer:\n")
    print(result["answer"])

    print("\nSources:\n")
    print(result["sources"])