from datetime import datetime
from typing import Optional

from app.schemas.base_schema import BaseSchema


class Token(BaseSchema):
    id_token: Optional[str] = None
    access_token: str
    refresh_token: Optional[str] = None
    token_type: str = "bearer"


class AccessTokenPayload(BaseSchema):
    sub: int
    exp: datetime
    iat: datetime
    role: str


class IdTokenPayload(BaseSchema):
    sub: int
    exp: datetime
    iat: datetime
    name: str
    email: str
    roles: str


class RefreshTokenPayload(BaseSchema):
    sub: int
    exp: datetime
    iat: datetime
