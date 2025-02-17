from datetime import timedelta
from typing import Annotated

from fastapi import APIRouter, HTTPException

from app.api.deps import RequestFormDep, SessionDep, decode_refresh_token
from app.core import security
from app.crud.user_crud import crud_user
from app.schemas.token import Token
from app.schemas.user import UserCreate, UserCreateMe

router = APIRouter()


@router.post("/", response_model=Token)
def login(session: SessionDep, form_data: RequestFormDep) -> Token:
    user = crud_user.authenticate(
        db=session, email=form_data.username, password=form_data.password
    )
    if not user:
        raise HTTPException(
            status_code=404, detail="メールアドレスまたはパスワードが正しくありません"
        )
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="ログイン権限がありません")

    role = "admin" if user.is_admin else "user"

    return Token(
        access_token=security.create_access_token(user.id, role=role),
        id_token=security.create_id_token(user, role=role),
        refresh_token=security.create_refresh_token(user.id, role=role),
    )


@router.post("/refresh", response_model=Token)
def refresh_access_token(refresh_token: str) -> Token:
    payload = decode_refresh_token(refresh_token)
    user = crud_user.get(db=SessionDep, id=payload.sub)
    if not user:
        raise HTTPException(status_code=404, detail="ユーザーが見つかりません")
    if not user.is_active:
        raise HTTPException(status_code=400, detail="ログイン権限がありません")

    role = "admin" if user.is_admin else "user"

    return Token(
        access_token=security.create_access_token(user.id, role),
    )


@router.post("/signup", response_model=Token)
def signup(session: SessionDep, user_in: UserCreateMe) -> Token:
    obj_in = UserCreate(
        is_active=True,
        is_admin=False,
        **user_in.dict(),
    )
    user = crud_user.create(db=session, obj_in=obj_in, user_id=None)
    role = "admin" if user.is_admin else "user"

    return Token(
        access_token=security.create_access_token(user.id, role),
        id_token=security.create_id_token(user, role),
        refresh_token=security.create_refresh_token(user.id, role),
    )
