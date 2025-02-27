import hashlib
import os
import time
from abc import ABC, abstractmethod
from typing import List, Optional

import aiohttp
from fake_useragent import UserAgent
from moviepy import VideoFileClip

from schemas.video import MaterialInfo
from utils.log import logger


class MaterialHelper(ABC):
    def __init__(self, api_key: str, minimum_duration: int, video_width: int, video_height: int, max_page: int = 3):
        self.api_key = api_key
        self.minimum_duration = minimum_duration
        self.video_width = video_width
        self.video_height = video_height
        self.max_page = max_page
        self.headers = {"User-Agent": UserAgent().random}

    def _find_closest_video(
        self, video_items: List[MaterialInfo], audio_length: float, urls: set[str]
    ) -> Optional[MaterialInfo]:
        closest_video = None
        min_diff = float("inf")

        for video in video_items:
            if video.url in urls:
                continue
            if video.duration > audio_length:
                diff = video.duration - audio_length
                if diff < min_diff:
                    min_diff = diff
                    closest_video = video

        return closest_video

    @abstractmethod
    def _filter_video_items(self, videos: List[dict]) -> List[MaterialInfo]:
        pass

    @abstractmethod
    async def search_videos(self, search_term: str, page: int) -> List[MaterialInfo]:
        pass

    async def get_videos(self, audio_lengths: List[float], search_terms_list: List[List[str]]) -> List[MaterialInfo]:
        urls = set()
        videos: List[MaterialInfo] = []
        for search_terms, audio_length in zip(search_terms_list, audio_lengths):
            logger.info(f"Searching videos for {search_terms}")
            for page in range(1, self.max_page + 1):
                logger.info(f"Searching videos on page {page}")
                for search_term in search_terms:
                    logger.info(f"Searching videos on {search_term}")
                    video_items = await self.search_videos(search_term, page)
                    time.sleep(1)
                    closest_video = self._find_closest_video(video_items, audio_length, urls)
                    if closest_video:
                        urls.add(closest_video.url)
                        videos.append(closest_video)
                        break
                else:
                    continue
                break
            else:
                raise ValueError("No video found")
        for video in videos:
            video_url = video.url
            video_path = await self.save_video(video_url)
            if video_path:
                video.video_path = video_path
        return videos

    async def save_video(self, video_url: str, save_dir: str = "./cache_videos") -> str:
        if not os.path.exists(save_dir):
            os.makedirs(save_dir)

        url_without_query = video_url.split("?")[0]
        url_hash = hashlib.md5(url_without_query.encode("utf-8")).hexdigest()
        video_id = f"vid-{url_hash}"
        video_path = f"{save_dir}/{video_id}.mp4"

        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            logger.info(f"video already exists: {video_path}")
            return video_path

        logger.info(f"downloading video: {video_url}")
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(video_url, headers=self.headers, timeout=aiohttp.ClientTimeout(total=240)) as r:
                    with open(video_path, "wb") as f:
                        f.write(await r.read())

            if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
                try:
                    clip = VideoFileClip(video_path)
                    duration = clip.duration
                    fps = clip.fps
                    clip.close()
                    if duration > 0 and fps > 0:
                        return video_path
                except Exception as e:
                    logger.warning(f"invalid video file: {video_path} => {str(e)}")
                    os.remove(video_path)
        except Exception as e:
            logger.error(f"download video failed: {str(e)}")
            if os.path.exists(video_path):
                os.remove(video_path)

        return ""
