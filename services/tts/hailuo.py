from typing import List

from openai import OpenAI

from .base import TextToSpeechConverter


class HaiLuoTextToSpeechConverter(TextToSpeechConverter):
    def __init__(self, api_key: str, base_url: str, voices: List[str], folder: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        super().__init__(voices, folder)

    async def generate_audio(self, content: str, voice: str, file_name: str):
        with self.client.audio.speech.with_streaming_response.create(
            model="hailuo", voice=voice, input=content, speed=1.2
        ) as response:
            response.stream_to_file(file_name)
