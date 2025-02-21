from typing import List

from pydantic import BaseModel, ConfigDict


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
    api_key: str
    model: str
    voices: List[str]


class VideoConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fps: int
    font: str
    opening_audio: str
    background_audio: str
    width: int
    height: int


class ApiConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    database_url: str
    app_port: int
    max_concurrent_tasks: int
    task_timeout_seconds: int


class PexelsConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str
    minimum_duration: int
    prompt: str


class Config(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    llm: LLMConfig
    tts: TTSConfig
    video: VideoConfig
    api: ApiConfig
    pexels: PexelsConfig
