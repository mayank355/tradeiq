from app.graph.state import GraphState
from app.services.embeddings import embed_texts
from app.services.vectorstore import query_chunks
from app.services.stock_service import get_stock_quote
from app.services.cache import get_cached_quote, set_cached_quote
from app.llm.groq_client import generate_answer


def retrieve_node(state: GraphState) -> dict:
    """
    Embeds the question and retrieves the top_k most relevant chunks
    from ChromaDB, optionally filtered by ticker.
    """
    question_embedding = embed_texts([state["question"]])[0]

    results = query_chunks(
        question_embedding,
        top_k=state.get("top_k", 3),
        ticker=state.get("ticker"),
    )

    chunks = results.get("documents", [[]])[0]
    metadatas = results.get("metadatas", [[]])[0]

    return {"chunks": chunks, "chunk_metadatas": metadatas}


def fetch_stock_node(state: GraphState) -> dict:
    """
    Fetches a live stock quote for stock_ticker, checking the Redis
    cache first. Only reached when the conditional edge in pipeline.py
    determines stock_ticker is present.

    Cache-first pattern: a hit avoids the Alpha Vantage call entirely
    (instant, doesn't consume rate-limit budget). A miss falls through
    to the real API call, then write-through caches the result for
    the next request within the TTL window.
    """
    ticker = state["stock_ticker"]

    cached = get_cached_quote(ticker)
    if cached is not None:
        return {"stock_data": cached}

    stock_data = get_stock_quote(ticker)

    if stock_data is not None:
        set_cached_quote(ticker, stock_data)

    return {"stock_data": stock_data}


def generate_node(state: GraphState) -> dict:
    """
    Generates the final grounded answer using whatever chunks and
    stock_data are currently in state - stock_data may be None if
    fetch_stock_node was skipped entirely, or if the fetch failed.
    """
    answer = generate_answer(
        state["question"],
        state["chunks"],
        stock_data=state.get("stock_data"),
    )
    return {"answer": answer}
