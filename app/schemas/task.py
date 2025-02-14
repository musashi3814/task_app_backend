from datetime import datetime
from typing import List, Optional

from app.schemas.base_schema import BaseSchema
from app.schemas.user import Abst_User


class SummaryTask(BaseSchema):
    id: int
    title: str
    due_date: Optional[datetime] = None
    status_id: int
    status: str
    priority_id: int
    priority: str


class InfoTask(SummaryTask):
    description: Optional[str] = None
    assigned: Optional[List[int]] = None
    created_at: datetime
    created_by: int


class TaskCreate(BaseSchema):
    title: str
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status_id: int
    priority_id: int
    assigned_id: List[int]


class TaskUpdate(BaseSchema):
    title: Optional[str] = None
    description: Optional[str] = None
    due_date: Optional[datetime] = None
    status_id: Optional[int] = None
    priority_id: Optional[int] = None
    tag_id: Optional[int] = None
    assigned_id: Optional[List[int]] = None


class Task_Status(BaseSchema):
    id: int
    name: str
    color: str


class Task_Priority(BaseSchema):
    id: int
    name: str
    color: str


class Task_Tag(BaseSchema):
    id: int
    name: str
    color: str


class Task_Status_Update(BaseSchema):
    color: Optional[str]


class Task_Tag_Create(BaseSchema):
    name: str
    color: str


class Task_Tag_Update(BaseSchema):
    name: Optional[str] = None
    color: Optional[str] = None
