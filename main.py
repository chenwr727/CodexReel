import argparse
import asyncio
from typing import Optional

from api.schemas import TaskCreate
from services.video import VideoGenerator
from utils.log import logger


async def url2video(task_create: TaskCreate, doc_id: Optional[int] = None) -> Optional[str]:
    generator = VideoGenerator()
    return await generator.generate_video(task_create, doc_id)


async def main():
    parser = argparse.ArgumentParser(description="Process and convert text to speech from a given URL.")
    parser.add_argument("url", type=str, help="The URL of the content to process")
    parser.add_argument("--doc-id", type=int, help="Optional document ID", default=None)
    args = parser.parse_args()

    task_create = TaskCreate(name=args.url)
    result = await url2video(task_create, args.doc_id)

    if result:
        if result == "Script":
            logger.info("Script generation completed")
        else:
            logger.info("Video generation completed")
    else:
        logger.error("Failed to generate video")


if __name__ == "__main__":
    asyncio.run(main())
