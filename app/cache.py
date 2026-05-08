import threading
import time


class TTLCache:
    def __init__(self, ttl_seconds: int = 30):
        self.ttl_seconds = ttl_seconds
        self._store: dict[str, tuple[float, object]] = {}
        self._lock = threading.Lock()

    def get(self, key: str):
        with self._lock:
            entry = self._store.get(key)
            if entry is None:
                return None

            expires_at, value = entry
            if expires_at <= time.time():
                self._store.pop(key, None)
                return None
            return value

    def set(self, key: str, value: object):
        with self._lock:
            self._store[key] = (time.time() + self.ttl_seconds, value)

    def invalidate_prefix(self, prefix: str):
        with self._lock:
            keys_to_delete = [key for key in self._store if key.startswith(prefix)]
            for key in keys_to_delete:
                self._store.pop(key, None)

    def clear(self):
        with self._lock:
            self._store.clear()


cache = TTLCache()
