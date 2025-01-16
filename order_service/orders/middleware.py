from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError

class CacheCheckMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        try:
            cache.set('health_check', 'OK', timeout=60)
        except InvalidCacheBackendError:
            print("Redis is unavailable. Skipping global cache checks.")
        response = self.get_response(request)
        return response
