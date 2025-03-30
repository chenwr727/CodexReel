from datetime import datetime

from sqlalchemy import func, select
from sqlalchemy.orm import Session

from .models import Task, TaskStatus
from .schemas import TaskCreate


async def create_task(session: Session, task: TaskCreate) -> Task:
    result = await session.execute(select(Task).where(Task.name == task.name))
    db_task = result.scalars().first()
    if db_task:
        db_task.status = TaskStatus.PENDING
        return db_task
    else:
        db_task = Task(name=task.name, status=TaskStatus.PENDING)
        session.add(db_task)
    await session.commit()
    await session.refresh(db_task)
    return db_task


async def get_task(session: Session, task_id: int) -> Task:
    return await session.get(Task, task_id)


async def get_status(session: Session, task_date: str) -> dict[str, int]:
    result = await session.execute(
        select(Task.status, func.count(Task.id)).where(Task.create_time.like(f"%{task_date}%")).group_by(Task.status)
    )
    return dict(result.all())


async def get_task_list(session: Session, task_date: str) -> list[Task]:
    result = await session.execute(select(Task).where(Task.update_time.like(f"%{task_date}%")))
    return result.scalars().all()


async def update_task_status(session: Session, task: Task, status: TaskStatus, error_message=None, result=None) -> Task:
    task.status = status
    if status == TaskStatus.RUNNING:
        task.start_time = datetime.now()
        task.end_time = None
    else:
        task.end_time = datetime.now()
    task.result = result
    task.error_message = error_message
    await session.commit()
