from contextlib import asynccontextmanager

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from app.repositories.auth_repository import init_users_table
from app.routes.auth_routes import router as auth_router
from app.routes.dimension_routes import router as dimension_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_users_table()
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


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(
        app,
        host="0.0.0.0",
        port=8000,
    )
