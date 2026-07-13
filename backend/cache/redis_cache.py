from redis import Redis


def redis_client(url="redis://localhost:6379/2"):
    """Return a Redis client for low-level cache operations when needed."""
    return Redis.from_url(url, decode_responses=True)
