from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.controllers.auth_controller import (
    authenticate_user,
    create_access_token,
    register_user,
    user_from_token,
)
from app.schemas.auth_schema import Registration, Token, User

router = APIRouter(tags=["auth"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: Registration):
    return register_user(payload.username, payload.password)


@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    user = authenticate_user(form.username, form.password)
    token = create_access_token(user["id"])
    response.headers["Authorization"] = f"Bearer {token}"
    return Token(access_token=token)


@router.get("/auth/me", response_model=User)
def me(token: Annotated[str, Depends(oauth2_scheme)]):
    return user_from_token(token)
