import redis

from app.config import settings

_redis_client = redis.from_url(settings.redis_url, decode_responses=True)

RATE_LIMIT_MAX_REQUESTS = 10
RATE_LIMIT_WINDOW_SECONDS = 60


def is_rate_limited(client_ip: str) -> bool:
    """
    Simple fixed-window rate limiter: allows RATE_LIMIT_MAX_REQUESTS
    per client_ip per RATE_LIMIT_WINDOW_SECONDS. Uses Redis INCR with
    an expiry, which is an atomic, cheap way to implement this without
    a separate counting data structure.
    """
    key = f"ratelimit:{client_ip}"

    current_count = _redis_client.incr(key)

    if current_count == 1:
        # First request in this window - set the expiry now.
        _redis_client.expire(key, RATE_LIMIT_WINDOW_SECONDS)

    return current_count > RATE_LIMIT_MAX_REQUESTS
