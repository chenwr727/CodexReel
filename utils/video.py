import gc
import math
import os
import random
import re
import subprocess

from tqdm import tqdm

from utils.log import logger

os.environ["IMAGEMAGICK_BINARY"] = (
    r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
)

from moviepy import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
    concatenate_videoclips,
)


def wrap_text_by_punctuation_and_width(
    text: str, max_width: int, font: str, fontsize: int
) -> str:
    punctuation = r"[，。！？]"
    english_char = r"[a-zA-Z]"
    words = re.split(f"({punctuation})", text)

    lines = []
    current_line = ""

    for word in words:
        if re.match(punctuation, word):
            current_line += word
            continue

        temp_line = current_line + word
        temp_clip = TextClip(font, temp_line, font_size=fontsize, color="white")

        if temp_clip.size[0] <= max_width:
            current_line = temp_line
        else:
            split_index = len(temp_line)
            for i in range(len(temp_line) - 1, 0, -1):
                temp_clip = TextClip(
                    font, temp_line[:i], font_size=fontsize, color="white"
                )
                if temp_clip.size[0] <= max_width:
                    split_index = i
                    break

            lines.append(temp_line[:split_index])
            current_line = temp_line[split_index:]

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


def create_filelist(input_files: list[str], list_file: str):
    with open(list_file, "w") as f:
        for file in input_files:
            f.write(f"file '{file}'\n")


def merge_videos(input_files: list[str], output_file: str, list_file: str):
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
        "-c",
        "copy",
        output_file,
    ]

    try:
        subprocess.run(command, check=True)
        logger.info(f"视频文件合并成功，输出文件：{output_file}")
    except subprocess.CalledProcessError as e:
        logger.error(f"FFmpeg 执行失败: {e}")
    except Exception as e:
        logger.error(f"未知错误: {e}")


def create_video_from_audio_and_image(
    audio: AudioFileClip,
    image: ImageClip,
    video_width: int,
    fps: int,
    offset: int = None,
    direction: int = None,
    step: int = 1,
) -> VideoClip:
    original_width = image.size[0]
    original_height = image.size[1]

    video_height = original_height

    frames = []
    offset = (
        random.randint(0, original_width - video_width - 1)
        if offset is None
        else offset
    )
    direction = random.choice([1, -1]) if direction is None else direction
    for _ in range(math.ceil(audio.duration * fps)):
        if offset >= original_width - video_width:
            direction = -1
        elif offset <= 0:
            direction = 1

        offset += direction * step
        frame = image.cropped(x1=offset, y1=0, x2=offset + video_width, y2=video_height)
        frame = frame.with_duration(1 / fps)
        frames.append(frame)

    video = concatenate_videoclips(frames, method="compose")
    video = video.with_duration(audio.duration)
    video = video.with_audio(audio)

    return video, offset, direction


def create_video(
    image_files: list[str],
    dialogues: list[dict],
    floder: str,
    output_file: str,
    fps: int = 24,
    font: str = None,
) -> VideoClip:
    images = [ImageClip(image_file) for image_file in image_files]

    image_width = images[0].size[0]
    video_width = int(image_width / 16 * 9)
    subtitle_width = int(video_width * 0.8)
    estimated_font_size = int(subtitle_width / 16)
    subtitle_position = int(images[0].size[1] * 2 / 3)

    for i, dialogue in tqdm(
        enumerate(dialogues), desc="Creating video", total=len(dialogues)
    ):
        video_file = os.path.join(floder, f"{i}.mp4")
        if os.path.exists(video_file):
            continue

        texts = dialogue["contents"]
        videos = []
        txt_clips = []
        offset = None
        direction = None
        duration_start = 0
        for j, text in enumerate(texts):
            audio_file = os.path.join(floder, f"{i}_{j}.mp3")
            audio = AudioFileClip(audio_file)

            text = wrap_text_by_punctuation_and_width(
                text, subtitle_width, font, estimated_font_size
            )
            txt_clip = TextClip(
                font,
                text,
                font_size=estimated_font_size,
                color="white",
                stroke_color="black",
                stroke_width=1,
                text_align="center",
            )
            txt_clip = txt_clip.with_position(
                ("center", subtitle_position - txt_clip.size[1] // 2)
            )

            image_index = i % len(image_files)
            video, offset, direction = create_video_from_audio_and_image(
                audio, images[image_index], video_width, fps, offset, direction
            )

            video = video.with_start(duration_start)
            txt_clip = txt_clip.with_duration(video.duration).with_start(duration_start)

            videos.append(video)
            txt_clips.append(txt_clip)

            duration_start += video.duration

        final_video = CompositeVideoClip(videos + txt_clips)

        try:
            final_video.write_videofile(video_file, codec="libx264", fps=fps)
        except Exception as e:
            logger.error(f"Error writing video file: {e}")
            if os.path.exists(video_file):
                os.remove(video_file)

        del audio
        del txt_clip
        del video
        del final_video

        gc.collect()

    video_files = [f"{i}.mp4" for i in range(len(dialogues))]
    list_file = os.path.join(floder, "listfile.txt")
    merge_videos(video_files, output_file, list_file)

    gc.collect()

    return None
