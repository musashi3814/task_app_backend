from decimal import Decimal
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base import Base, CommonColumns


class Tasks(Base, CommonColumns):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)

    status = relationship("Task_Status", back_populates="tasks")
    tags = relationship("Task_Tags", back_populates="tasks")


class Task_Assign(Base, CommonColumns):
    __tablename__ = "task_assign"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)


class Task_Status(Base, CommonColumns):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#FFFFFF", nullable=False)

    tasks = relationship("Tasks", back_populates="status")


class Task_Tags(Base, CommonColumns):
    __tablename__ = "tags"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#FFFFFF", nullable=False)

    tasks = relationship("Tasks", back_populates="tags")
