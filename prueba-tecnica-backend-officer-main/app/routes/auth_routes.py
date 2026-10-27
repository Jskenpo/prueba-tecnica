from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm

from app.controllers.auth_controller import (
    login_user,
    register_user,
    user_from_token,
)
from app.schemas.auth_schema import Registration, Token, User

router = APIRouter()
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: Registration):
    return register_user(payload.username, payload.password)


@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    token = login_user(form.username, form.password)
    response.headers["Authorization"] = f"Bearer {token}"
    return Token(access_token=token)


@router.get("/me", response_model=User)
def me(token: Annotated[str, Depends(oauth2_scheme)]):
    return user_from_token(token)
