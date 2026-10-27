from fastapi import APIRouter, Depends

from app.controllers.auth_controller import get_current_user
from app.controllers.dashboard_controller import top_5, totals
from app.schemas.dashboard_schemas import DashboardTop5, DashboardTotals

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/kpis/totals", response_model=DashboardTotals)
def dashboard_totals():
    return totals()


@router.get("/kpis/top-5", response_model=DashboardTop5)
def dashboard_top_5():
    return top_5()
