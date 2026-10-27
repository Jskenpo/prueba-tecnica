from datetime import date

from app.database.engine import get_connection

POLIZA_COLUMNS = "id, correlativo, fecha_declaracion, tipo_cambio_dolar, aduana_id, tipo_regimen_id"
ITEM_COLUMNS = (
    "id, poliza_id, sac_id, pais_id, tipo_unidad_medida_id, "
    "cantidad_fraccion, tasa_dai, valor_dai, valor_cif_uds, tasa_cif_cantidad_fraccion"
)


def ensure_lookup_indexes():
    with get_connection() as connection:
        connection.execute("CREATE INDEX IF NOT EXISTS idx_polizas_fecha ON polizas(fecha_declaracion)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_polizas_aduana ON polizas(aduana_id)")
        connection.execute("CREATE INDEX IF NOT EXISTS idx_polizas_regimen ON polizas(tipo_regimen_id)")


def list_polizas(
    *, correlativo: int | None, fecha_desde: date | None, fecha_hasta: date | None,
    aduana_id: int | None, tipo_regimen_id: int | None, limit: int, offset: int,
):
    clauses = []
    params = []
    for column, value in (
        ("correlativo", correlativo), ("aduana_id", aduana_id),
        ("tipo_regimen_id", tipo_regimen_id),
    ):
        if value is not None:
            clauses.append(f"{column} = ?")
            params.append(value)
    if fecha_desde is not None:
        clauses.append("fecha_declaracion >= ?")
        params.append(fecha_desde.isoformat())
    if fecha_hasta is not None:
        clauses.append("fecha_declaracion <= ?")
        params.append(fecha_hasta.isoformat())
    where = " WHERE " + " AND ".join(clauses) if clauses else ""

    with get_connection() as connection:
        total = connection.execute("SELECT COUNT(*) FROM polizas" + where, params).fetchone()[0]
        rows = connection.execute(
            f"SELECT {POLIZA_COLUMNS} FROM polizas{where} ORDER BY id DESC LIMIT ? OFFSET ?",
            (*params, limit, offset),
        ).fetchall()
    return total, [dict(row) for row in rows]


def get_poliza(poliza_id: int):
    with get_connection() as connection:
        row = connection.execute(
            f"SELECT {POLIZA_COLUMNS} FROM polizas WHERE id = ?", (poliza_id,)
        ).fetchone()
    return dict(row) if row else None


def list_poliza_items(
    poliza_id: int, *, pais_id: int | None, sac_id: int | None,
    limit: int, offset: int,
):
    clauses = ["poliza_id = ?"]
    params = [poliza_id]
    if pais_id is not None:
        clauses.append("pais_id = ?")
        params.append(pais_id)
    if sac_id is not None:
        clauses.append("sac_id = ?")
        params.append(sac_id)
    where = " WHERE " + " AND ".join(clauses)
    source = "poliza_items INDEXED BY idx_poliza_items_poliza_id"

    with get_connection() as connection:
        total = connection.execute(
            "SELECT COUNT(*) FROM " + source + where, params
        ).fetchone()[0]
        rows = connection.execute(
            f"SELECT {ITEM_COLUMNS} FROM {source}{where} ORDER BY id LIMIT ? OFFSET ?",
            (*params, limit, offset),
        ).fetchall()
    return total, [dict(row) for row in rows]


def create_poliza(data: dict):
    """Insert the header and every item in one SQLite transaction."""
    with get_connection() as connection:
        cursor = connection.execute(
            """INSERT INTO polizas
               (correlativo, fecha_declaracion, tipo_cambio_dolar, aduana_id, tipo_regimen_id)
               VALUES (?, ?, ?, ?, ?)""",
            (
                data["correlativo"], data["fecha_declaracion"],
                data["tipo_cambio_dolar"], data["aduana_id"],
                data["tipo_regimen_id"],
            ),
        )
        poliza_id = cursor.lastrowid
        connection.executemany(
            """INSERT INTO poliza_items
               (poliza_id, sac_id, pais_id, tipo_unidad_medida_id,
                cantidad_fraccion, tasa_dai, valor_dai, valor_cif_uds,
                tasa_cif_cantidad_fraccion)
               VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)""",
            [
                (
                    poliza_id, item["sac_id"], item["pais_id"],
                    item["tipo_unidad_medida_id"], item["cantidad_fraccion"],
                    item["tasa_dai"], item["valor_dai"], item["valor_cif_uds"],
                    item["tasa_cif_cantidad_fraccion"],
                )
                for item in data["items"]
            ],
        )
    return poliza_id
