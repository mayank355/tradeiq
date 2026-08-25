from typing import TypedDict


class GraphState(TypedDict, total=False):
    """
    Shared state passed between graph nodes. Each node reads what it
    needs and writes updates back into this dict - this is the
    "memory" that flows through the pipeline.
    """
    question: str
    ticker: str | None          # filters WHICH documents to search
    stock_ticker: str | None    # which ticker to fetch a LIVE price for
    top_k: int

    chunks: list[str]
    chunk_metadatas: list[dict]
    stock_data: dict | None
    answer: str
