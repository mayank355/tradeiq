from pydantic import BaseModel
from datetime import datetime


class DocumentResponse(BaseModel):
    id: int
    filename: str
    ticker: str | None
    chunk_count: int
    uploaded_at: datetime

    class Config:
        from_attributes = True


class DocumentUploadResult(BaseModel):
    document: DocumentResponse
    message: str
