import chromadb

_client = chromadb.PersistentClient(path="/app/chroma_data")
_collection = _client.get_or_create_collection(name="documents")


def add_chunks(document_id: int, chunks: list[str], embeddings: list[list[float]], ticker: str | None):
    ids = [f"doc{document_id}_chunk{i}" for i in range(len(chunks))]
    metadatas = [{"document_id": document_id, "ticker": ticker or ""} for _ in chunks]

    _collection.add(
        ids=ids,
        documents=chunks,
        embeddings=embeddings,
        metadatas=metadatas,
    )


def query_chunks(query_embedding: list[float], top_k: int = 3):
    return _collection.query(
        query_embeddings=[query_embedding],
        n_results=top_k,
    )
