import time
from contextlib import AbstractContextManager, contextmanager
from typing import Callable, Optional

from cacheout import Cache


class CacheMemory:
    def __init__(self) -> None:
        self._cache = Cache(maxsize=256, ttl=60, timer=time.time, default=None)

    def get(self, key: str) -> Optional[object]:
        return self._cache.get(key)

    def set(self, key: str, value: object) -> None:
        self._cache.set(key, value)
