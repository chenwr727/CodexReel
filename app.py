import asyncio
from contextlib import asynccontextmanager
from typing import List

from fastapi import Depends, FastAPI, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession

from web import crud
from web.config import settings
from web.database import engine, get_session, init_db
from web.models import TaskStatus
from web.schemas import TaskCreate, TaskResponse
from web.service import TaskService


@asynccontextmanager
async def lifespan(app: FastAPI):
    await init_db()
    yield
    TaskService.cancel_all_background_tasks()
    await engine.dispose()


app = FastAPI(lifespan=lifespan)


@app.post("/v1/tasks", response_model=TaskResponse)
async def create_task(task: TaskCreate, session: AsyncSession = Depends(get_session)):
    db_task = await crud.create_task(session, task)

    background_task = asyncio.create_task(
        TaskService.process_task(db_task.id, db_task.name)
    )
    TaskService._background_tasks[db_task.id] = background_task

    return db_task


@app.post("/v1/tasks/{task_id}/cancel")
async def cancel_task(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")

    if task.status != TaskStatus.RUNNING:
        raise HTTPException(
            status_code=400, detail="Only running tasks can be cancelled"
        )

    background_task = TaskService._background_tasks.get(task_id)
    if background_task and not background_task.done():
        background_task.cancel()
        try:
            await background_task
        except asyncio.CancelledError:
            pass

    return {"message": "Task was cancelled"}


@app.get("/v1/tasks/{task_id}", response_model=TaskResponse)
async def get_task_status(task_id: int, session: AsyncSession = Depends(get_session)):
    task = await crud.get_task(session, task_id)
    if not task:
        raise HTTPException(status_code=404, detail="Task not found")
    return task


@app.get("/v1/tasks/queue/status/{task_date}")
async def get_queue_status(
    task_date: str, session: AsyncSession = Depends(get_session)
):
    status_counts = await crud.get_status(session, task_date)
    return {
        "max_concurrent_tasks": settings.MAX_CONCURRENT_TASKS,
        "running_tasks": status_counts.get(TaskStatus.RUNNING, 0),
        "pending_tasks": status_counts.get(TaskStatus.PENDING, 0),
        "completed_tasks": status_counts.get(TaskStatus.COMPLETED, 0),
        "failed_tasks": status_counts.get(TaskStatus.FAILED, 0),
        "timeout_tasks": status_counts.get(TaskStatus.TIMEOUT, 0),
        "available_slots": settings.MAX_CONCURRENT_TASKS - TaskService._running_tasks,
    }


@app.get("/v1/tasks/list/{task_date}", response_model=List[TaskResponse])
async def get_task_list(task_date: str, session: AsyncSession = Depends(get_session)):
    return await crud.get_task_list(session, task_date)


if __name__ == "__main__":
    import uvicorn

    uvicorn.run("app:app", host="0.0.0.0", port=settings.APP_PORT)
