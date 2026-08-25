from sqlalchemy import Column, Integer, String, Float, DateTime, Text
from datetime import datetime, timezone

from app.database import Base


class QueryHistory(Base):
    __tablename__ = "query_history"

    id = Column(Integer, primary_key=True, index=True)
    question = Column(Text, nullable=False)
    answer = Column(Text, nullable=False)
    ticker = Column(String, nullable=True, index=True)          # document filter used
    stock_ticker = Column(String, nullable=True, index=True)    # live quote ticker used
    source_count = Column(Integer, default=0)
    latency_ms = Column(Float, nullable=False)
    created_at = Column(DateTime, default=lambda: datetime.now(timezone.utc), index=True)
