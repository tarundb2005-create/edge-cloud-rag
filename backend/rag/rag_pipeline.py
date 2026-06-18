
import chromadb
import ollama
from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent.parent

client = chromadb.PersistentClient(
    path=str(BASE_DIR / "chroma_db")
)

collection = client.get_collection("knowledge_base")


def retrieve(query):
    results = collection.query(
        query_texts=[query],
        n_results=2
    )
    return "\n".join(results["documents"][0])


def generate_answer(query):
    print("1. Retrieving context...")

    context = retrieve(query)

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

    return response["message"]["content"]
if __name__ == "__main__":
    query = input("Ask: ")

    answer = generate_answer(query)

    print("\nAnswer:\n")
    print(answer)