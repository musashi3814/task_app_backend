from datetime import datetime

from app.schemas.base_schema import BaseSchema


class Token(BaseSchema):
    id_token: str
    access_token: str
    refresh_token: str
    token_type: str = "bearer"


class AccessTokenPayload(BaseSchema):
    sub: str
    iss: str
    aud: str
    exp: datetime
    iat: datetime
    role: str


class IdTokenPayload(BaseSchema):
    sub: str
    iss: str
    aud: str
    exp: datetime
    iat: datetime
    name: str
    email: str
    roles: str


class RefreshTokenPayload(BaseSchema):
    sub: str
    iss: str
    aud: str
    exp: datetime
    iat: datetime
