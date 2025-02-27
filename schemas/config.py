from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class TTSSource(str, Enum):
    dashscope = "dashscope"
    edge = "edge"


class MaterialSource(str, Enum):
    pexels = "pexels"
    pixabay = "pixabay"


class LLMConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str
    base_url: str
    model: str
    prompt_writer: str
    prompt_reflector: str
    prompt_rewriter: str


class TTSConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source: TTSSource
    api_key: str = ""
    model: str = ""
    voices: List[str]


class SubtitleConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    font: str
    width_ratio: float = 0.8
    font_size_ratio: int = 17
    position_ratio: float = 2 / 3
    color: str = "white"
    stroke_color: str = "black"
    stroke_width: int = 1
    text_align: str = "center"


class VideoConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fps: int
    background_audio: str
    width: int
    height: int
    subtitle: Optional[SubtitleConfig] = None


class ApiConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    database_url: str
    app_port: int
    max_concurrent_tasks: int
    task_timeout_seconds: int


class MaterialConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source: MaterialSource
    api_key: str
    minimum_duration: int
    prompt: str
    locale: str = ""
    lang: str = "zh"
    video_type: str = "all"


class Config(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    llm: LLMConfig
    tts: TTSConfig
    video: VideoConfig
    api: ApiConfig
    material: MaterialConfig
