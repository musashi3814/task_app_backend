from collections.abc import Generator
from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import ExpiredSignatureError, InvalidAudienceError, InvalidTokenError
from pydantic import ValidationError
from sqlmodel import Session

from app.core import security
from app.core.config import settings
from app.crud.user_crud import crud_user
from app.db.db import engine
from app.models.users_model import Users
from app.schemas.token import AccessTokenPayload, RefreshTokenPayload

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token/")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[str, Depends(reusable_oauth2)]


def decode_token(token: str) -> AccessTokenPayload:
    print(token)
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return AccessTokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンの有効期限が切れています",
        )
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="トークンの検証に失敗しました",
        )
    except ValidationError:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="デコードに失敗しました",
        )


def decode_refresh_token(token: str) -> RefreshTokenPayload:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[security.ALGORITHM]
        )
        return RefreshTokenPayload(**payload)
    except ExpiredSignatureError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="トークンの有効期限が切れています",
        )
    except (InvalidTokenError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="デコードに失敗しました",
        )


def get_current_user(session: SessionDep, token: TokenDep) -> AccessTokenPayload:
    token_data = decode_token(token)
    user = crud_user.get(db=session, id=token_data.sub)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    if not user.is_active:
        raise HTTPException(status_code=401, detail="ログイン権限がありません")
    return user


CurrentUser = Annotated[Users, Depends(get_current_user)]


def get_current_active_admin(current_user: CurrentUser) -> Users:
    if not current_user.is_admin:
        raise HTTPException(status_code=403, detail="権限がありません")
    return current_user


CurrentAdminUser = Annotated[Users, Depends(get_current_active_admin)]
