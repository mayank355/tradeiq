import redis
from fastapi import FastAPI
from sqlalchemy import text

from app.config import settings
from app.database import engine, Base
from app.routers import documents
from app.models import document  # noqa: F401

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.include_router(documents.router)


@app.get("/health")
def health_check():
    status = {"postgres": "disconnected", "redis": "disconnected"}

    try:
        with engine.connect() as conn:
            conn.execute(text("SELECT 1"))
        status["postgres"] = "connected"
    except Exception as e:
        status["postgres"] = f"error: {str(e)}"

    try:
        r = redis.from_url(settings.redis_url)
        r.ping()
        status["redis"] = "connected"
    except Exception as e:
        status["redis"] = f"error: {str(e)}"

    return status
