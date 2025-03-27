import asyncio
import base64
import json
import os
import re
from typing import Optional

import requests
from bs4 import BeautifulSoup
from Crypto.Cipher import AES
from Crypto.Util.Padding import unpad
from fake_useragent import UserAgent

from utils.log import logger


async def fetch_url(url: str, max_retries: int = 5, retry_delay: int = 3) -> Optional[requests.Response]:
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(url, headers={"User-Agent": UserAgent().random}, timeout=10)
            response.raise_for_status()
            return response
        except requests.ConnectionError as ce:
            logger.error(f"ConnectionError: {ce}")
        except requests.Timeout as te:
            logger.error(f"Timeout: {te}")
        except requests.RequestException as e:
            logger.error(f"Error: {e}")
            return None
        retries += 1
        if retries < max_retries:
            logger.warning(f"Request failed. Retrying ({retries}/{max_retries})...")
            await asyncio.sleep(retry_delay)
    logger.error("Maximum retries reached.")
    return None


async def parse_response(response: requests.Response) -> str:
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text().strip()
    return content


async def decode_36kr_text(text: str, key: str = "efabccee-b754-4c") -> str:
    match = re.search(r"window\.initialState=(\{.*\})", text)
    if not match:
        logger.error("Failed to parse 36kr text.")
        return ""
    try:
        res = json.loads(match.group(1))
        raw_state: str = res["state"]
        aes = AES.new(key.encode("utf-8"), AES.MODE_ECB)
        padded_text = aes.decrypt(base64.b64decode(raw_state.encode("utf-8")))
        res = str(unpad(padded_text, AES.block_size), encoding="utf-8")
        res_json = json.loads(res)
        if "article" in res_json:
            data = res_json["article"]["detail"]["data"]
        else:
            data = res_json["articleDetail"]["articleDetailData"]["data"]
        return json.dumps(data, ensure_ascii=False)
    except Exception as e:
        logger.error(f"Failed to decode 36kr text: {e}")
        return ""


async def get_content(url: str, max_retries: int = 3, retry_delay: int = 2) -> str:
    response = await fetch_url(url, max_retries, retry_delay)
    if response is None:
        return ""

    content = await parse_response(response)

    if url.startswith("https://36kr.com/p/"):
        content += "\n" + await decode_36kr_text(response.text)

    return content


def parse_url(url: str, doc_id: int = None, output_folder: str = "output") -> str:
    if doc_id:
        dir_name = f"{doc_id:04}"
    else:
        dir_name = url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?", "_")

    folder = os.path.join(output_folder, dir_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder
