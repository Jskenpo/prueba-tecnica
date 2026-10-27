from app.services.dashboard_service import get_top_5, get_totals, get_valor_por_mes


def totals():
    return get_totals()


def top_5():
    return get_top_5()


def valor_por_mes(year: int):
    return get_valor_por_mes(year)
