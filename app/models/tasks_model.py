from decimal import Decimal
from uuid import UUID

from sqlalchemy import Column, DateTime, ForeignKey, Integer, String
from sqlalchemy.orm import relationship

from app.models.base_model import Base, CommonColumns


class Tasks(Base, CommonColumns):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    title = Column(String, index=True, nullable=False)
    description = Column(String, nullable=True)
    status_id = Column(Integer, ForeignKey("task_status.id"), nullable=False)
    tag_id = Column(Integer, ForeignKey("tags.id"), nullable=True)
    due_date = Column(DateTime, nullable=True)
    priority_id = Column(Integer, ForeignKey("priority.id"), nullable=False)

    assign = relationship("Task_Assign", back_populates="tasks")
    status = relationship("Task_Status", back_populates="tasks")
    priority = relationship("Task_Priority", back_populates="tasks")


class Task_Assign(Base, CommonColumns):
    __tablename__ = "task_assign"

    task_id = Column(Integer, ForeignKey("tasks.id"), primary_key=True)
    user_id = Column(Integer, ForeignKey("users.id"), primary_key=True)

    tasks = relationship("Tasks", back_populates="assign")
    user = relationship("Users", back_populates="assign")


class Task_Status(Base):
    __tablename__ = "task_status"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#FFFFFF", nullable=False)

    tasks = relationship("Tasks", back_populates="status")


class Task_Priority(Base):
    __tablename__ = "priority"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True, nullable=False)
    color = Column(String, default="#FFFFFF", nullable=False)

    tasks = relationship("Tasks", back_populates="priority")
