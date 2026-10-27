from datetime import date
from typing import Annotated

from fastapi import APIRouter, Depends, Path, Query, Response, status

from app.controllers.auth_controller import get_current_user
from app.controllers.polizas_controller import create_poliza, get_poliza, list_polizas
from app.schemas.poliza_schemas import PolizaCreate, PolizaCreated, PolizaDetail, PolizaPage

router = APIRouter(dependencies=[Depends(get_current_user)])

Page = Annotated[int, Query(ge=1)]
PageSize = Annotated[int, Query(ge=1, le=100)]
PositiveId = Annotated[int, Query(ge=1)]


@router.post("", response_model=PolizaCreated, status_code=status.HTTP_201_CREATED)
def create(payload: PolizaCreate, response: Response):
    created = create_poliza(payload.model_dump(mode="json"))
    response.headers["Location"] = f"/polizas/{created['id']}"
    return created


@router.get("", response_model=PolizaPage)
def polizas(
    page: Page = 1, page_size: PageSize = 20,
    correlativo: Annotated[int | None, Query(ge=1)] = None,
    fecha_desde: date | None = None, fecha_hasta: date | None = None,
    aduana_id: PositiveId | None = None,
    tipo_regimen_id: PositiveId | None = None,
):
    return list_polizas(
        page=page, page_size=page_size, correlativo=correlativo,
        fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
        aduana_id=aduana_id, tipo_regimen_id=tipo_regimen_id,
    )


@router.get("/{poliza_id}", response_model=PolizaDetail)
def poliza_by_id(
    poliza_id: Annotated[int, Path(ge=1)],
    page: Page = 1, page_size: PageSize = 50,
    pais_id: PositiveId | None = None, sac_id: PositiveId | None = None,
):
    return get_poliza(
        poliza_id, page=page, page_size=page_size,
        pais_id=pais_id, sac_id=sac_id,
    )
