from typing import List

import aiohttp
from async_lru import alru_cache

from schemas.video import MaterialInfo
from utils.log import logger

from .base import MaterialHelper


class PixabayHelper(MaterialHelper):
    def __init__(
        self,
        api_key: str,
        lang: str,
        video_type: str,
        minimum_duration: int,
        video_width: int,
        video_height: int,
        max_page: int = 3,
    ):
        super().__init__(api_key, minimum_duration, video_width, video_height, max_page)

        self.lang = lang
        self.video_type = video_type
        self.url = "https://pixabay.com/api/videos/"

    def _filter_video_items(self, videos: List[dict]) -> List[MaterialInfo]:
        video_items = []
        for v in videos:
            duration = v["duration"]
            if duration < self.minimum_duration:
                continue
            video_files: dict = v["videos"]
            h_diff = float("inf")
            item = None
            for _, video in video_files.items():
                w = video["width"]
                h = video["height"]
                # if not math.isclose(w / h, self.video_width / self.video_height, rel_tol=1e-5):
                #     break
                if w < self.video_width or h < self.video_height:
                    continue
                if h - self.video_height < h_diff:
                    h_diff = h - self.video_height
                    item = MaterialInfo(url=video["url"], duration=duration)
                    if h_diff == 0:
                        break
            if item:
                video_items.append(item)
        return video_items

    @alru_cache()
    async def search_videos(self, search_term: str, page: int, per_page: int = 20) -> List[MaterialInfo]:
        params = {
            "key": self.api_key,
            "q": search_term,
            "lang": self.lang,
            "video_type": self.video_type,
            "min_width": self.video_width,
            "min_height": self.video_height,
            "safesearch": "true",
            "page": page,
            "per_page": per_page,
        }

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.url, params=params, headers=self.headers, timeout=aiohttp.ClientTimeout(total=60)
                ) as r:
                    response = await r.json()
                    if "hits" not in response:
                        logger.error(f"search videos failed: {response}")
                        return []
                    return self._filter_video_items(response["hits"])
        except Exception as e:
            logger.error(f"search videos failed: {str(e)}")
            return []
