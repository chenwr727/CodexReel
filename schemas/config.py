from enum import Enum
from typing import List, Optional

from pydantic import BaseModel, ConfigDict


class PromptSource(str, Enum):
    crosstalk = "crosstalk"
    talkshow = "talkshow"
    book = "book"


class TTSSource(str, Enum):
    dashscope = "dashscope"
    edge = "edge"
    hailuo = "hailuo"
    kokoro = "kokoro"


class MaterialSource(str, Enum):
    pixabay = "pixabay"
    pexels = "pexels"


class LLMConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str
    base_url: str
    model: str
    prompt: PromptSource = PromptSource.crosstalk


class PromptConfig(BaseModel):
    prompt_writer: str = ""
    prompt_reflector: str = ""
    prompt_rewriter: str = ""


class TTSDashscopeConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str = ""
    model: str = ""
    voices: List[str] = []


class TTSEdgeConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    voices: List[str] = []


class TTSKokoroConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    model: str = ""
    voices: List[str]
    config: str = ""
    lang_code: str = ""


class TTSHaiLuoConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str = ""
    base_url: str = ""
    voices: List[str] = []


class TTSConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source: TTSSource
    dashscope: Optional[TTSDashscopeConfig] = None
    edge: Optional[TTSEdgeConfig] = None
    hailuo: Optional[TTSHaiLuoConfig] = None
    kokoro: Optional[TTSKokoroConfig] = None


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


class TitleConfig(SubtitleConfig):
    model_config = ConfigDict(from_attributes=True)
    duration: float = 0.5


class VideoConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    fps: int
    background_audio: str
    width: int
    height: int
    title: TitleConfig
    subtitle: SubtitleConfig


class ApiConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    database_url: str
    app_port: int
    max_concurrent_tasks: int
    task_timeout_seconds: int


class MaterialPexelsConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str = ""
    locale: str = ""


class MaterialPixabayConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    api_key: str = ""
    lang: str = "zh"
    video_type: str = "all"


class MaterialConfig(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    source: MaterialSource
    minimum_duration: int
    prompt: str
    pexels: Optional[MaterialPexelsConfig] = None
    pixabay: Optional[MaterialPixabayConfig] = None


class Config(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    llm: LLMConfig
    prompt: Optional[PromptConfig] = None
    tts: TTSConfig
    video: VideoConfig
    api: ApiConfig
    material: MaterialConfig
