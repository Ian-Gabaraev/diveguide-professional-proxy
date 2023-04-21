import shelve
import settings


def is_api_healthy():
    with shelve.open('cache') as db:
        return db.get(settings.HEALTHY_CACHE_KEY, 0) == 1
