import os

from dotenv import load_dotenv

from app.loaders.jira_loader import JiraLoader
from app.vectorstore.chroma import get_chroma_client

load_dotenv()

def main():
    JIRA_USERNAME = os.getenv("JIRA_USERNAME")
    JIRA_API_TOKEN = os.getenv("JIRA_API_TOKEN")
    JIRA_SERVER = os.getenv("JIRA_SERVER")

    print("[+] Loading JIRA tickets...")
    docs = JiraLoader(token=JIRA_API_TOKEN,base_url=JIRA_SERVER,email=JIRA_USERNAME).load()
    print(f"[+] Loaded {len(docs)} JIRA tickets.")

    print("[+] Connecting to ChromaDB...")
    collection = get_chroma_client()

    print("[+] Inserting documents into ChromaDB...")
    collection.write_documents(docs)

    print("[✓] Done. JIRA data indexed.")

if __name__ == "__main__":
    main()