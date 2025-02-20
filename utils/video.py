import gc
import math
import os
import random
import re
import subprocess
from typing import List, Tuple

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
    VideoFileClip,
    concatenate_videoclips,
    vfx,
)
from tqdm import tqdm

from utils.log import logger
from utils.schema import Dialogue, MaterialInfo, VideoConfig, VideoTranscript


async def find_split_index(current_line: str, font: str, fontsize: int, max_width: int) -> int:
    split_index = len(current_line)
    for i in range(len(current_line) - 1, 0, -1):
        temp_clip = TextClip(font, current_line[:i], font_size=fontsize, color="white")
        if temp_clip.size[0] <= max_width:
            split_index = i
            break
    return split_index


async def wrap_text_by_punctuation_and_width(text: str, max_width: int, font: str, fontsize: int) -> str:
    punctuation = r"[，。！？]"
    english_char = r"[a-zA-Z]"
    words = re.split(f"({punctuation})", text)

    lines = []
    current_line = ""

    for word in words:
        if re.match(punctuation, word):
            current_line += word
            continue

        current_line += word

        while current_line:
            temp_clip = TextClip(font, current_line, font_size=fontsize, color="white")
            if temp_clip.size[0] <= max_width:
                break
            else:
                split_index = await find_split_index(current_line, font, fontsize, max_width)
                lines.append(current_line[:split_index])
                current_line = current_line[split_index:]

                while current_line and re.match(punctuation, current_line[0]):
                    lines[-1] += current_line[0]
                    current_line = current_line[1:]

                if current_line and re.match(english_char, current_line[0]):
                    last_line = lines[-1]

                    i = len(last_line) - 1
                    while i >= 0 and re.match(english_char, last_line[i]):
                        i -= 1

                    if i > 0:
                        english_part = last_line[i + 1 :]
                        lines[-1] = last_line[: i + 1]
                        current_line = english_part + current_line

    if current_line:
        lines.append(current_line)

    return "\n".join(lines)


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
        "copy",
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


async def create_video_from_audio_and_image(
    audio: AudioFileClip,
    image: ImageClip,
    video_width: int,
    fps: int,
    offset: int = None,
    direction: int = None,
    step: int = 3,
) -> Tuple[VideoClip, int, int]:
    original_width = image.size[0]
    original_height = image.size[1]

    video_height = original_height

    frames = []
    offset = random.randint(0, original_width - video_width - 1) if offset is None else offset
    direction = random.choice([1, -1]) if direction is None else direction
    for _ in range(math.ceil(audio.duration * fps)):
        if offset >= original_width - video_width - 1:
            direction = -1
        elif offset <= 0:
            direction = 1

        offset += direction * step
        if offset < 0:
            offset = 0
        if offset > original_width - video_width:
            offset = original_width - video_width - 1
        frame = image.cropped(x1=offset, y1=0, x2=offset + video_width, y2=video_height)
        frame = frame.with_duration(1 / fps)
        frames.append(frame)

    video = concatenate_videoclips(frames, method="compose")
    video = video.with_duration(audio.duration)
    video = video.with_audio(audio)

    return video, offset, direction


