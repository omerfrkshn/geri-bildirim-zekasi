import hashlib
import json
import logging
import os
from functools import lru_cache

import redis

logger = logging.getLogger(__name__)

REDIS_URL = os.environ.get("REDIS_URL", "redis://localhost:6379")
TTL_SANIYE = 7 * 24 * 60 * 60


@lru_cache(maxsize=1)
def istemciyi_al() -> redis.Redis:
    return redis.Redis.from_url(REDIS_URL, decode_responses=True)


def anahtar_uret(metin: str) -> str:
    parmak_izi = hashlib.sha256(metin.strip().encode("utf-8")).hexdigest()
    return f"duygu-analizi:{parmak_izi}"


def onbellekten_oku(metin: str) -> tuple[str, float] | None:
    try:
        ham = istemciyi_al().get(anahtar_uret(metin))
    except redis.RedisError as e:
        logger.warning("Redis'ten okunamadı: %s", e)
        return None
    if ham is None:
        return None
    veri = json.loads(ham)
    return veri["duygu"], veri["guven"]


def onbellege_yaz(metin: str, duygu: str, guven: float) -> None:
    try:
        istemciyi_al().setex(
            anahtar_uret(metin), TTL_SANIYE, json.dumps({"duygu": duygu, "guven": guven})
        )
    except redis.RedisError as e:
        logger.warning("Redis'e yazılamadı: %s", e)
