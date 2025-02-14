from typing import Annotated

from fastapi import APIRouter

from app.api.deps import RequestFormDep, SessionDep
from app.schemas.token import Token

router = APIRouter()


@router.post("/", response_model=Token)
def login_access_token(session: SessionDep, form_data: RequestFormDep) -> Token:
    return Token()


@router.post("/refresh", response_model=Token)
def refresh_access_token(session: SessionDep, form_data: RequestFormDep) -> Token:
    return Token()


@router.post("/signup", response_model=Token)
def signup_access_token(session: SessionDep, form_data: RequestFormDep) -> Token:
    return Token()


@router.post("/logout")
def logout(session: SessionDep) -> None:
    return None
