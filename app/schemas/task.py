from datetime import datetime
from typing import Optional

from app.schemas.base_schema import BaseSchema
from app.schemas.user import Abst_User


class SummaryTask(BaseSchema):
    id: int
    title: str
    due_date: Optional[datetime]
    status_id: int
    status: str
    priority_id: int
    priority: str
    assigned: Optional[Abst_User]


class InfoTask(SummaryTask):
    description: Optional[str]
    tag_id: Optional[int]
    tag: Optional[str]
    created_at: datetime
    created_by: Abst_User


class TaskCreate(BaseSchema):
    title: str
    description: Optional[str]
    due_date: Optional[datetime]
    status_id: int
    priority_id: int
    tag_id: Optional[int]
    assigned_id: Optional[int]


class TaskUpdate(BaseSchema):
    title: Optional[str]
    description: Optional[str]
    due_date: Optional[datetime]
    status_id: Optional[int]
    priority_id: Optional[int]
    tag_id: Optional[int]
    assigned_id: Optional[int]


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
    name: Optional[str]
    color: Optional[str]
