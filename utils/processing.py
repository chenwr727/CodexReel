import os
import re
import time

import requests
from bs4 import BeautifulSoup

from utils.log import logger

USER_AGENT = "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/58.0.3029.110 Safari/537.3"


def fetch_url(url, max_retries=5, retry_delay=3):
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


def parse_response(response):
    """
    解析响应内容，提取标题和内容。
    """
    soup = BeautifulSoup(response.content, "html.parser")

    # text_content = soup.get_text()
    # text_content = text_content.replace('\n', ' ').replace('\r', '')
    # return text_content

    breadnav_span = soup.find("span", id="breadnav")
    if breadnav_span:
        a_tags = breadnav_span.find_all("a")
        if a_tags:
            title = "《" + a_tags[-1].text.strip() + "》"
        else:
            title = ""
    else:
        title = ""

    mbtitle = soup.find("div", class_="mbtitle")
    if mbtitle:
        mbtitle = mbtitle.text.replace("\u3000", " ")
    else:
        mbtitle = ""

    content = soup.find("div", id="vcon")
    if content:
        content = content.text.strip()
    else:
        content = ""

    return f"{title}\n{mbtitle}\n{content}"


def get_content(url, max_retries=3, retry_delay=2):
    """
    获取并解析URL内容。
    """
    response = fetch_url(url, max_retries, retry_delay)
    if response is None:
        return ""
    return parse_response(response)


def extract_chapter_number(url):
    """
    从URL中提取章节编号。
    """
    # 使用正则表达式匹配URL中的章节编号
    match = re.search(r"/(\d+)\.html$", url)
    if match:
        return match.group(1)
    else:
        return None


if __name__ == "__main__":
    url = "https://www.jinyongwang.net/tian/644.html"
    file_name = f"{extract_chapter_number(url)}.txt"

    if not os.path.exists(file_name):
        text = get_content(url)
        with open(file_name, "w", encoding="utf-8") as f:
            f.write(text)
