from app.services.dashboard_service import get_top_5, get_totals


def totals():
    return get_totals()


def top_5():
    return get_top_5()
