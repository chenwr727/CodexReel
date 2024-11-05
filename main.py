import argparse
import json
import os

from utils.config import load_config
from utils.llm import LLmWriter
from utils.processing import extract_chapter_number, get_content
from utils.tts import TextToSpeechConverter
from utils.log import logger


def main(url: str):
    logger.info(f"开始处理{url}")
    chapter = extract_chapter_number(url)
    folder = f"./{chapter}"
    if not os.path.exists(folder):
        os.mkdir(folder)

    config = load_config()

    file_json = os.path.join(folder, f"{chapter}.json")
    if not os.path.exists(file_json):
        file_txt = os.path.join(folder, f"{chapter}.txt")

        if not os.path.exists(file_txt):
            logger.info("开始获取内容")
            text = get_content(url)
            if text:
                with open(file_txt, "w", encoding="utf-8") as f:
                    f.write(text)
            else:
                logger.error("获取内容失败")
                return
        else:
            logger.info("小说文件已存在")

        with open(file_txt, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info("开始生成播客")
        assistant = LLmWriter(
            config["llm"]["api_key"], config["llm"]["base_url"], config["llm"]["model"]
        )

        logger.info("第一次生成播客")
        text_writer = assistant.writer(content, config["llm"]["prompt_writer"])
        logger.info("第二次生成播客")
        text_rewriter = assistant.writer(text_writer, config["llm"]["prompt_rewriter"])
        text_json = json.loads(text_rewriter)
        with open(file_json, "w", encoding="utf-8") as f:
            json.dump(text_json, f, ensure_ascii=False, indent=4)
    else:
        logger.info("播客文件已存在")

    with open(file_json, "r", encoding="utf-8") as f:
        text_json = json.load(f)

    logger.info("开始生成语音")
    converter = TextToSpeechConverter(
        config["tts"]["api_key"],
        config["tts"]["model"],
        config["tts"]["voices"],
        chapter,
    )
    converter.text_to_speech(text_json)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and convert text to speech from a given URL."
    )
    parser.add_argument("url", type=str, help="The URL of the content to process")
    args = parser.parse_args()

    main(args.url)
