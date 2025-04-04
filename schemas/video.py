from typing import List

from pydantic import BaseModel, ConfigDict


class Dialogue(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    speaker: str
    contents: List[str]


class Paragraph(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    description: str
    dialogues: List[Dialogue]


class VideoTranscript(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    title: str
    paragraphs: List[Paragraph]


class MaterialInfo(BaseModel):
    url: str
    duration: int
    video_path: str = ""
