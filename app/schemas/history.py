from pydantic import BaseModel
from datetime import datetime


class QueryHistoryResponse(BaseModel):
    id: int
    question: str
    answer: str
    ticker: str | None
    stock_ticker: str | None
    source_count: int
    latency_ms: float
    created_at: datetime

    class Config:
        from_attributes = True
