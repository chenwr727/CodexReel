import asyncio
from typing import List

from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from api import crud
from api.database import get_session
from api.models import TaskStatus
from api.schemas import TaskCreate, TaskResponse
from api.service import TaskService
from utils.config import api_config as settings

tasks_router = APIRouter()


@tasks_router.post("/", response_model=TaskResponse)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    db_task = await crud.create_task(session, task)

    background_task = asyncio.create_task(TaskService.process_task(db_task.id, task))
    TaskService._background_tasks[db_task.id] = background_task

    return db_task


@tasks_router.post("/{task_id}/cancel")
async def cancel_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != TaskStatus.RUNNING:
        raise HTTPException(status_code=400, detail="Only running tasks can be cancelled")

    background_task = TaskService._background_tasks.get(task_id)
    if background_task and not background_task.done():
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass

    return {"message": "Task was cancelled"}


@tasks_router.get("/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@tasks_router.get("/queue/status/{task_date}")
async def get_queue_status(task_date: str, session: AsyncSession = Depends(get_session)):
    status_counts = await crud.get_status(session, task_date)
    return {
        "max_concurrent_tasks": settings.max_concurrent_tasks,
        "running_tasks": status_counts.get(TaskStatus.RUNNING, 0),
        "pending_tasks": status_counts.get(TaskStatus.PENDING, 0),
        "completed_tasks": status_counts.get(TaskStatus.COMPLETED, 0),
        "failed_tasks": status_counts.get(TaskStatus.FAILED, 0),
        "timeout_tasks": status_counts.get(TaskStatus.TIMEOUT, 0),
        "available_slots": settings.max_concurrent_tasks - TaskService._running_tasks,
    }


@tasks_router.get("/list/{task_date}", response_model=List[TaskResponse])
async def get_task_list(task_date: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_task_list(session, task_date)
