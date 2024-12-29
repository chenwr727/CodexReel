from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import Integer, String

from .database import Base


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"

    def __str__(self):
        return self.value


class Task(Base):
    __tablename__ = "tasks"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    start_time = Column(DateTime, nullable=True)
    end_time = Column(DateTime, nullable=True)
    result = Column(String, nullable=True)
    error_message = Column(String, nullable=True)

    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "status": self.status.value,
            "create_time": self.create_time.isoformat(),
            "update_time": self.update_time.isoformat(),
            "start_time": self.start_time.isoformat() if self.start_time else None,
            "end_time": self.end_time.isoformat() if self.end_time else None,
            "result": self.result,
            "error_message": self.error_message,
        }
