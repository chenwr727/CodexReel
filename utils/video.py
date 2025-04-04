import os
import random
import subprocess
from typing import List

from moviepy import AudioFileClip, CompositeVideoClip, VideoClip, VideoFileClip, vfx

from schemas.config import VideoConfig
from schemas.video import MaterialInfo, VideoTranscript
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
        "[1:a]volume=0.2[v1];[0:a][v1]amerge=inputs=2[a]",
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
        logger.info("Video created successfully.")
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
    probabilities = [0.4, 0.4, 0.2]
    shuffle_transition = random.choices(transition_funcs, probabilities, k=1)[0]
    return shuffle_transition(video)


def resize_video(video: VideoFileClip, video_width: int, video_height: int) -> VideoClip:
    if video.size[0] / video.size[1] != video_width / video_height:
        target_aspect_ratio = video_width / video_height
        video_aspect_ratio = video.size[0] / video.size[1]

        if video_aspect_ratio > target_aspect_ratio:
            new_width = int(video.size[1] * target_aspect_ratio)
            crop_x = (video.size[0] - new_width) // 2
            video = video.cropped(x1=crop_x, x2=crop_x + new_width, y1=0, y2=video.size[1])
        else:
            new_height = int(video.size[0] / target_aspect_ratio)
            crop_y = (video.size[1] - new_height) // 2
            video = video.cropped(x1=0, x2=video.size[0], y1=crop_y, y2=crop_y + new_height)

    if video.size[0] != video_width:
        video = video.resized((video_width, video_height))
    return video


def formatter_text(text: str) -> str:
    text = text.replace("‘", "“").replace("’", "”").strip()
    return text


async def create_video(
    videos: List[MaterialInfo],
    video_transcript: VideoTranscript,
    folder: str,
    output_file: str,
    video_config: VideoConfig,
) -> VideoClip:
    logger.info("Creating video...")

    title = video_transcript.title
    video_files = []
    for i, paragraph in enumerate(video_transcript.paragraphs, start=1):
        logger.info(f"Processing paragraph {i}/{len(video_transcript.paragraphs)}")

        base_name = f"{i}.mp4"
        video_file = os.path.join(folder, base_name)
        video_files.append(base_name)
        if os.path.exists(video_file):
            continue
        video = VideoFileClip(videos[i - 1].video_path).without_audio()
        video = resize_video(video, video_config.width, video_config.height)
        final_videos = []
        txt_clips = []
        duration_start = 0

        dialogues = paragraph.dialogues
        for j, dialogue in enumerate(dialogues, start=1):
            logger.info(f"Processing dialogue {j}/{len(dialogues)}")

            texts = dialogue.contents

            for k, text in enumerate(texts, start=1):
                if i == 1 and j == 1 and k == 1:
                    duration_delta = video_config.title.duration
                    title = formatter_text(title)
                    txt_clip = await create_subtitle(title, video_config.width, video_config.height, video_config.title)
                    txt_clip = txt_clip.with_duration(duration_delta).with_start(duration_start)
                    txt_clips.append(txt_clip)
                else:
                    duration_delta = video_config.subtitle.interval

                audio_file = os.path.join(folder, f"{i}_{j}_{k}.mp3")
                audio = AudioFileClip(audio_file)

                text = formatter_text(text)
                txt_clip = await create_subtitle(text, video_config.width, video_config.height, video_config.subtitle)
                txt_clip = txt_clip.with_duration(audio.duration).with_start(duration_start + duration_delta)
                txt_clips.append(txt_clip)

                video_sub = video.subclipped(duration_start, duration_start + duration_delta + audio.duration)
                video_sub = video_sub.with_audio(audio.with_start(duration_delta)).with_start(duration_start)
                if i > 1 and j == 1 and k == 1:
                    video_sub = transition_video(video_sub)
                final_videos.append(video_sub)

                duration_start += video_sub.duration

        final_video = CompositeVideoClip(final_videos + txt_clips)

        try:
            final_video.write_videofile(
                video_file, codec="libx264", fps=video_config.fps, temp_audiofile_path=folder, threads=4
            )
        except Exception as e:
            logger.error(f"Error writing video file: {e}")
            if os.path.exists(video_file):
                os.remove(video_file)
            raise e

    logger.info("Merging videos...")
    list_file = os.path.join(folder, "listfile.txt")
    await merge_videos(video_files, output_file, list_file, video_config.background_audio)

    return None
