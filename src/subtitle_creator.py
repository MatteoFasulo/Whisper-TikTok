import os
from pathlib import Path
import stable_whisper as whisper
import torch


def srt_create(model, path: str, series: str, part: int, text: str, filename: str, font_color: str) -> bool:
    series = series.replace(' ', '_')

    srt_path = f"{path}{os.sep}{series}{os.sep}"
    srt_filename = f"{srt_path}{series}_{part}.srt"
    ass_filename = f"{srt_path}{series}_{part}.ass"

    absolute_srt_path = Path(srt_filename).absolute()
    absolute_ass_path = Path(ass_filename).absolute()

    word_dict = {
        'Fontname': 'Lexend Bold',
        'Alignment': '5',
        'BorderStyle': '1',
        'Outline': '1',
        'Shadow': '2',
        'Blur': '21',
        'Fontsize': '20',
        'MarginL': '0',
        'MarginR': '0',
    }

    transcribe = model.transcribe(
        filename, regroup=True, fp16=torch.cuda.is_available())
    transcribe.split_by_gap(0.5).split_by_length(
        38).merge_by_gap(0.15, max_words=2)
    transcribe.to_srt_vtt(str(absolute_srt_path), word_level=True)
    transcribe.to_ass(str(absolute_ass_path), word_level=True,
                      karaoke=True, highlight_color=font_color, **word_dict)
    return ass_filename
