import redis
from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from sqlalchemy import text

from app.config import settings
from app.database import engine, Base
from app.routers import documents, query, history
from app.models import document, query_history  # noqa: F401 - registers models before create_all

app = FastAPI(title=settings.app_name)

Base.metadata.create_all(bind=engine)

app.include_router(documents.router)
app.include_router(query.router)
app.include_router(history.router)


@app.exception_handler(Exception)
async def unhandled_exception_handler(request: Request, exc: Exception):
    """
    Catches anything not already handled by FastAPI's own HTTPException
    flow (e.g. a raw exception from Groq, ChromaDB, or Alpha Vantage)
    and returns a consistent, clean JSON error shape instead of the
    default bare 'Internal Server Error' text. Full details still go
    to the server logs (via FastAPI's default logging), just not to
    the client - avoids leaking stack trace internals to API consumers.
    """
    return JSONResponse(
        status_code=500,
        content={
            "error": "internal_server_error",
            "detail": "Something went wrong processing this request. Please try again.",
        },
    )


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
