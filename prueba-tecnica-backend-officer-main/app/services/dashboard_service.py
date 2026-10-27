from functools import lru_cache
from time import monotonic

from app.repositories.dashboard_repository import fetch_totals

CACHE_SECONDS = 60


@lru_cache(maxsize=2)
def _totals_for_period(period: int):
    return fetch_totals()


def get_totals():
    return _totals_for_period(int(monotonic() // CACHE_SECONDS))


def invalidate_totals_cache():
    _totals_for_period.cache_clear()
