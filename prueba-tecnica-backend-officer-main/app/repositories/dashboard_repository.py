from app.database.engine import get_connection


def fetch_totals():
    with get_connection() as connection:
        row = connection.execute("""
            SELECT
                (SELECT COUNT(*) FROM polizas) AS total_polizas,
                COUNT(*) AS total_items,
                ROUND(COALESCE(SUM(valor_cif_uds), 0), 2) AS valor_cif_total_usd,
                ROUND(COALESCE(SUM(valor_dai), 0), 2) AS valor_dai_total
            FROM poliza_items
        """).fetchone()
    return dict(row)


def fetch_top_5():
    with get_connection() as connection:
        countries = connection.execute("""
            WITH ranked AS (
                SELECT pais_id AS id, SUM(valor_cif_uds) AS total_value
                FROM poliza_items
                WHERE pais_id IS NOT NULL AND valor_cif_uds IS NOT NULL
                GROUP BY pais_id
                ORDER BY total_value DESC, pais_id
                LIMIT 5
            )
            SELECT p.id, p.name, ROUND(r.total_value, 2) AS valor_cif_total_usd
            FROM ranked AS r
            JOIN pais AS p ON p.id = r.id
            ORDER BY r.total_value DESC, p.id
        """).fetchall()
        products = connection.execute("""
            WITH ranked AS (
                SELECT sac_id AS id, SUM(valor_cif_uds) AS total_value
                FROM poliza_items
                WHERE sac_id IS NOT NULL AND valor_cif_uds IS NOT NULL
                GROUP BY sac_id
                ORDER BY total_value DESC, sac_id
                LIMIT 5
            )
            SELECT s.id, s.fraccion, s.descripcion,
                   ROUND(r.total_value, 2) AS valor_cif_total_usd
            FROM ranked AS r
            JOIN sac AS s ON s.id = r.id
            ORDER BY r.total_value DESC, s.id
        """).fetchall()
    return {
        "paises": [dict(row) for row in countries],
        "productos_sac": [dict(row) for row in products],
    }
