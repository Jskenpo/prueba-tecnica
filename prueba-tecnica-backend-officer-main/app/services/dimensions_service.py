from app.repositories.dimensions_repository import list_dimensions


def get_dimensions(table: str, page: int, page_size: int, q: str | None):
    search = q.strip() if q else None
    total, items = list_dimensions(table, search, page_size, (page - 1) * page_size)
    return {"items": items, "total": total, "page": page, "page_size": page_size}
