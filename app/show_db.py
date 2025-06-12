from chromadb import PersistentClient

client = PersistentClient(path="chroma/")
collection = client.get_collection("documents")

results = collection.get()
print(results)