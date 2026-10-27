from app.database.engine import get_connection

TABLES = {"pais", "aduanas", "tipo_regimen"}


def list_dimensions(table: str, search: str | None, limit: int, offset: int):
    if table not in TABLES:
        raise ValueError("Unsupported dimension")

    where = ""
    params: tuple[str, ...] = ()
    if search:
        escaped = search.replace("\\", "\\\\").replace("%", "\\%").replace("_", "\\_")
        where = " WHERE name LIKE ? ESCAPE '\\'"
        params = (f"%{escaped}%",)

    with get_connection() as connection:
        total = connection.execute(
            f"SELECT COUNT(*) FROM {table}{where}", params
        ).fetchone()[0]
        rows = connection.execute(
            f"SELECT id, name FROM {table}{where} ORDER BY name COLLATE NOCASE, id LIMIT ? OFFSET ?",
            (*params, limit, offset),
        ).fetchall()

    return total, [dict(row) for row in rows]
