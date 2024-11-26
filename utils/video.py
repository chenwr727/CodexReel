import gc
import math
import os
import random

from tqdm import tqdm

from utils.log import logger

os.environ["IMAGEMAGICK_BINARY"] = (
    r"C:\Program Files\ImageMagick-7.1.1-Q16-HDRI\magick.exe"
)

from moviepy.editor import (
    AudioFileClip,
    CompositeVideoClip,
    ImageClip,
    TextClip,
    VideoClip,
    VideoFileClip,
    concatenate_videoclips,
)


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
        frame = image.crop(x1=offset, y1=0, x2=offset + video_width, y2=video_height)
        frame = frame.set_duration(1 / fps)
        frames.append(frame)

    video = concatenate_videoclips(frames, method="compose")
    video = video.set_audio(audio)

    return video, offset, direction


def create_video(
    image_files: list[str],
    dialogues: list[dict],
    audio_directory: str,
    output_file: str,
    fps: int = 24,
) -> VideoClip:
    images = [ImageClip(image_file) for image_file in image_files]

    image_width = images[0].size[0]
    video_width = int(image_width / 16 * 9)
    subtitle_width = video_width * 0.8
    estimated_font_size = int(subtitle_width / 16)
    subtitle_position = int(images[0].size[1] * 2 / 3)

    for i, dialogue in tqdm(
        enumerate(dialogues), desc="Creating video", total=len(dialogues)
    ):
        video_file = f"{audio_directory}/{i}.mp4"
        if os.path.exists(video_file):
            continue

        texts = dialogue["contents"]
        videos = []
        txt_clips = []
        offset = None
        direction = None
        duration_start = 0
        for j, text in enumerate(texts):
            audio_file = os.path.join(audio_directory, f"{i}_{j}.mp3")
            audio = AudioFileClip(audio_file)

            txt_clip = TextClip(
                text,
                fontsize=estimated_font_size,
                color="white",
                stroke_color="black",
                size=(subtitle_width, None),
                font="Microsoft-YaHei-Bold-&-Microsoft-YaHei-UI-Bold",
                align="center",
                method="caption",
            )
            txt_clip = txt_clip.set_position(
                ("center", subtitle_position - txt_clip.size[1] // 2)
            )

            image_index = i % len(image_files)
            video, offset, direction = create_video_from_audio_and_image(
                audio, images[image_index], video_width, fps, offset, direction
            )

            txt_clip = txt_clip.set_duration(video.duration).set_start(duration_start)
            video = video.set_start(duration_start)

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

    video_files = [f"{audio_directory}/{i}.mp4" for i in range(len(dialogues))]
    videos = [VideoFileClip(video_file) for video_file in video_files]
    final_video = concatenate_videoclips(videos)
    final_video.write_videofile(output_file, codec="libx264", fps=fps)

    del videos
    del final_video

    gc.collect()

    return None
