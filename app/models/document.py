from sqlalchemy import Column, Integer, String, DateTime
from datetime import datetime, timezone

from app.database import Base


class Document(Base):
    __tablename__ = "documents"

    id = Column(Integer, primary_key=True, index=True)
    filename = Column(String, nullable=False)
    ticker = Column(String, nullable=True, index=True)
    chunk_count = Column(Integer, default=0)
    uploaded_at = Column(DateTime, default=lambda: datetime.now(timezone.utc))
