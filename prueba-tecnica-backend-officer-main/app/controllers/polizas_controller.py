from datetime import date

from fastapi import HTTPException

from app.services import polizas_service


def list_polizas(
    *, page: int, page_size: int, correlativo: int | None,
    fecha_desde: date | None, fecha_hasta: date | None,
    aduana_id: int | None, tipo_regimen_id: int | None,
):
    try:
        return polizas_service.get_polizas(
            page=page, page_size=page_size, correlativo=correlativo,
            fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
            aduana_id=aduana_id, tipo_regimen_id=tipo_regimen_id,
        )
    except polizas_service.InvalidDateRange as exc:
        raise HTTPException(status_code=422, detail="fecha_desde must not exceed fecha_hasta") from exc


def get_poliza(
    poliza_id: int, *, page: int, page_size: int,
    pais_id: int | None, sac_id: int | None,
):
    try:
        return polizas_service.get_poliza_detail(
            poliza_id, page=page, page_size=page_size,
            pais_id=pais_id, sac_id=sac_id,
        )
    except polizas_service.PolizaNotFound as exc:
        raise HTTPException(status_code=404, detail="Poliza not found") from exc