async def create_video_by_images(
    image_files: List[str],
    data: VideoTranscript,
    folder: str,
    output_file: str,
    opening_audio: str,
    background_audio: str,
    fps: int = 24,
    font: str = None,
) -> VideoClip:

    async def process_dialogue(
        audio_file: str,
        content: str,
        font_size: int,
        position: int,
        offset: int,
        direction: int,
    ) -> Tuple[int, int, int]:
        audio = AudioFileClip(audio_file)

        text = await wrap_text_by_punctuation_and_width(content, subtitle_width, font, font_size)
        txt_clip = TextClip(
            font,
            text,
            font_size=font_size,
            color="white",
            stroke_color="black",
            stroke_width=1,
            text_align="center",
        )
        txt_clip = txt_clip.with_position(("center", position - txt_clip.size[1] // 2))

        video, offset, direction = await create_video_from_audio_and_image(
            audio, images[image_index], video_width, fps, offset, direction
        )

        video = video.with_start(duration_start)
        txt_clip = txt_clip.with_duration(video.duration).with_start(duration_start)

        videos.append(video)
        txt_clips.append(txt_clip)

        duration = video.duration

        del audio
        del txt_clip
        del video

        return duration, offset, direction

    images = [ImageClip(image_file) for image_file in image_files]

    image_width = images[0].size[0]
    video_width = int(image_width / 16 * 9)
    subtitle_width = int(video_width * 0.8)
    estimated_font_size = int(subtitle_width / 17)
    subtitle_position = int(images[0].size[1] * 2 / 3)

    title_font_size = int(subtitle_width / 16)
    title_position = int(images[0].size[1] / 2)

    title = data.topic
    dialogues = data.dialogues
    for i, dialogue in tqdm(enumerate(dialogues), desc="Creating video", total=len(dialogues)):
        video_file = os.path.join(folder, f"{i}.mp4")
        if os.path.exists(video_file):
            continue

        texts = dialogue.contents
        videos = []
        txt_clips = []
        offset = None
        direction = None
        duration_start = 0
        for j, text in enumerate(texts):
            text = text.replace("‘", "“").replace("’", "”").strip()
            image_index = i % len(image_files)

            if i == 0 and j == 0:
                audio_file = opening_audio
                duration, offset, direction = await process_dialogue(
                    audio_file,
                    title,
                    title_font_size,
                    title_position,
                    offset,
                    direction,
                )
                duration_start += duration

            audio_file = os.path.join(folder, f"{i}_{j}.mp3")
            duration, offset, direction = await process_dialogue(
                audio_file,
                text,
                estimated_font_size,
                subtitle_position,
                offset,
                direction,
            )
            duration_start += duration

        final_video = CompositeVideoClip(videos + txt_clips)

        try:
            final_video.write_videofile(video_file, codec="libx264", fps=fps)
        except Exception as e:
            logger.error(f"Error writing video file: {e}")
            if os.path.exists(video_file):
                os.remove(video_file)

        del final_video

        gc.collect()

    video_files = [f"{i}.mp4" for i in range(len(dialogues))]
    list_file = os.path.join(folder, "listfile.txt")
    await merge_videos(video_files, output_file, list_file, background_audio)

    gc.collect()

    return None


async def create_video_by_videos(
    videos: List[MaterialInfo],
    dialogues: List[Dialogue],
    folder: str,
    output_file: str,
    video_config: VideoConfig,
) -> VideoClip:
    subtitle_width = int(video_config.width * 0.8)
    font_size = int(subtitle_width / 16)
    subtitle_position = int(video_config.height * 2 / 3)

    for i, dialogue in tqdm(enumerate(dialogues), desc="Creating video", total=len(dialogues)):
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

            text = await wrap_text_by_punctuation_and_width(text, subtitle_width, video_config.font, font_size)
            txt_clip = TextClip(
                video_config.font,
                text,
                font_size=font_size,
                color="white",
                stroke_color="black",
                stroke_width=1,
                text_align="center",
            )
            txt_clip = txt_clip.with_position(("center", subtitle_position - txt_clip.size[1] // 2))

            video_sub = video.subclipped(duration_start, duration_start + audio.duration)
            video_sub = video_sub.with_audio(audio).with_start(duration_start)
            txt_clip = txt_clip.with_duration(audio.duration).with_start(duration_start)

            if i > 0 and j == 0:
                shuffle_side = random.choice(["left", "right", "top", "bottom"])
                transition_funcs = [
                    lambda c: c.with_effects([vfx.CrossFadeIn(0.5)]),
                    lambda c: c.with_effects([vfx.SlideIn(0.5, shuffle_side)]),
                    lambda c: c,
                ]
                shuffle_transition = random.choice(transition_funcs)
                video_sub = shuffle_transition(video_sub)

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

        del audio
        del video
        del final_videos
        del txt_clips
        del final_video

        gc.collect()

    video_files = [f"{i}.mp4" for i in range(len(dialogues))]
    list_file = os.path.join(folder, "listfile.txt")
    await merge_videos(video_files, output_file, list_file, video_config.background_audio)

    gc.collect()

    return None
