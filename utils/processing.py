import time

import requests
from bs4 import BeautifulSoup

from utils.log import logger

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


def fetch_url(url: str, max_retries: int = 5, retry_delay: int = 3):
    """
    尝试获取URL内容，支持重试机制。
    """
    retries = 0
    while retries < max_retries:
        try:
            response = requests.get(
                url,
                headers={"User-Agent": USER_AGENT},
                timeout=10,
            )
            response.raise_for_status()
            return response
        except requests.ConnectionError as ce:
            logger.error(f"连接错误: {ce}")
        except requests.Timeout as te:
            logger.error(f"请求超时: {te}")
        except requests.RequestException as e:
            logger.error(f"请求出错: {e}")
            return None
        retries += 1
        if retries < max_retries:
            logger.warning(f"尝试重新连接 ({retries}/{max_retries})...")
            time.sleep(retry_delay)
    logger.error("达到最大重试次数，请求失败。")
    return None


def parse_response(response: requests.Response):
    """
    解析响应内容，提取标题和内容。
    """
    soup = BeautifulSoup(response.content, "html.parser")
    content = soup.get_text().strip()
    return content


def get_content(url: str, max_retries: int = 3, retry_delay: int = 2):
    """
    获取并解析URL内容。
    """
    response = fetch_url(url, max_retries, retry_delay)
    if response is None:
        return ""
    return parse_response(response)


def parse_url(url: str):
    return url.replace("http://", "").replace("https://", "").replace("/", "_").replace("?", "_")
