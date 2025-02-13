from collections.abc import Generator
from typing import Annotated

from fastapi import Depends
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from sqlmodel import Session

from app.core.config import settings
from app.db.db import engine
from app.models.users import Users

reusable_oauth2 = OAuth2PasswordBearer(tokenUrl=f"{settings.API_V1_STR}/token/")


def get_db() -> Generator[Session, None, None]:
    with Session(engine) as session:
        yield session


SessionDep = Annotated[Session, Depends(get_db)]
RequestFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]
TokenDep = Annotated[str, Depends(reusable_oauth2)]
