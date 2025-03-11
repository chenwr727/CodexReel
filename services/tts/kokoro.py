from typing import List

import soundfile as sf
from kokoro import KModel, KPipeline

from .base import TextToSpeechConverter


class KokoroTextToSpeechConverter(TextToSpeechConverter):
    def __init__(self, config: str, model: str, lang_code: str, voices: List[str], folder: str):
        super().__init__(voices, folder)
        model = KModel(config=config, model=model)
        self.pipeline = KPipeline(lang_code=lang_code, model=model)

    async def generate_audio(self, content: str, voice: str, file_name: str):
        generator = self.pipeline(content, voice=voice, speed=1.2, split_pattern=r"\n+")
        for _, _, audio in generator:
            sf.write(file_name, audio, 24000)
