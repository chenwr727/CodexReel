import os
import time
from typing import List

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
from moviepy import AudioFileClip
from tqdm import tqdm

from utils.log import logger
from utils.schema import Dialogue


class TextToSpeechConverter:
    def __init__(self, api_key: str, model: str, voices: List[str], folder: str):
        self.api_key = api_key
        self.model = model
        self.voices = voices
        self.folder = folder

        dashscope.api_key = self.api_key

    async def process_dialogue(self, index: int, dialogue: Dialogue):
        duration = 0

        contents = dialogue.contents
        voice = self.voices[index % 2]

        for i, content in enumerate(contents):
            file_name = os.path.join(self.folder, f"{index}_{i}.mp3")
            if os.path.exists(file_name):
                duration += AudioFileClip(file_name).duration
                continue
            synthesizer = SpeechSynthesizer(model=self.model, voice=voice, speech_rate=1.2)
            for _ in range(3):
                try:
                    audio = synthesizer.call(content)
                    with open(file_name, "wb") as f:
                        f.write(audio)
                    duration += AudioFileClip(file_name).duration
                    break
                except Exception as e:
                    logger.error(f"Error generate audio file: {e}")
                    if os.path.exists(file_name):
                        os.remove(file_name)
                    time.sleep(3)
                    continue
            time.sleep(2)
        return duration

    async def text_to_speech(self, dialogues: List[Dialogue]):
        durations = []

        for i, dialogue in tqdm(enumerate(dialogues), desc="Create Audio", total=len(dialogues)):
            duration = await self.process_dialogue(i, dialogue)
            if duration:
                durations.append(duration)
            else:
                logger.error(f"Error generate audio {i}")
                return []
        return durations
