from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from app.database import get_db
from app.models.query_history import QueryHistory
from app.schemas.history import QueryHistoryResponse

router = APIRouter(prefix="/history", tags=["history"])


@router.get("/", response_model=list[QueryHistoryResponse])
def list_history(limit: int = 20, offset: int = 0, db: Session = Depends(get_db)):
    """
    Returns past queries, most recent first. This is the audit-trail
    retrieval endpoint - the record of what was asked and answered,
    and how the system behaved (latency, sources used) for each query.
    """
    return (
        db.query(QueryHistory)
        .order_by(QueryHistory.created_at.desc())
        .offset(offset)
        .limit(limit)
        .all()
    )
