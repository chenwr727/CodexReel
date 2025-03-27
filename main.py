import argparse
import asyncio
from typing import Optional

from services.video import VideoGenerator
from utils.log import logger


async def url2video(url: str, doc_id: Optional[int] = None, copywriter_type: Optional[str] = None) -> Optional[str]:
    generator = VideoGenerator()
    return await generator.generate_video(url, doc_id, copywriter_type)


async def main():
    parser = argparse.ArgumentParser(description="Process and convert text to speech from a given URL.")
    parser.add_argument("url", type=str, help="The URL of the content to process")
    parser.add_argument("--doc-id", type=int, help="Optional document ID", default=None)
    args = parser.parse_args()

    result = await url2video(args.url, args.doc_id)

    if result:
        if result == "Script":
            logger.info("Script generation completed")
        else:
            logger.info("Video generation completed")
    else:
        logger.error("Failed to generate video")


if __name__ == "__main__":
    asyncio.run(main())
