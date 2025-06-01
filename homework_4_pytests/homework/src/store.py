import logging

from src.utils import retry_decorator

class Store:
    def __init__(self, store, repository):
        self.local_cache = store
        self.repository = repository


    def get(self, key):
        return self.local_cache.get(key)

    @retry_decorator(timeout=5, retry_times=5)
    def cache_get(self, key):
        return self.repository.cache_get(key)

    @retry_decorator(timeout=5, retry_times=5)
    def cache_set(self, key, score, duration):
        return self.repository.cache_set(key, score, duration)
