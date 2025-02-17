from datetime import datetime
from typing import Optional

from pydantic import EmailStr

from app.schemas.base_schema import BaseSchema


class UserBase(BaseSchema):
    id: Optional[int] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False
    last_login: Optional[datetime] = None


class Abst_User(BaseSchema):
    user_id: int
    user_name: str
    user_email: EmailStr
    is_admin: bool


class SummaryUser(UserBase):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    last_login: Optional[datetime] = None


class InfoUser(SummaryUser):
    count_wait: int
    count_work: int
    created_at: datetime
    created_by: Optional[int] = None


class UserMe(BaseSchema):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool
    created_at: datetime
    created_by: Optional[int] = None
    last_login: Optional[datetime] = None


# Properties to receive via API on creation


class UserCreateMe(BaseSchema):
    email: EmailStr
    password: str
    name: str


class UserCreate(UserCreateMe):
    is_active: bool = True
    is_admin: bool = False


# Properties to receive via API on update
class UserUpdate(BaseSchema):
    is_active: Optional[bool] = True
    is_admin: Optional[bool] = False


class UserUpdateMe(BaseSchema):
    email: Optional[EmailStr] = None
    name: Optional[str] = None
    password: Optional[str] = None
