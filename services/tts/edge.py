from typing import List

import edge_tts

from .base import TextToSpeechConverter


class EdgeTextToSpeechConverter(TextToSpeechConverter):
    def __init__(self, voices: List[str], folder: str):
        super().__init__(voices, folder)

    async def generate_audio(self, content, voice, file_name):
        communicate = edge_tts.Communicate(content, voice)
        await communicate.save(file_name)
