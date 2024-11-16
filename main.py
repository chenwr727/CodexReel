import argparse
import json
import os

from utils.config import load_config
from utils.image import ImageAssistant
from utils.llm import LLmWriter
from utils.log import logger
from utils.processing import extract_chapter_number, get_content
from utils.tts import TextToSpeechConverter
from utils.video import create_video


def main(url: str):
    logger.info(f"开始处理{url}")
    chapter = extract_chapter_number(url)
    folder = f"./{chapter}"
    if not os.path.exists(folder):
        os.mkdir(folder)

    config = load_config()

    file_json = os.path.join(folder, f"{chapter}.json")
    file_txt = os.path.join(folder, f"{chapter}.txt")
    assistant = LLmWriter(
        config["llm"]["api_key"], config["llm"]["base_url"], config["llm"]["model"]
    )

    if not os.path.exists(file_json):
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
    output_file = f"{chapter}.mp3"
    if not os.path.exists(output_file):
        converter = TextToSpeechConverter(
            config["tts"]["api_key"],
            config["tts"]["model"],
            config["tts"]["voices"],
            chapter,
        )
        converter.text_to_speech(text_json, output_file)
    else:
        logger.info("语音文件已存在")

    logger.info("开始生成图片")
    file_prompt = os.path.join(folder, f"prompt.txt")
    if os.path.exists(file_prompt):
        logger.info("图片提示已存在")
        with open(file_prompt, "r", encoding="utf-8") as f:
            prompt = f.read()
    else:
        with open(file_txt, "r", encoding="utf-8") as f:
            content = f.readlines()[1]
        chapter_name = content.strip().split(" ")[-1]
        prompt = assistant.writer(chapter_name, config["image"]["prompt_image"])
        with open(file_prompt, "w", encoding="utf-8") as f:
            f.write(prompt)
    logger.info(prompt)

    assistant = ImageAssistant(config["llm"]["api_key"], chapter)
    image_files = assistant.generate_image(
        prompt,
        config["image"]["image_num"],
        config["image"]["image_size"],
    )

    logger.info("开始生成视频")
    output_file = f"{chapter}.mp4"
    if not os.path.exists(output_file):
        create_video(image_files, text_json, chapter, output_file)
    else:
        logger.info("视频文件已存在")


if __name__ == "__main__":
    # parser = argparse.ArgumentParser(
    #     description="Process and convert text to speech from a given URL."
    # )
    # parser.add_argument("url", type=str, help="The URL of the content to process")
    # args = parser.parse_args()

    # main(args.url)

    url = "https://www.jinyongwang.net/tian/644.html"
    main(url)
