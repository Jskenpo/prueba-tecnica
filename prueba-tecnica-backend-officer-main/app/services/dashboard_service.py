from functools import lru_cache
from time import monotonic

from app.repositories.dashboard_repository import fetch_top_5, fetch_totals, fetch_valor_por_mes

CACHE_SECONDS = 60


@lru_cache(maxsize=2)
def _totals_for_period(period: int):
    return fetch_totals()


def get_totals():
    return _totals_for_period(int(monotonic() // CACHE_SECONDS))


def invalidate_totals_cache():
    _totals_for_period.cache_clear()


@lru_cache(maxsize=2)
def _top_5_for_period(period: int):
    return fetch_top_5()


def get_top_5():
    return _top_5_for_period(int(monotonic() // CACHE_SECONDS))


def invalidate_top_5_cache():
    _top_5_for_period.cache_clear()


@lru_cache(maxsize=64)
def _monthly_for_period(year: int, period: int):
    values = fetch_valor_por_mes(year)
    return {
        "year": year,
        "meses": [
            {"mes": month, "valor_cif_total_usd": values.get(month, 0.0)}
            for month in range(1, 13)
        ],
    }


def get_valor_por_mes(year: int):
    return _monthly_for_period(year, int(monotonic() // CACHE_SECONDS))


def invalidate_monthly_cache():
    _monthly_for_period.cache_clear()
