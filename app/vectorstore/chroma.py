def get_chroma_client():
    try:
        from haystack_integrations.document_stores.chroma import ChromaDocumentStore
    except ImportError:
        raise ImportError("Please install haystack-ai[chromadb] for Chroma integration")

    document_store = ChromaDocumentStore(persist_path="chroma/")
    return document_store
