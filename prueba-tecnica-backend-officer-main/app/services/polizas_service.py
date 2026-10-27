from datetime import date

from app.repositories.polizas_repository import (
    get_poliza,
    list_poliza_items,
    list_polizas,
)


class PolizaNotFound(Exception):
    pass


class InvalidDateRange(Exception):
    pass


def get_polizas(
    *, page: int, page_size: int, correlativo: int | None,
    fecha_desde: date | None, fecha_hasta: date | None,
    aduana_id: int | None, tipo_regimen_id: int | None,
):
    if fecha_desde and fecha_hasta and fecha_desde > fecha_hasta:
        raise InvalidDateRange
    total, items = list_polizas(
        correlativo=correlativo, fecha_desde=fecha_desde, fecha_hasta=fecha_hasta,
        aduana_id=aduana_id, tipo_regimen_id=tipo_regimen_id,
        limit=page_size, offset=(page - 1) * page_size,
    )
    return {"items": items, "total": total, "page": page, "page_size": page_size}


def get_poliza_detail(
    poliza_id: int, *, page: int, page_size: int,
    pais_id: int | None, sac_id: int | None,
):
    poliza = get_poliza(poliza_id)
    if poliza is None:
        raise PolizaNotFound
    total, items = list_poliza_items(
        poliza_id, pais_id=pais_id, sac_id=sac_id,
        limit=page_size, offset=(page - 1) * page_size,
    )
    return {**poliza, "items": items, "items_total": total,
            "page": page, "page_size": page_size}
