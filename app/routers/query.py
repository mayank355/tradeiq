import time

from fastapi import APIRouter, HTTPException, Depends, Request
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.query_history import QueryHistory
from app.schemas.query import QueryRequest, QueryResponse, SourceChunk, StockQuote
from app.graph.pipeline import compiled_graph
from app.services.rate_limit import is_rate_limited

router = APIRouter(prefix="/query", tags=["query"])


@router.post("/", response_model=QueryResponse)
def ask_question(request: QueryRequest, http_request: Request, db: Session = Depends(get_db)):
    client_ip = http_request.client.host if http_request.client else "unknown"

    if is_rate_limited(client_ip):
        raise HTTPException(
            status_code=429,
            detail="Rate limit exceeded. Please wait before sending more requests.",
        )

    start_time = time.perf_counter()

    initial_state = {
        "question": request.question,
        "ticker": request.ticker,
        "stock_ticker": request.stock_ticker,
        "top_k": request.top_k,
    }

    final_state = compiled_graph.invoke(initial_state)

    chunks = final_state.get("chunks", [])
    metadatas = final_state.get("chunk_metadatas", [])

    if not chunks:
        detail = (
            f"No documents found for ticker '{request.ticker}'."
            if request.ticker
            else "No documents found. Upload a document before querying."
        )
        raise HTTPException(status_code=404, detail=detail)

    sources = [
        SourceChunk(
            chunk_index=i,
            content=doc,
            document_id=meta.get("document_id", -1),
        )
        for i, (doc, meta) in enumerate(zip(chunks, metadatas))
    ]

    stock_data = final_state.get("stock_data")
    answer = final_state["answer"]

    latency_ms = (time.perf_counter() - start_time) * 1000

    history_entry = QueryHistory(
        question=request.question,
        answer=answer,
        ticker=request.ticker,
        stock_ticker=request.stock_ticker,
        source_count=len(sources),
        latency_ms=latency_ms,
    )
    db.add(history_entry)
    db.commit()

    return QueryResponse(
        answer=answer,
        sources=sources,
        stock_data=StockQuote(**stock_data) if stock_data else None,
    )
