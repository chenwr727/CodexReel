import asyncio

from robyn import Robyn

from web.api import cancel_task, create_task, get_queue_status, get_task_status
from web.config import settings
from web.model import Base
from web.session import engine


async def init_db():
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)


app = Robyn(__file__)

app.post("/v1/tasks")(create_task)
app.get("/v1/tasks/:task_id")(get_task_status)
app.get("/v1/tasks/queue/status")(get_queue_status)
app.get("/v1/tasks/cancel/:task_id")(cancel_task)

if __name__ == "__main__":
    asyncio.run(init_db())
    app.start(port=settings.APP_PORT)
