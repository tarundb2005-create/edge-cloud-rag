
import chromadb

client = chromadb.PersistentClient(path="./chroma_db")

print(client.list_collections())