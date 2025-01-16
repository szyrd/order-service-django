from django.apps import AppConfig
from django.core.cache import cache
from django.core.cache.backends.base import InvalidCacheBackendError

class OrdersConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'orders'

    # def ready(self):
    #     try:
    #         cache.set('startup_check', 'OK', timeout=60)
    #         print("Redis is available.")
    #     except InvalidCacheBackendError:
    #         print("Redis is unavailable.")

