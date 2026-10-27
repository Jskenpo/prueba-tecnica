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
