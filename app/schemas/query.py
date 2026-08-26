from pydantic import BaseModel


class QueryRequest(BaseModel):
    question: str
    ticker: str | None = None
    stock_ticker: str | None = None
    top_k: int = 3


class SourceChunk(BaseModel):
    chunk_index: int
    content: str
    document_id: int


class StockQuote(BaseModel):
    ticker: str
    price: str | None = None
    change: str | None = None
    change_percent: str | None = None
    volume: str | None = None
    latest_trading_day: str | None = None


class QueryResponse(BaseModel):
    answer: str
    sources: list[SourceChunk]
    stock_data: StockQuote | None = None
