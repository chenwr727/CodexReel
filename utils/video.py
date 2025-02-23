import gc
import os
import random
import subprocess
from typing import List

from moviepy import AudioFileClip, CompositeVideoClip, VideoClip, VideoFileClip, vfx

from schemas.config import VideoConfig
from schemas.video import Dialogue, MaterialInfo
from utils.log import logger
from utils.subtitle import create_subtitle


def create_filelist(input_files: List[str], list_file: str):
    with open(list_file, "w") as f:
        for file in input_files:
            f.write(f"file '{file}'\n")


async def merge_videos(
    input_files: List[str],
    output_file: str,
    list_file: str,
    background_audio: str,
):
    create_filelist(input_files, list_file)

    command = [
        "ffmpeg",
        "-y",
        "-f",
        "concat",
        "-safe",
        "0",
        "-i",
        list_file,
        "-stream_loop",
        "-1",
        "-i",
        background_audio,
        "-filter_complex",
        "[1:a]volume=0.3[v1];[0:a][v1]amerge=inputs=2[a]",
        "-map",
        "0:v",
        "-map",
        "[a]",
        "-c:v",
        "libx264",
        "-c:a",
        "aac",
        "-shortest",
        output_file,
    ]

    try:
        subprocess.run(command, check=True)
        logger.info(f"Video created successfully.")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFMPEG error: {e}")
    except Exception as e:
        logger.error(f"Error creating video: {e}")


def transition_video(video: VideoClip) -> VideoClip:
    shuffle_side = random.choice(["left", "right", "top", "bottom"])
    transition_funcs = [
        lambda c: c.with_effects([vfx.CrossFadeIn(0.5)]),
        lambda c: c.with_effects([vfx.SlideIn(0.5, shuffle_side)]),
        lambda c: c,
    ]
    shuffle_transition = random.choice(transition_funcs)
    return shuffle_transition(video)


async def create_video(
    videos: List[MaterialInfo], dialogues: List[Dialogue], folder: str, output_file: str, video_config: VideoConfig
) -> VideoClip:
    logger.info("Creating video...")
    subtitle_width = int(video_config.width * 0.8)
    font_size = int(subtitle_width / 16)
    subtitle_position = int(video_config.height * 2 / 3)

    total = len(dialogues)
    for i, dialogue in enumerate(dialogues):
        logger.info(f"Creating video {i+1}/{total}")
        video_file = os.path.join(folder, f"{i}.mp4")
        if os.path.exists(video_file):
            continue

        texts = dialogue.contents
        video = VideoFileClip(videos[i].video_path).without_audio()
        if video.size[0] != video_config.width:
            video = video.resized((video_config.width, video_config.height))
        final_videos = []
        txt_clips = []
        duration_start = 0

        for j, text in enumerate(texts):
            text = text.replace("‘", "“").replace("’", "”").strip()

            audio_file = os.path.join(folder, f"{i}_{j}.mp3")
            audio = AudioFileClip(audio_file)

            txt_clip = await create_subtitle(text, subtitle_position, subtitle_width, video_config.font, font_size)

            video_sub = video.subclipped(duration_start, duration_start + audio.duration)
            video_sub = video_sub.with_audio(audio).with_start(duration_start)
            txt_clip = txt_clip.with_duration(audio.duration).with_start(duration_start)

            if i > 0 and j == 0:
                video_sub = transition_video(video_sub)

            final_videos.append(video_sub)
            txt_clips.append(txt_clip)
            duration_start += audio.duration

        final_video = CompositeVideoClip(final_videos + txt_clips)

        try:
            final_video.write_videofile(video_file, codec="libx264", fps=video_config.fps, threads=4)
        except Exception as e:
            logger.error(f"Error writing video file: {e}")
            if os.path.exists(video_file):
                os.remove(video_file)
            raise e

        del audio
        del video
        del final_videos
        del txt_clips
        del final_video

        gc.collect()

    logger.info("Merging videos...")
    video_files = [f"{i}.mp4" for i in range(len(dialogues))]
    list_file = os.path.join(folder, "listfile.txt")
    await merge_videos(video_files, output_file, list_file, video_config.background_audio)

    gc.collect()

    return None
