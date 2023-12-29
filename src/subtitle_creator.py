import os
from pathlib import Path
import stable_whisper as whisper
import torch


def srt_create(model, path: str, series: str, part: int, text: str, filename: str) -> bool:
    series = series.replace(' ', '_')

    srt_path = f"{path}{os.sep}{series}{os.sep}"
    srt_filename = f"{srt_path}{series}_{part}.srt"
    absolute_srt_path = Path(srt_filename).absolute()

    transcribe = model.transcribe(
        filename, regroup=True, fp16=torch.cuda.is_available())
    transcribe.split_by_gap(0.5).split_by_length(
        38).merge_by_gap(0.15, max_words=2)
    transcribe.to_srt_vtt(str(absolute_srt_path), word_level=True)

    return srt_filename


def highlight_words(srt_file: str, subtitle_format: str = "b", font_color: str = "#FFF000") -> bool:
    subtitle_format = subtitle_format.lower()

    if not font_color.startswith('#'):
        print(
            f"Invalid font color. Using default color: #FFF000")
        font_color = "#FFF000"
    else:
        font_color = font_color.upper()

    with open(srt_file, 'r', encoding='UTF-8') as f:
        content = f.read()

    content = content.replace(
        '<u>', f'<font color={font_color}><{subtitle_format}>')
    content = content.replace('</u>', f'</{subtitle_format}></font>')

    with open(srt_file, 'w', encoding='UTF-8') as f:
        f.write(content)

    print(
        f"Subtitle file formatted successfully")

    return True
