import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_collection("knowledge_base")

results = collection.query(
    query_texts=["What is ChromaDB?"],
    n_results=2
)

print(results)