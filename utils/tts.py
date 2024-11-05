import os
import subprocess
import time

import dashscope
from dashscope.audio.tts_v2 import SpeechSynthesizer
from tqdm import tqdm

from utils.log import logger


class TextToSpeechConverter:
    def __init__(self, api_key, model, voices, chapter):
        self.api_key = api_key
        self.model = model
        self.voices = voices
        self.chapter = chapter
        self.output_file = f"{chapter}.mp3"

        dashscope.api_key = self.api_key

    def process_dialogue(self, index, dialogue, retry_delay=2):
        file_name = os.path.join(self.chapter, f"{index}.mp3")
        if os.path.exists(file_name):
            return file_name

        speaker = dialogue["speaker"]
        content = dialogue["content"]

        # 根据发言者选择声音
        if speaker == "发言者1":
            voice = self.voices[0]
        elif speaker == "发言者2":
            voice = self.voices[1]

        time.sleep(retry_delay)

        synthesizer = SpeechSynthesizer(model=self.model, voice=voice)
        try:
            audio = synthesizer.call(content)
            with open(file_name, "wb") as f:
                f.write(audio)
            return file_name
        except Exception as e:
            logger.error(f"合成语音时发生错误: {e}")
            if os.path.exists(file_name):
                os.remove(file_name)
            return None

    def text_to_speech(self, dialogues):
        file_names = []

        for i, dialogue in tqdm(enumerate(dialogues), desc="生成语音"):
            file_name = self.process_dialogue(i, dialogue)
            if file_name:
                file_names.append(file_name)
            else:
                logger.error(f"无法合成{i}的语音")
                return

        try:
            # 构建文件列表
            file_list = "|".join(file_names)

            # 使用ffmpeg合并音频文件
            subprocess.run(
                [
                    "ffmpeg",
                    "-y",
                    "-i",
                    f"concat:{file_list}",
                    "-acodec",
                    "copy",
                    self.output_file,
                ],
                check=True,
            )
        except subprocess.CalledProcessError as e:
            logger.error(f"FFmpeg执行失败: {e}")
        except Exception as e:
            logger.error(f"未知错误: {e}")
