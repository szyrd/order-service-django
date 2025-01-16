from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError

def set_cache(key, value, timeout=60):
    try:
        cache.set(key, value, timeout)
    except InvalidCacheBackendError:
        print("Redis is unavailable. Skipping cache.")
