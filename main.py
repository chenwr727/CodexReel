import argparse
import asyncio
import json
import os
import re

from utils import config
from utils.llm import LLmWriter
from utils.log import logger
from utils.pexels import PexelsHelper
from utils.schema import VideoTranscript
from utils.tts import TextToSpeechConverter
from utils.url import get_content, parse_url
from utils.video import create_video_by_videos


async def url2video(url: str, doc_id: int = None):
    logger.info(f"Start {url}")
    folder, dir_name = parse_url(url, doc_id)

    file_json = os.path.join(folder, f"{dir_name}.json")
    file_txt = os.path.join(folder, f"{dir_name}.txt")
    assistant = LLmWriter(config.llm.api_key, config.llm.base_url, config.llm.model)

    if not os.path.exists(file_json):
        if not os.path.exists(file_txt):
            if url.startswith("http"):
                logger.info("Starting to fetch content from URL")
                text = await get_content(url)
                if not text:
                    logger.error("Failed to fetch content from URL")
                    return
            else:
                text = url
            with open(file_txt, "w", encoding="utf-8") as f:
                f.write(text)
        else:
            logger.info("File already exists.")

        with open(file_txt, "r", encoding="utf-8") as f:
            content = f.read()

        logger.info("Start to generate video transcript")
        logger.info("Generating first draft...")
        text_writer = await assistant.writer(
            f"文章内容：\n{content}",
            config.llm.prompt_writer,
            response_format={"type": "json_object"},
        )
        if text_writer is None:
            logger.error("Failed to generate first draft.")
            return None
        logger.info("Reflecting...")
        text_reflector = await assistant.writer(
            f"文章内容：\n{content}\n\n初稿文案：\n{text_writer}",
            config.llm.prompt_reflector,
            response_format={"type": "json_object"},
        )
        if text_reflector is None:
            logger.error("Reflector failed")
            return None
        logger.info("Optimizing...")
        text_rewriter = await assistant.writer(
            f"文章内容：\n{content}\n\n初稿文案：\n{text_writer}\n\n反思建议：\n{text_reflector}",
            config.llm.prompt_rewriter,
            response_format={"type": "json_object"},
        )
        if text_rewriter is None:
            logger.error("Rewriter failed")
            return None

        json_pattern = r"(\{.*\s?\})"
        matches = re.findall(json_pattern, text_rewriter, flags=re.DOTALL)
        if matches:
            text_rewriter = matches[0]
        else:
            logger.error("Error: No JSON object found in the response.")
            return

        text_json = json.loads(text_rewriter)
        with open(file_json, "w", encoding="utf-8") as f:
            json.dump(text_json, f, ensure_ascii=False, indent=4)
        return
    else:
        logger.info("File already exists.")

    with open(file_json, "r", encoding="utf-8") as f:
        text_json = json.load(f)
    video_transcript = VideoTranscript.model_validate(text_json)

    logger.info("Start to generate audios...")
    file_durations = os.path.join(folder, "durations.json")
    durations = []
    if os.path.exists(file_durations):
        with open(file_durations, "r", encoding="utf-8") as f:
            durations = json.load(f)
    if not durations:
        converter = TextToSpeechConverter(
            config.tts.api_key,
            config.tts.model,
            config.tts.voices,
            folder,
        )
        durations = await converter.text_to_speech(video_transcript.dialogues)
        with open(file_durations, "w", encoding="utf-8") as f:
            json.dump(durations, f, ensure_ascii=False)

    logger.info("Start to download videos...")
    videos = []
    file_videos = os.path.join(folder, "videos.json")
    if os.path.exists(file_videos):
        with open(file_videos, "r", encoding="utf-8") as f:
            videos = json.load(f)
    if not videos:
        search_terms = []
        file_terms = os.path.join(folder, "terms.json")
        if os.path.exists(file_terms):
            with open(file_terms, "r", encoding="utf-8") as f:
                search_terms = json.load(f)
        if not search_terms:
            content = await assistant.writer(
                video_transcript.model_dump_json(),
                config.pexels.prompt,
                response_format={"type": "json_object"},
            )
            json_pattern = r"(\[.*\s?\])"
            matches = re.findall(json_pattern, content, flags=re.DOTALL)
            if not matches:
                logger.error("Error parsing JSON: No valid JSON found in the response.")
                return
            search_terms = json.loads(matches[0])
            with open(file_terms, "w", encoding="utf-8") as f:
                json.dump(search_terms, f, ensure_ascii=False)
        pexels_helper = PexelsHelper(
            config.pexels.api_key, config.video.width, config.video.height, config.pexels.minimum_duration
        )
        videos = pexels_helper.get_videos(durations, search_terms)
        with open(file_videos, "w", encoding="utf-8") as f:
            json.dump([video.model_dump() for video in videos], f, ensure_ascii=False, indent=4)

    logger.info("Start Creating Video")
    output_file = os.path.join(folder, f"{dir_name}.mp4")
    if not os.path.exists(output_file):
        await create_video_by_videos(videos, video_transcript.dialogues, folder, output_file, config.video)
    else:
        logger.info("File already exists.")
    if os.path.exists(output_file):
        return output_file


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Process and convert text to speech from a given URL.")
    parser.add_argument("url", type=str, help="The URL of the content to process")
    args = parser.parse_args()

    asyncio.run(url2video(args.url))
