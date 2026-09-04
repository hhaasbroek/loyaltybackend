import json
from typing import List, Optional

import redis

from app.core.config import settings

_redis_client: Optional["redis.Redis"] = None


def get_redis_client() -> Optional["redis.Redis"]:
    """Lazily connect to Redis. Returns None (cache disabled) if unconfigured
    or unreachable, so callers can treat caching as a pure best-effort layer."""
    global _redis_client
    if _redis_client is not None:
        return _redis_client
    if not settings.REDIS_URL:
        return None
    try:
        client = redis.from_url(
            settings.REDIS_URL, decode_responses=True, socket_connect_timeout=2
        )
        client.ping()
    except Exception as e:
        print(f"Warning: Redis connection failed: {e}")
        return None
    _redis_client = client
    return _redis_client


def _cards_key(user_id: str) -> str:
    return f"cards:{user_id}"


def get_cached_cards(user_id: str) -> Optional[List[dict]]:
    client = get_redis_client()
    if client is None:
        return None
    try:
        raw = client.get(_cards_key(user_id))
    except Exception as e:
        print(f"Warning: Redis get failed: {e}")
        return None
    return json.loads(raw) if raw is not None else None


def set_cached_cards(user_id: str, cards: List[dict]) -> None:
    client = get_redis_client()
    if client is None:
        return
    try:
        client.setex(
            _cards_key(user_id), settings.CARD_CACHE_TTL_SECONDS, json.dumps(cards)
        )
    except Exception as e:
        print(f"Warning: Redis set failed: {e}")


def invalidate_cards(user_id: str) -> None:
    client = get_redis_client()
    if client is None:
        return
    try:
        client.delete(_cards_key(user_id))
    except Exception as e:
        print(f"Warning: Redis delete failed: {e}")
