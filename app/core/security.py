from datetime import datetime, timedelta, timezone
from typing import Any

import jwt
from fastapi import HTTPException
from passlib.context import CryptContext

from app.core.config import settings
from app.models.users_model import Users

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

ALGORITHM = "HS256"


def create_token(subject: int, role: str, expires_delta: timedelta) -> str:
    expire = datetime.now(timezone.utc) + expires_delta
    to_encode = {
        "sub": subject,
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "role": role,
    }
    encoded_jwt: str = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_access_token(subject: int, role: str) -> str:
    return create_token(
        subject, role, timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )


def create_id_token(user: Users, role: str) -> str:
    expire = datetime.now(timezone.utc) + timedelta(
        minutes=settings.ID_TOKEN_EXPIRE_MINUTES
    )
    claims = {
        "sub": user.id,
        "user_id": str(user.id),
        "exp": expire,
        "iat": datetime.now(timezone.utc),
        "name": user.name,
        "email": user.email,
        "role": role,
    }
    encoded_jwt: str = jwt.encode(claims, settings.SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


def create_refresh_token(subject: str | Any, role: str) -> str:
    return create_token(
        subject, role, timedelta(days=settings.REFRESH_TOKEN_EXPIRE_DAYS)
    )


def verify_password(plain_password: str, hashed_password: str) -> bool:
    response: bool = pwd_context.verify(plain_password, hashed_password)
    return response


def get_password_hash(password: str) -> str:
    response: str = pwd_context.hash(password)
    return response
