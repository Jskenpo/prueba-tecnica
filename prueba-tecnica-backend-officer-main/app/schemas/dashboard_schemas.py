from pydantic import BaseModel


class DashboardTotals(BaseModel):
    total_polizas: int
    total_items: int
    valor_cif_total_usd: float
    valor_dai_total: float
