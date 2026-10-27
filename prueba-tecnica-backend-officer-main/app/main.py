from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repositories.auth_repository import init_users_table
from app.repositories.polizas_repository import ensure_lookup_indexes
from app.routes import auth_router, dashboard_router, dimension_router, polizas_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_users_table()
    ensure_lookup_indexes()
    yield

app = FastAPI(
    title="Prueba Técnica improgress",
    lifespan=lifespan,
)

origins = ["*"]
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

app.include_router(auth_router, prefix="/auth", tags=["auth"])
app.include_router(dimension_router, prefix="/dimensions", tags=["dimensions"])
app.include_router(polizas_router, prefix="/polizas", tags=["polizas"])
app.include_router(dashboard_router, prefix="/dashboard", tags=["dashboard"])


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
