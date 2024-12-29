import asyncio
from datetime import datetime
from typing import Dict

from main import url2video

from . import crud
from .config import settings
from .database import AsyncSessionLocal
from .models import TaskStatus


class TaskService:
    _running_tasks = 0
    _semaphore = asyncio.Semaphore(settings.MAX_CONCURRENT_TASKS)
    _background_tasks: Dict[int, asyncio.Task] = {}

    @classmethod
    async def cleanup_task(cls, task_id: int):
        cls._background_tasks.pop(task_id, None)
        cls._running_tasks = max(0, cls._running_tasks - 1)

    @classmethod
    async def process_task(cls, task_id: int, name: str):
        try:
            async with cls._semaphore:
                cls._running_tasks += 1

                async with AsyncSessionLocal() as session:
                    task = await crud.get_task(session, task_id)
                    if task:
                        task.status = TaskStatus.RUNNING
                        task.start_time = datetime.now()
                        await session.commit()

                    try:
                        result = await asyncio.wait_for(
                            url2video(name),
                            timeout=float(settings.TASK_TIMEOUT_SECONDS),
                        )

                        await crud.update_task_status(
                            session, task, TaskStatus.COMPLETED, result=result
                        )

                    except asyncio.CancelledError:
                        await crud.update_task_status(
                            session,
                            task,
                            TaskStatus.FAILED,
                            "Task was manually cancelled",
                        )
                        raise

                    except asyncio.TimeoutError:
                        await crud.update_task_status(
                            session,
                            task,
                            TaskStatus.TIMEOUT,
                            f"Task exceeded {settings.TASK_TIMEOUT_SECONDS} second timeout limit",
                        )

                    except Exception as e:
                        await crud.update_task_status(
                            session, task, TaskStatus.FAILED, str(e)
                        )
                        raise

        finally:
            await cls.cleanup_task(task_id)

    @classmethod
    def cancel_all_background_tasks(cls):
        for task in cls._background_tasks.values():
            task.cancel()
