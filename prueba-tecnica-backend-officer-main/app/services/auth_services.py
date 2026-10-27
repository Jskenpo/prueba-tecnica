import os
import sqlite3
from datetime import datetime, timedelta, timezone

from jose import JWTError, jwt
from pwdlib import PasswordHash

from app.repositories.auth_repository import (
    create_user,
    find_user_by_id,
    find_user_by_username,
)

ALGORITHM = "HS256"
TOKEN_LIFETIME_MINUTES = 30
password_hash = PasswordHash.recommended()


class UsernameTaken(Exception):
    pass


class InvalidCredentials(Exception):
    pass


def register_user(username: str, password: str):
    hashed = password_hash.hash(password)
    try:
        return create_user(username, hashed)
    except sqlite3.IntegrityError as exc:
        raise UsernameTaken from exc


def authenticate_user(username: str, password: str):
    user = find_user_by_username(username)
    if user is None or not password_hash.verify(password, user["password_hash"]):
        raise InvalidCredentials
    return user


def create_access_token(user_id: int):
    secret = os.environ["JWT_SECRET_KEY"]
    expires = datetime.now(timezone.utc) + timedelta(minutes=TOKEN_LIFETIME_MINUTES)
    return jwt.encode({"sub": str(user_id), "exp": expires}, secret, algorithm=ALGORITHM)


def login_user(username: str, password: str):
    user = authenticate_user(username, password)
    return create_access_token(user["id"])


def user_from_token(token: str):
    try:
        claims = jwt.decode(token, os.environ["JWT_SECRET_KEY"], algorithms=[ALGORITHM])
        user_id = int(claims["sub"])
    except (JWTError, KeyError, ValueError) as exc:
        raise InvalidCredentials from exc
    user = find_user_by_id(user_id)
    if user is None:
        raise InvalidCredentials
    return user
