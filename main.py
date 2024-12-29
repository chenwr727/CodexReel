import argparse
import asyncio
import json
import os

from utils.config import load_config
from utils.image import ImageAssistant
from utils.llm import LLmWriter
from utils.log import logger
from utils.processing import get_content, parse_url
from utils.tts import TextToSpeechConverter
from utils.video import create_video


async def url2video(url: str):
    logger.info(f"开始处理{url}")
    dir_name = parse_url(url)
    folder = os.path.join("output", dir_name)
    if not os.path.exists(folder):
        os.makedirs(folder)

    config = load_config()

    file_json = os.path.join(folder, f"{dir_name}.json")
    file_txt = os.path.join(folder, f"{dir_name}.txt")
    assistant = LLmWriter(
        config["llm"]["api_key"], config["llm"]["base_url"], config["llm"]["model"]
    )

    if not os.path.exists(file_json):
        if not os.path.exists(file_txt):
            logger.info("开始获取内容")
            text = await get_content(url)
            if text:
                with open(file_txt, "w", encoding="utf-8") as f:
                    f.write(text)
            else:
                logger.error("获取内容失败")
                return
        else:
            logger.info("网页文件已存在")

        with open(file_txt, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info("开始生成播客")
        logger.info("第一次生成播客")
        text_writer = await assistant.writer(content, config["llm"]["prompt_writer"])
        logger.info("第二次生成播客")
        text_rewriter = await assistant.writer(
            text_writer, config["llm"]["prompt_rewriter"]
        )
        text_json = json.loads(text_rewriter)
        with open(file_json, "w", encoding="utf-8") as f:
            json.dump(text_json, f, ensure_ascii=False, indent=4)
    else:
        logger.info("播客文件已存在")

    with open(file_json, "r", encoding="utf-8") as f:
        text_json = json.load(f)

    logger.info("开始生成语音")
    output_file = os.path.join(folder, f"{dir_name}.mp3")
    if not os.path.exists(output_file):
        converter = TextToSpeechConverter(
            config["tts"]["api_key"],
            config["tts"]["model"],
            config["tts"]["voices"],
            folder,
        )
        await converter.text_to_speech(text_json["dialogues"], output_file)
    else:
        logger.info("语音文件已存在")

    logger.info("开始生成图片")
    prompt = ""
    file_prompt = os.path.join(folder, "prompt.txt")
    if os.path.exists(file_prompt):
        with open(file_prompt, "r", encoding="utf-8") as f:
            prompt = f.read()
    if not prompt:
        description = text_json["description"]
        assistant = LLmWriter(
            config["image"]["api_key"],
            config["image"]["base_url"],
            config["image"]["model_llm"],
        )
        prompt = await assistant.writer(description, config["image"]["prompt_image"])
        with open(file_prompt, "w", encoding="utf-8") as f:
            f.write(prompt)
    else:
        logger.info("图片提示已存在")
    logger.info(prompt)

    assistant = ImageAssistant(config["image"]["api_key"], folder)
    image_files = await assistant.generate_image(
        prompt,
        config["image"]["model"],
        config["image"]["image_num"],
        config["image"]["image_size"],
    )

    logger.info("开始生成视频")
    output_file = os.path.join(folder, f"{dir_name}.mp4")
    if not os.path.exists(output_file):
        await create_video(
            image_files,
            text_json,
            folder,
            output_file,
            config["video"]["opening_audio"],
            config["video"]["background_audio"],
            config["video"]["fps"],
            config["video"]["font"],
        )
    else:
        logger.info("视频文件已存在")
    if os.path.exists(output_file):
        return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Process and convert text to speech from a given URL."
    )
    parser.add_argument("url", type=str, help="The URL of the content to process")
    args = parser.parse_args()

    asyncio.run(url2video(args.url))
