import math
from typing import List

import aiohttp
from async_lru import alru_cache

from schemas.video import MaterialInfo
from utils.log import logger

from .base import MaterialHelper


class PexelsHelper(MaterialHelper):
    def __init__(
        self, api_key: str, locale: str, minimum_duration: int, video_width: int, video_height: int, max_page: int = 3
    ):
        super().__init__(api_key, minimum_duration, video_width, video_height, max_page)

        self.locale = locale
        if video_width < video_height:
            video_orientation = "portrait"
        elif video_width > video_height:
            video_orientation = "landscape"
        else:
            video_orientation = "square"
        self.video_orientation = video_orientation
        self.url = "https://api.pexels.com/videos/search"

    def _filter_video_items(self, videos: List[dict]) -> List[MaterialInfo]:
        video_items = []
        for v in videos:
            duration = v["duration"]
            if duration < self.minimum_duration:
                continue
            w = v["width"]
            h = v["height"]
            if w < self.video_width or h < self.video_height:
                continue
            if not math.isclose(w / h, self.video_width / self.video_height, rel_tol=1e-5):
                continue
            video_files = v["video_files"]
            w_diff = float("inf")
            item = None
            for video in video_files:
                w = video["width"]
                h = video["height"]
                if w < self.video_width or h < self.video_height:
                    continue
                if w - self.video_width < w_diff:
                    w_diff = w - self.video_width
                    item = MaterialInfo(url=video["link"], duration=duration)
                    if w_diff == 0:
                        break
            if item:
                video_items.append(item)
        return video_items

    @alru_cache()
    async def search_videos(self, search_term: str, page: int, per_page: int = 80) -> List[MaterialInfo]:
        params = {"query": search_term, "orientation": self.video_orientation, "page": page, "per_page": per_page}
        if self.locale:
            params["locale"] = self.locale
        headers = self.headers.copy()
        headers.update({"Authorization": self.api_key})

        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                    self.url, params=params, headers=headers, timeout=aiohttp.ClientTimeout(total=60)
                ) as r:
                    response = await r.json()
                    if "videos" not in response:
                        logger.error(f"search videos failed: {response}")
                        return []
                    return self._filter_video_items(response["videos"])
        except Exception as e:
            logger.error(f"search videos failed: {str(e)}")
            return []
