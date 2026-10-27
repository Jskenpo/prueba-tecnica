from contextlib import asynccontextmanager

from fastapi import FastAPI

from app.repositories.auth_repository import init_users_table
from app.routes.auth_routes import router as auth_router


@asynccontextmanager
async def lifespan(app: FastAPI):
    init_users_table()
    yield


app = FastAPI(title="Comercio Exterior API", lifespan=lifespan)
app.include_router(auth_router)
