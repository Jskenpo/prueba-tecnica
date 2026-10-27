from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.controllers.auth_controller import get_current_user
from app.controllers.dashboard_controller import top_5, totals, valor_por_mes
from app.schemas.dashboard_schemas import DashboardMonthly, DashboardTop5, DashboardTotals

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/kpis/totals", response_model=DashboardTotals)
def dashboard_totals():
    return totals()


@router.get("/kpis/top-5", response_model=DashboardTop5)
def dashboard_top_5():
    return top_5()


@router.get("/kpis/valor-por-mes", response_model=DashboardMonthly)
def dashboard_valor_por_mes(year: Annotated[int, Query(ge=1, le=9998)]):
    return valor_por_mes(year)
