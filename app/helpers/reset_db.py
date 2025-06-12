from chromadb import PersistentClient

client = PersistentClient(path="chroma/")

collection = client.get_collection("documents")
all_docs = collection.get()
all_ids = all_docs['ids']

if all_ids:
    collection.delete(ids=all_ids)

print(f"All documents from '{collection.name}' have been deleted")