from datetime import date

from pydantic import BaseModel, Field, FiniteFloat, PositiveInt


class Poliza(BaseModel):
    id: int
    correlativo: int
    fecha_declaracion: date | None
    tipo_cambio_dolar: float | None
    aduana_id: int | None
    tipo_regimen_id: int | None


class PolizaItem(BaseModel):
    id: int
    poliza_id: int | None
    sac_id: int | None
    pais_id: int | None
    tipo_unidad_medida_id: int | None
    cantidad_fraccion: float | None
    tasa_dai: float | None
    valor_dai: float | None
    valor_cif_uds: float | None
    tasa_cif_cantidad_fraccion: float | None


class PolizaPage(BaseModel):
    items: list[Poliza]
    total: int
    page: int
    page_size: int


class PolizaDetail(Poliza):
    items: list[PolizaItem]
    items_total: int
    page: int
    page_size: int


class PolizaItemCreate(BaseModel):
    sac_id: PositiveInt
    pais_id: PositiveInt
    tipo_unidad_medida_id: PositiveInt
    cantidad_fraccion: FiniteFloat | None = None
    tasa_dai: FiniteFloat | None = None
    valor_dai: FiniteFloat | None = None
    valor_cif_uds: FiniteFloat | None = None
    tasa_cif_cantidad_fraccion: FiniteFloat | None = None


class PolizaCreate(BaseModel):
    correlativo: PositiveInt
    fecha_declaracion: date
    tipo_cambio_dolar: FiniteFloat = Field(gt=0)
    aduana_id: PositiveInt
    tipo_regimen_id: PositiveInt
    items: list[PolizaItemCreate] = Field(min_length=1, max_length=1000)


class PolizaCreated(BaseModel):
    id: int
    correlativo: int
    items_created: int
