from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TaskCreate(BaseModel):
    name: str
    prompt_source: Optional[str] = None
    tts_source: Optional[str] = None
    material_source: Optional[str] = None


class TaskResponse(BaseModel):
    id: int
    name: str
    status: str
    create_time: datetime
    update_time: datetime
    start_time: Optional[datetime] = None
    end_time: Optional[datetime] = None
    result: Optional[str] = None
    error_message: Optional[str] = None

    class Config:
        from_attributes = True
