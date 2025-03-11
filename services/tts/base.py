import os
import time
from abc import ABC, abstractmethod
from typing import List

from moviepy import AudioFileClip

from schemas.video import Dialogue
from utils.log import logger


class TextToSpeechConverter(ABC):

    def __init__(self, voices: List[str], folder: str):
        self.voices = voices
        self.folder = folder

    async def text_to_speech(self, dialogues: List[Dialogue]):
        durations = []

        total = len(dialogues)
        for i, dialogue in enumerate(dialogues):
            logger.info(f"Generating audio {i+1}/{total}")
            duration = await self.process_dialogue(i, dialogue)
            if duration:
                durations.append(duration)
            else:
                logger.error(f"Error generate audio {i}")
                raise ValueError("Error generate audio")
        return durations

    async def process_dialogue(self, index: int, dialogue: Dialogue, max_retries: int = 3):
        duration = 0

        contents = dialogue.contents
        voice = self.voices[index % len(self.voices)]

        for i, content in enumerate(contents):
            file_name = os.path.join(self.folder, f"{index}_{i}.mp3")
            if not os.path.exists(file_name):
                for _ in range(max_retries):
                    try:
                        await self.generate_audio(content, voice, file_name)
                        break
                    except Exception as e:
                        logger.error(f"Error generate audio file: {e}")
                        if os.path.exists(file_name):
                            os.remove(file_name)
                        time.sleep(3)
                        continue
                else:
                    logger.error(f"Error generate audio {index}_{i}")
                    raise ValueError("Error generate audio")
                time.sleep(3)
            duration += AudioFileClip(file_name).duration
        return duration

    @abstractmethod
    async def generate_audio(self, content: str, voice: str, file_name: str):
        pass
