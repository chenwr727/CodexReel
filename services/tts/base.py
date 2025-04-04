import os
import time
from abc import ABC, abstractmethod
from typing import List

from moviepy import AudioFileClip

from schemas.video import Paragraph
from utils.log import logger


class TextToSpeechConverter(ABC):

    def __init__(self, voices: List[str], folder: str):
        self.voices = voices
        self.folder = folder

    async def text_to_speech(self, paragraphs: List[Paragraph]) -> List[float]:
        durations = []

        speaker_voice = {}
        idx_voice = 0
        for paragraph in paragraphs:
            dialogues = paragraph.dialogues
            for dialogue in dialogues:
                if dialogue.speaker not in speaker_voice:
                    speaker_voice[dialogue.speaker] = self.voices[idx_voice]
                    idx_voice += 1

        for i, paragraph in enumerate(paragraphs, start=1):
            logger.info(f"Processing paragraph {i}/{len(paragraphs)}")
            dialogues = paragraph.dialogues
            duration = 0
            for j, dialogue in enumerate(dialogues, start=1):
                logger.info(f"Processing dialogue {j}/{len(dialogues)}")
                file_prefix = f"{i}_{j}"
                duration += await self.process_dialogue(speaker_voice[dialogue.speaker], dialogue.contents, file_prefix)
            durations.append(duration)
        return durations

    async def process_dialogue(self, voice: str, contents: List[str], file_prefix: str, max_retries: int = 3):
        duration = 0

        for i, content in enumerate(contents, start=1):
            file_name = os.path.join(self.folder, f"{file_prefix}_{i}.mp3")
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
                    logger.error(f"Error generate audio {file_prefix}_{i}")
                    raise ValueError("Error generate audio")
                time.sleep(3)
            duration += AudioFileClip(file_name).duration
        return duration

    @abstractmethod
    async def generate_audio(self, content: str, voice: str, file_name: str):
        pass
