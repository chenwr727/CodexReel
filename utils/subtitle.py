import re

from moviepy import TextClip

from schemas.config import SubtitleConfig


async def find_split_index(current_line: str, font: str, font_size: int, max_width: int) -> int:
    split_index = len(current_line)
    for i in range(len(current_line) - 1, 0, -1):
        temp_clip = TextClip(font, current_line[:i], font_size=font_size)
        if temp_clip.size[0] <= max_width:
            split_index = i
            break
    return split_index


async def wrap_text_by_punctuation_and_width(text: str, max_width: int, font: str, font_size: int) -> TextClip:
    punctuation = r"[，。！？；”]"
    english_char = r"[a-zA-Z]"
    words = re.split(f"({punctuation})", text)

    lines = []
    current_line = ""

    for word in words:
        if word == "":
            continue
        if re.match(punctuation, word):
            current_line += word
            continue

        current_line += word

        while current_line:
            temp_clip = TextClip(font, current_line, font_size=font_size)
            if temp_clip.size[0] <= max_width:
                break
            else:
                split_index = await find_split_index(current_line, font, font_size, max_width)
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


async def create_subtitle(
    text: str,
    video_width: int,
    video_height: int,
    subtitle_config: SubtitleConfig,
) -> TextClip:
    subtitle_width = int(video_width * subtitle_config.width_ratio)
    font_size = int(subtitle_width / subtitle_config.font_size_ratio)
    subtitle_position = int(video_height * subtitle_config.position_ratio)

    text = await wrap_text_by_punctuation_and_width(text, subtitle_width, subtitle_config.font, font_size)
    txt_clip = TextClip(
        subtitle_config.font,
        text,
        font_size=font_size,
        color=subtitle_config.color,
        stroke_color=subtitle_config.stroke_color,
        stroke_width=subtitle_config.stroke_width,
        text_align=subtitle_config.text_align,
    )
    txt_clip = txt_clip.with_position(("center", subtitle_position - txt_clip.size[1] // 2))
    return txt_clip
