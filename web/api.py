from robyn import Request, Response

from .model import TaskStatus
from .service import TaskService
from .session import AsyncSessionLocal


def _create_response(status_code: int, description: str) -> Response:
    return Response(
        status_code=status_code,
        headers={"Content-Type": "text"},
        description=description,
    )


async def create_task(request: Request) -> Response:
    try:
        data = request.json()
        task_name = data.get("name")
        if not task_name:
            return _create_response(400, "Task name is required")

        async with AsyncSessionLocal() as session:
            task = await TaskService.create_task(session, task_name)
            TaskService.start_background_task(task.id, task_name)

        return _create_response(201, task.id)
    except Exception as e:
        return _create_response(500, str(e))


async def get_task_status(request: Request) -> Response:
    try:
        task_id = request.path_params.get("task_id")

        async with AsyncSessionLocal() as session:
            task = await TaskService.get_task(session, task_id)
            if not task:
                return _create_response(404, "Task not found")

            return task.to_dict()
    except Exception as e:
        return _create_response(500, str(e))


async def get_queue_status(request: Request) -> Response:
    try:
        async with AsyncSessionLocal() as session:
            status = await TaskService.get_queue_status(session)
            return status
    except Exception as e:
        return _create_response(500, str(e))


async def cancel_task(request: Request) -> Response:
    try:
        task_id = request.path_params.get("task_id")

        async with AsyncSessionLocal() as session:
            task = await TaskService.get_task(session, task_id)
            if not task:
                return _create_response(404, "Task not found")

            if task.status != TaskStatus.RUNNING:
                return _create_response(400, "Only running tasks can be cancelled")

            success = await TaskService.cancel_task(session, task_id)
            if success:
                return _create_response(200, "Task cancelled successfully")
            else:
                return _create_response(400, "Task could not be cancelled")

    except Exception as e:
        return _create_response(500, str(e))
