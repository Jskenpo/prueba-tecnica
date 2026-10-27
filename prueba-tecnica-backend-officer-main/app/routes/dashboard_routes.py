from fastapi import APIRouter, Depends

from app.controllers.auth_controller import get_current_user
from app.controllers.dashboard_controller import totals
from app.schemas.dashboard_schemas import DashboardTotals

router = APIRouter(dependencies=[Depends(get_current_user)])


@router.get("/kpis/totals", response_model=DashboardTotals)
def dashboard_totals():
    return totals()
