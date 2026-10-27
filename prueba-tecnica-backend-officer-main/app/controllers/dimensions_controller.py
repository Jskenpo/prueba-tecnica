from app.services.dimensions_service import get_dimensions


def list_paises(page: int, page_size: int, q: str | None):
    return get_dimensions("pais", page, page_size, q)


def list_aduanas(page: int, page_size: int, q: str | None):
    return get_dimensions("aduanas", page, page_size, q)


def list_tipos_regimen(page: int, page_size: int, q: str | None):
    return get_dimensions("tipo_regimen", page, page_size, q)
