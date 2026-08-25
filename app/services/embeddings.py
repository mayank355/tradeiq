from sentence_transformers import SentenceTransformer

# all-MiniLM-L6-v2: small, fast, CPU-friendly - sufficient for
# semantic similarity search at this project's scale.
_model = SentenceTransformer("all-MiniLM-L6-v2")


def embed_texts(texts: list[str]) -> list[list[float]]:
    """Convert a list of text chunks into embedding vectors."""
    embeddings = _model.encode(texts, convert_to_numpy=True)
    return embeddings.tolist()
