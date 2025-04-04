import json
import os
import re
from dataclasses import dataclass
from typing import Any, Dict, List, Optional

from api.schemas import TaskCreate
from schemas.config import MaterialSource, TTSSource
from schemas.video import MaterialInfo, VideoTranscript
from services.llm import LLmWriter
from utils.config import config, get_prompt_config
from utils.log import logger
from utils.text import split_content_with_punctuation
from utils.url import get_content, parse_url
from utils.video import create_video


@dataclass
class ProcessingFiles:
    """Class to manage file paths for video processing."""

    folder: str

    def __post_init__(self):
        """Initialize all file paths after instance creation."""
        self.script = os.path.join(self.folder, "_transcript.json")
        self.html = os.path.join(self.folder, "_html.txt")
        self.draft = os.path.join(self.folder, "_transcript.txt")
        self.durations = os.path.join(self.folder, "_durations.json")
        self.videos = os.path.join(self.folder, "_videos.json")
        self.terms = os.path.join(self.folder, "_terms.json")
        self.output = os.path.join(self.folder, "_output.mp4")


class VideoGenerator:
    def __init__(self):
        self.config = config
        self.assistant = LLmWriter(config.llm.api_key, config.llm.base_url, config.llm.model)

    async def _get_content_from_source(self, url: str, files: ProcessingFiles) -> Optional[str]:
        """Fetch or read content from URL or direct text."""
        logger.info("Starting to fetch content")
        if os.path.exists(files.html):
            logger.info("Content file already exists, reading from file")
            return self._read_file(files.html)

        if url.startswith("http"):
            logger.info("Starting to fetch content from URL")
            content = await get_content(url)
            if not content:
                logger.error("Failed to fetch content from URL")
                return None
        else:
            content = url

        self._write_file(files.html, content)
        return content

    async def _generate_transcript(self, content: str, files: ProcessingFiles) -> Optional[str]:
        """Generate first transcript."""
        logger.info("Starting to generate transcrip")
        if os.path.exists(files.draft):
            logger.info("transcript file already exists")
            return self._read_file(files.draft)

        text_writer = await self.assistant.writer(content, self.config.prompt.prompt_writer)
        if text_writer:
            self._write_file(files.draft, text_writer)
            return text_writer
        return None

    async def _generate_final_transcript(self, transcript: str) -> Optional[Dict[str, Any]]:
        """Generate final video transcript."""
        logger.info("Starting to generate final transcript")
        text_rewriter = await self.assistant.writer(
            transcript,
            self.config.prompt.prompt_rewriter,
            response_format={"type": "json_object"},
        )
        if not text_rewriter:
            return None

        json_match = re.search(r"(\{.*\s?\})", text_rewriter, re.DOTALL)
        if not json_match:
            logger.error("No JSON object found in response")
            return None

        return json.loads(json_match.group(1))

    async def _convert_to_transcript(
        self, transcript_data: Dict[str, str | List[Dict[str, str | List[Dict[str, str]]]]]
    ) -> VideoTranscript:
        """Convert transcript data to VideoTranscript"""
        for paragraph in transcript_data["paragraphs"]:
            for dialogue in paragraph["dialogues"]:
                content = dialogue.pop("content")
                dialogue["contents"] = split_content_with_punctuation(content)
        video_transcript = VideoTranscript.model_validate(transcript_data)
        return video_transcript

    async def _process_audio(
        self, video_transcript: VideoTranscript, files: ProcessingFiles, tts_source: Optional[str] = None
    ) -> List[float]:
        """Process audio for the video."""
        logger.info("Starting to process audio")
        if os.path.exists(files.durations):
            return json.loads(self._read_file(files.durations))

        tts_source = tts_source or self.config.tts.source
        if tts_source == TTSSource.dashscope:
            from services.tts import DashscopeTextToSpeechConverter

            converter = DashscopeTextToSpeechConverter(
                self.config.tts.dashscope.api_key,
                self.config.tts.dashscope.model,
                self.config.tts.dashscope.voices,
                files.folder,
            )
        elif tts_source == TTSSource.edge:
            from services.tts import EdgeTextToSpeechConverter

            converter = EdgeTextToSpeechConverter(self.config.tts.edge.voices, files.folder)
        elif tts_source == TTSSource.hailuo:
            from services.tts import HaiLuoTextToSpeechConverter

            converter = HaiLuoTextToSpeechConverter(
                self.config.tts.hailuo.api_key,
                self.config.tts.hailuo.base_url,
                self.config.tts.hailuo.voices,
                files.folder,
            )
        elif tts_source == TTSSource.kokoro:
            from services.tts import KokoroTextToSpeechConverter

            converter = KokoroTextToSpeechConverter(
                self.config.tts.kokoro.config,
                self.config.tts.kokoro.model,
                self.config.tts.kokoro.lang_code,
                self.config.tts.kokoro.voices,
                files.folder,
            )
        else:
            raise ValueError("Invalid TTS source")
        durations = await converter.text_to_speech(video_transcript.paragraphs)
        self._write_json(files.durations, durations)
        return durations

    async def _process_videos(
        self,
        video_transcript: VideoTranscript,
        durations: List[float],
        files: ProcessingFiles,
        material_source: Optional[str] = None,
    ) -> List[MaterialInfo]:
        """Process videos for the final output."""
        logger.info("Starting to process videos")
        if os.path.exists(files.videos):
            datas = json.loads(self._read_file(files.videos))
            return [MaterialInfo.model_validate(data) for data in datas]

        search_terms = await self._get_search_terms(video_transcript, files)

        material_source = material_source or self.config.material.source
        if material_source == MaterialSource.pexels:
            from services.material import PexelsHelper

            material_helper = PexelsHelper(
                self.config.material.pexels.api_key,
                self.config.material.pexels.locale,
                self.config.material.minimum_duration,
                self.config.video.width,
                self.config.video.height,
            )
        elif material_source == MaterialSource.pixabay:
            from services.material import PixabayHelper

            material_helper = PixabayHelper(
                self.config.material.pixabay.api_key,
                self.config.material.pixabay.lang,
                self.config.material.pixabay.video_type,
                self.config.material.minimum_duration,
                self.config.video.width,
                self.config.video.height,
            )
        else:
            raise ValueError("Invalid material source")
        videos = await material_helper.get_videos(durations, search_terms)
        self._write_json(files.videos, [video.model_dump() for video in videos])
        return videos

    async def _get_search_terms(
        self, video_transcript: VideoTranscript, files: ProcessingFiles, max_retries: int = 3
    ) -> List[str]:
        """Get search terms for video content."""
        logger.info("Starting to get search terms")
        if os.path.exists(files.terms):
            return json.loads(self._read_file(files.terms))

        content_list = []
        i = 0
        for paragraph in video_transcript.paragraphs:
            dialogues = paragraph.dialogues
            contents = []
            for dialogue in dialogues:
                contents.extend(dialogue.contents)
            content_list.append({"id": i + 1, "content": "\n".join(contents)})

        for i in range(max_retries):
            logger.debug(f"Trying to get search terms {i+1}/{max_retries}")
            content = await self.assistant.writer(
                str(content_list), self.config.material.prompt, response_format={"type": "json_object"}
            )
            json_match = re.search(r"(\[.*\s?\])", content, re.DOTALL)
            if not json_match:
                logger.warning("No valid JSON found in search terms response")
                continue
            results = json.loads(json_match.group(1))
            if len(results) != len(content_list):
                logger.warning("Number of search terms does not match number of dialogues")
            try:
                search_terms = [result["search_terms"] for result in results]
                break
            except KeyError:
                logger.warning("Invalid search terms response")
                continue
        else:
            raise ValueError("Number of search terms does not match number of dialogues")
        self._write_json(files.terms, search_terms)
        return search_terms

    @staticmethod
    def _read_file(filepath: str) -> str:
        """Read content from a file."""
        with open(filepath, "r", encoding="utf-8") as f:
            return f.read()

    @staticmethod
    def _write_file(filepath: str, content: str) -> None:
        """Write content to a file."""
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)

    @staticmethod
    def _write_json(filepath: str, content: Any) -> None:
        """Write JSON content to a file."""
        with open(filepath, "w", encoding="utf-8") as f:
            json.dump(content, f, ensure_ascii=False, indent=4)

    async def generate_video(self, task_create: TaskCreate, doc_id: Optional[int] = None) -> Optional[str]:
        """Main method to generate video from URL or text content."""
        try:
            url = task_create.name
            logger.info(f"Starting video generation for {url}")
            folder = parse_url(url, doc_id)
            files = ProcessingFiles(folder)

            # Early return if output already exists
            if os.path.exists(files.output):
                logger.info("Output video already exists")
                return files.output

            # Process content and generate transcript
            if not os.path.exists(files.script):
                self.config.prompt = get_prompt_config(task_create.prompt_source)

                content = await self._get_content_from_source(url, files)
                if not content:
                    raise ValueError("Failed to fetch content from source")

                transcript = await self._generate_transcript(content, files)
                if not transcript:
                    raise ValueError("Failed to generate transcript")

                final_transcript = await self._generate_final_transcript(transcript)
                if not final_transcript:
                    raise ValueError("Failed to generate final transcript")

                self._write_json(files.script, final_transcript)
                logger.info("Video script generation completed")
                return "Script"

            # Load transcript and process
            transcript_data = json.loads(self._read_file(files.script))
            video_transcript = await self._convert_to_transcript(transcript_data)

            # Generate audio and video
            durations = await self._process_audio(video_transcript, files, task_create.tts_source)
            videos = await self._process_videos(video_transcript, durations, files, task_create.material_source)

            # Create final video
            await create_video(videos, video_transcript, files.folder, files.output, self.config.video)

            return files.output if os.path.exists(files.output) else None

        except Exception as e:
            logger.error(f"Error in video generation: {str(e)}")
            raise e
