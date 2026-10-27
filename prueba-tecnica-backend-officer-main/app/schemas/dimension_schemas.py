from pydantic import BaseModel


class Dimension(BaseModel):
    id: int
    name: str


class DimensionPage(BaseModel):
    items: list[Dimension]
    total: int
    page: int
    page_size: int
