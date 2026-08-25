import json

import redis

from app.config import settings

_redis_client = redis.from_url(settings.redis_url, decode_responses=True)

STOCK_QUOTE_TTL_SECONDS = 60


def get_cached_quote(ticker: str) -> dict | None:
    """
    Return a cached stock quote for ticker if one exists and hasn't
    expired, otherwise None. A cache miss (None) tells the caller to
    go fetch fresh data from Alpha Vantage.
    """
    key = f"stock_quote:{ticker.upper()}"
    cached = _redis_client.get(key)

    if cached is None:
        print(f"[cache] MISS for {ticker}")
        return None

    print(f"[cache] HIT for {ticker}")
    return json.loads(cached)


def set_cached_quote(ticker: str, data: dict, ttl_seconds: int = STOCK_QUOTE_TTL_SECONDS) -> None:
    """
    Write-through: store a freshly fetched quote in the cache with a
    TTL, so the next request for the same ticker within that window
    is served from Redis instead of hitting Alpha Vantage again.
    """
    key = f"stock_quote:{ticker.upper()}"
    _redis_client.setex(key, ttl_seconds, json.dumps(data))
    print(f"[cache] SET {ticker} (expires in {ttl_seconds}s)")
