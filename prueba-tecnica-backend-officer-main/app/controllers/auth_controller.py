from fastapi import HTTPException, status

from app.services import auth_services


def register_user(username: str, password: str):
    try:
        return auth_services.register_user(username, password)
    except auth_services.UsernameTaken as exc:
        raise HTTPException(status_code=409, detail="Username already exists") from exc


def login_user(username: str, password: str):
    try:
        return auth_services.login_user(username, password)
    except auth_services.InvalidCredentials as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid username or password",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc


def user_from_token(token: str):
    try:
        return auth_services.user_from_token(token)
    except auth_services.InvalidCredentials as exc:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid or expired token",
            headers={"WWW-Authenticate": "Bearer"},
        ) from exc
