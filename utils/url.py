import asyncio
import os

import requests
from bs4 import BeautifulSoup

from fake_useragent import UserAgent

from utils.log import logger


async def fetch_url(url: str, max_retries: int = 5, retry_delay: int = 3):
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


async def parse_response(response: requests.Response):
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text().strip()
    return content


async def get_content(url: str, max_retries: int = 3, retry_delay: int = 2):
    response = await fetch_url(url, max_retries, retry_delay)
    if response is None:
        return ""
    return await parse_response(response)


def parse_url(url: str, doc_id: int = None, output_folder: str = "output"):
    if doc_id:
        dir_name = f"{doc_id:04}"
    else:
        dir_name = url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?", "_")

    folder = os.path.join(output_folder, dir_name)
    if not os.path.exists(folder):
        os.makedirs(folder)
    return folder, dir_name
