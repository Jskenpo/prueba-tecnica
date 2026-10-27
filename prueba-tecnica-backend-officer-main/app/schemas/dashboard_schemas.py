from pydantic import BaseModel


class DashboardTotals(BaseModel):
    total_polizas: int
    total_items: int
    valor_cif_total_usd: float
    valor_dai_total: float


class TopCountry(BaseModel):
    id: int
    name: str
    valor_cif_total_usd: float


class TopSac(BaseModel):
    id: int
    fraccion: int
    descripcion: str | None
    valor_cif_total_usd: float


class DashboardTop5(BaseModel):
    paises: list[TopCountry]
    productos_sac: list[TopSac]
