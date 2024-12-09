import os
import subprocess

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
from tqdm import tqdm

from utils.log import logger


class TextToSpeechConverter:
    def __init__(self, api_key: str, model: str, voices: list[str], folder: str):
        self.api_key = api_key
        self.model = model
        self.voices = voices
        self.folder = folder

        dashscope.api_key = self.api_key

    def process_dialogue(self, index: int, dialogue: dict):
        file_names = []

        contents = dialogue["contents"]

        # 根据发言者选择声音
        if index % 2 == 0:
            voice = self.voices[0]
        else:
            voice = self.voices[1]

        for i, content in enumerate(contents):
            file_name = os.path.join(self.folder, f"{index}_{i}.mp3")
            if os.path.exists(file_name):
                file_names.append(file_name)
                continue
            try:
                synthesizer = SpeechSynthesizer(
                    model=self.model, voice=voice, speech_rate=1.1
                )
                audio = synthesizer.call(content)
                with open(file_name, "wb") as f:
                    f.write(audio)
                file_names.append(file_name)
            except Exception as e:
                logger.error(f"合成语音时发生错误: {e}")
                if os.path.exists(file_name):
                    os.remove(file_name)
                return None
        return file_names

    def text_to_speech(self, dialogues: list[dict], output_file: str):
        file_list = []

        for i, dialogue in tqdm(
            enumerate(dialogues), desc="生成语音", total=len(dialogues)
        ):
            file_names = self.process_dialogue(i, dialogue)
            if file_names:
                file_list.extend(file_names)
            else:
                logger.error(f"无法合成{i}的语音")
                return

        try:
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    f"concat:{'|'.join(file_list)}",
                    "-acodec",
                    "copy",
                    output_file,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg执行失败: {e}")
        except Exception as e:
            logger.error(f"未知错误: {e}")
