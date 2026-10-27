from .auth_routes import router as auth_router
from .dimension_routes import router as dimension_router
from .polizas_routes import router as polizas_router

__all__ = [
    "auth_router",
    "dimension_router",
    "polizas_router",
]
