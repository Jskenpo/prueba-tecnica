from typing import Annotated

from fastapi import APIRouter, Depends, Query

from app.controllers.auth_controller import get_current_user
from app.controllers.dimensions_controller import (
    list_aduanas,
    list_paises,
    list_tipos_regimen,
)
from app.schemas.dimension_schemas import DimensionPage

router = APIRouter(dependencies=[Depends(get_current_user)])

Page = Annotated[int, Query(ge=1)]
PageSize = Annotated[int, Query(ge=1, le=100)]
Search = Annotated[str | None, Query(max_length=100)]


@router.get("/paises", response_model=DimensionPage)
def paises(page: Page = 1, page_size: PageSize = 20, q: Search = None):
    return list_paises(page, page_size, q)


@router.get("/aduanas", response_model=DimensionPage)
def aduanas(page: Page = 1, page_size: PageSize = 20, q: Search = None):
    return list_aduanas(page, page_size, q)


@router.get("/tipos-regimen", response_model=DimensionPage)
def tipos_regimen(page: Page = 1, page_size: PageSize = 20, q: Search = None):
    return list_tipos_regimen(page, page_size, q)
