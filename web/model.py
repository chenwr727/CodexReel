from datetime import datetime
from enum import Enum

from sqlalchemy import Column, DateTime
from sqlalchemy import Enum as SQLAlchemyEnum
from sqlalchemy import String
from sqlalchemy.ext.declarative import declarative_base

Base = declarative_base()


class TaskStatus(str, Enum):
    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    TIMEOUT = "timeout"  # 新增超时状态

    def __str__(self):
        return self.value


class Task(Base):
    __tablename__ = "tasks"

    id = Column(String, primary_key=True)
    name = Column(String, nullable=False)
    status = Column(SQLAlchemyEnum(TaskStatus), default=TaskStatus.PENDING)
    create_time = Column(DateTime, default=datetime.now)
    update_time = Column(DateTime, default=datetime.now, onupdate=datetime.now)
    start_time = Column(DateTime, nullable=True)  # 任务开始时间
    end_time = Column(DateTime, nullable=True)  # 任务结束时间
    result = Column(String, nullable=True)  # 任务结果
    error_message = Column(String, nullable=True)  # 错误信息

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
