import os
from http import HTTPStatus
from typing import List

import dashscope
import requests
from dashscope import ImageSynthesis

from utils.log import logger


class ImageAssistant:
    def __init__(self, api_key: str, chapter: str):
        self.chapter = chapter
        dashscope.api_key = api_key

    async def generate_image(self, prompt: str, model: str, n: int = 2, size: str = "1024*1024") -> List[str]:
        for i in range(n):
            file_name = os.path.join(self.chapter, f"{i}.png")
            if not os.path.exists(file_name):
                break
        else:
            return [os.path.join(self.chapter, f"{i}.png") for i in range(n)]

        file_names = []
        rsp = ImageSynthesis.call(model=model, prompt=prompt, n=n, size=size)
        if rsp.status_code == HTTPStatus.OK:
            for i, result in enumerate(rsp.output.results):
                file_name = os.path.join(self.chapter, f"{i}.png")
                with open(file_name, "wb+") as f:
                    f.write(requests.get(result.url).content)
                file_names.append(file_name)
        else:
            logger.error("Failed, status_code: %s, code: %s, message: %s" % (rsp.status_code, rsp.code, rsp.message))
        return file_names
