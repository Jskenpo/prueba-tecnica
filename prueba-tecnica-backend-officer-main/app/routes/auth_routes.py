from typing import Annotated

from fastapi import APIRouter, Depends, Response, status
from fastapi.security import OAuth2PasswordRequestForm

from app.controllers.auth_controller import (
    get_current_user,
    login_user,
    register_user,
)
from app.schemas.auth_schema import Registration, Token, User

router = APIRouter()


@router.post("/register", response_model=User, status_code=status.HTTP_201_CREATED)
def register(payload: Registration):
    return register_user(payload.username, payload.password)


@router.post("/login", response_model=Token)
def login(form: Annotated[OAuth2PasswordRequestForm, Depends()], response: Response):
    token = login_user(form.username, form.password)
    response.headers["Authorization"] = f"Bearer {token}"
    return Token(access_token=token)


@router.get("/me", response_model=User)
def me(user: Annotated[dict, Depends(get_current_user)]):
    return user
