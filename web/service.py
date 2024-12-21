import asyncio
import logging
import uuid
from datetime import datetime
from typing import Dict

from sqlalchemy import func, select
from sqlalchemy.ext.asyncio import AsyncSession

from main import url2video

from .config import settings
from .model import Task, TaskStatus
from .session import AsyncSessionLocal

logger = logging.getLogger(__name__)


class TaskService:
    _tasks: Dict[str, asyncio.Task] = {}
    _semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_TASKS)

    @staticmethod
    async def create_task(session: AsyncSession, name: str) -> Task:
        task_id = str(uuid.uuid4())
        db_task = Task(id=task_id, name=name, status=TaskStatus.PENDING)
        session.add(db_task)
        await session.commit()
        return db_task

    @staticmethod
    async def get_task(session: AsyncSession, task_id: str) -> Task:
        stmt = select(Task).where(Task.id == task_id)
        result = await session.execute(stmt)
        return result.scalar_one_or_none()

    @staticmethod
    async def update_task_status(
        session: AsyncSession,
        task_id: str,
        status: TaskStatus,
        result: str = None,
        error_message: str = None,
    ):
        task = await TaskService.get_task(session, task_id)
        if task:
            task.status = status
            if status == TaskStatus.RUNNING:
                task.start_time = datetime.now()
            elif status in [
                TaskStatus.COMPLETED,
                TaskStatus.FAILED,
                TaskStatus.TIMEOUT,
            ]:
                task.end_time = datetime.now()
            if result:
                task.result = result
            if error_message:
                task.error_message = error_message
            await session.commit()

    @classmethod
    async def execute_task_with_timeout(cls, task_id: str, name: str):
        """实际的任务执行逻辑，在单独的进程中运行"""

        try:
            async with AsyncSessionLocal() as session:
                await cls.update_task_status(session, task_id, TaskStatus.RUNNING)

            result = await url2video(name)

            async with AsyncSessionLocal() as session:
                await cls.update_task_status(
                    session, task_id, TaskStatus.COMPLETED, result=result
                )

        except Exception as e:
            async with AsyncSessionLocal() as session:
                await cls.update_task_status(
                    session, task_id, TaskStatus.FAILED, str(e)
                )

    @classmethod
    async def process_task(cls, task_id: str, name: str):
        """处理任务，包含超时控制"""
        try:
            async with cls._semaphore:
                try:
                    await asyncio.wait_for(
                        cls.execute_task_with_timeout(task_id, name),
                        timeout=settings.TASK_TIMEOUT_SECONDS,
                    )
                except asyncio.TimeoutError:
                    # 超时处理
                    if task_id in cls._tasks:
                        task = cls._tasks[task_id]
                        if not task.done():
                            task.cancel()

                    async with AsyncSessionLocal() as session:
                        await cls.update_task_status(
                            session,
                            task_id,
                            TaskStatus.TIMEOUT,
                            f"Task exceeded timeout of {settings.TASK_TIMEOUT_SECONDS} seconds",
                        )
        finally:
            # 清理任务记录
            cls._tasks.pop(task_id, None)

    @classmethod
    async def cancel_task(cls, session: AsyncSession, task_id: str) -> bool:
        if task_id in cls._tasks:
            task = cls._tasks[task_id]
            if not task.done():
                task.cancel()

        await cls.update_task_status(
            session, task_id, TaskStatus.FAILED, "Task was cancelled"
        )
        return True

    @classmethod
    def start_background_task(cls, task_id: str, name: str):
        task = asyncio.create_task(cls.process_task(task_id, name))
        cls._tasks[task_id] = task
        return task

    @classmethod
    async def get_queue_status(cls, session: AsyncSession):
        # 获取各种状态的任务数量
        stmt = select(Task.status, func.count(Task.id)).group_by(Task.status)
        result = await session.execute(stmt)
        status_counts = dict(result.all())

        return {
            "max_concurrent_tasks": settings.MAX_CONCURRENT_TASKS,
            "running_tasks": status_counts.get(TaskStatus.RUNNING, 0),
            "pending_tasks": status_counts.get(TaskStatus.PENDING, 0),
            "completed_tasks": status_counts.get(TaskStatus.COMPLETED, 0),
            "failed_tasks": status_counts.get(TaskStatus.FAILED, 0),
            "timeout_tasks": status_counts.get(TaskStatus.TIMEOUT, 0),
            "available_slots": settings.MAX_CONCURRENT_TASKS
            - status_counts.get(TaskStatus.RUNNING, 0),
        }
