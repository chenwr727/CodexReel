import bisect
import hashlib
import math
import os
from typing import List

import requests
from fake_useragent import UserAgent
from moviepy import VideoFileClip

from utils.log import logger
from utils.schema import MaterialInfo


def match_audio_to_video(audio_lengths, video_lengths):
    audio_with_index = [(length, idx) for idx, length in enumerate(audio_lengths)]
    video_with_index = [(length, idx) for idx, length in enumerate(video_lengths)]

    audio_with_index.sort()
    video_with_index.sort()

    matched_videos = []

    for audio_length, audio_idx in audio_with_index:
        idx = bisect.bisect_right(video_with_index, (audio_length, float("inf")))

        if idx < len(video_with_index):
            _, video_idx = video_with_index[idx]
            matched_videos.append((audio_idx, video_idx))
            video_with_index.pop(idx)
        else:
            return []

    matched_videos.sort(key=lambda x: x[0])

    return [idx for _, idx in matched_videos]


class PexelsHelper:
    def __init__(self, api_key, video_width: int, video_height: int, minimum_duration: int, max_page: int = 3):
        self.api_key = api_key
        self.video_width = video_width
        self.video_height = video_height
        self.minimum_duration = minimum_duration

        if video_width < video_height:
            video_orientation = "portrait"
        elif video_width > video_height:
            video_orientation = "landscape"
        else:
            video_orientation = "square"
        self.video_orientation = video_orientation

        self.max_page = max_page
        self.headers = {"User-Agent": UserAgent().random}
        self.url = "https://api.pexels.com/videos/search"

    def get_videos(self, audio_lengths: List[float], search_terms: List[str]) -> List[MaterialInfo]:
        urls = set()
        videos: List[MaterialInfo] = []
        matches = []
        for page in range(1, self.max_page + 1):
            logger.info(f"Searching videos on page {page}")
            for search_term in search_terms:
                logger.info(f"Searching videos on {search_term}")
                video_items = self.search_videos(search_term, page)
                for video_item in video_items:
                    if video_item.url not in urls:
                        urls.add(video_item.url)
                        videos.append(video_item)

                        if len(videos) >= len(audio_lengths):
                            video_lengths = [video.duration for video in videos]
                            matches = match_audio_to_video(audio_lengths, video_lengths)
                            if matches:
                                break
                else:
                    continue
                break
            else:
                continue
            break
        videos = [videos[idx] for idx in matches]
        for video in videos:
            video_url = video.url
            video_path = self.save_video(video_url)
            if video_path:
                video.video_path = video_path
        return videos

    def search_videos(self, search_term: str, page: int) -> List[MaterialInfo]:
        params = {"query": search_term, "orientation": self.video_orientation, "per_page": 20, page: page}
        headers = self.headers.copy()
        headers.update({"Authorization": self.api_key})

        try:
            r = requests.get(self.url, params=params, headers=headers, timeout=(30, 60))
            response = r.json()
            video_items = []
            if "videos" not in response:
                logger.error(f"search videos failed: {response}")
                return video_items
            videos = response["videos"]
            for v in videos:
                duration = v["duration"]
                if duration < self.minimum_duration:
                    continue
                video_files = v["video_files"]
                for video in video_files:
                    w = int(video["width"])
                    h = int(video["height"])
                    if (
                        w >= self.video_width
                        and h >= self.video_height
                        and math.isclose(w / h, self.video_width / self.video_height, rel_tol=1e-9)
                    ):
                        item = MaterialInfo(url=video["link"], duration=duration)
                        video_items.append(item)
                        break
            return video_items
        except Exception as e:
            logger.error(f"search videos failed: {str(e)}")

        return []

    def save_video(self, video_url: str, save_dir: str = "./cache_videos") -> str:
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
        with open(video_path, "wb") as f:
            f.write(requests.get(video_url, headers=self.headers, timeout=(60, 240)).content)

        if os.path.exists(video_path) and os.path.getsize(video_path) > 0:
            try:
                clip = VideoFileClip(video_path)
                duration = clip.duration
                fps = clip.fps
                clip.close()
                if duration > 0 and fps > 0:
                    return video_path
            except Exception as e:
                try:
                    os.remove(video_path)
                except Exception:
                    pass
                logger.warning(f"invalid video file: {video_path} => {str(e)}")
        return ""
