CHROMA_PATH = "chroma_db"
COLLECTION_NAME = "customer_success_knowledge"
DEFAULT_TOP_K = 3


def get_chroma_collection(path=CHROMA_PATH, collection_name=COLLECTION_NAME):
    """Return a persistent Chroma collection for manual local testing."""
    import chromadb

    client = chromadb.PersistentClient(path=path)
    return client.get_or_create_collection(name=collection_name)


def format_chroma_results(results):
    """Normalize Chroma query results into context chunk dictionaries.

    Chroma query results often look like:
        {
            "ids": [["chunk-1"]],
            "documents": [["Text"]],
            "metadatas": [[{"source_id": "SRC-1"}]],
            "distances": [[0.12]]
        }
    """
    if not results:
        return []

    ids = results.get("ids") or [[]]
    documents = results.get("documents") or [[]]
    metadatas = results.get("metadatas") or [[]]
    distances = results.get("distances") or [[]]

    ids = ids[0] if ids else []
    documents = documents[0] if documents else []
    metadatas = metadatas[0] if metadatas else []
    distances = distances[0] if distances else []

    chunks = []

    for index, document in enumerate(documents):
        if not isinstance(document, str) or not document.strip():
            continue

        metadata = (
            metadatas[index]
            if index < len(metadatas) and isinstance(metadatas[index], dict)
            else {}
        )

        chunks.append({
            "id": ids[index] if index < len(ids) else None,
            "text": document.strip(),
            "source_id": metadata.get("source_id"),
            "title": metadata.get("title"),
            "category": metadata.get("category"),
            "section": metadata.get("section"),
            "distance": (
                distances[index]
                if index < len(distances)
                else None
            ),
        })

    return chunks


def retrieve_context(question, collection=None, top_k=DEFAULT_TOP_K):
    """Retrieve context chunks for a user question.

    Tests may pass a fake collection. Manual use should call Chroma.
    """
    question = question.strip() if isinstance(question, str) else ""

    if not question:
        return []

    if collection is None:
        collection = get_chroma_collection()

    results = collection.query(
        query_texts=[question],
        n_results=top_k,
        include=["documents", "metadatas", "distances"],
    )

    return format_chroma_results(results)
