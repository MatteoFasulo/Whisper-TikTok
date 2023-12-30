import os
from pathlib import Path
import torch


def srt_create(whisper_model, path: str, series: str, part: int, text: str, filename: str, **kwargs) -> bool:
    series = series.replace(' ', '_')

    srt_path = f"{path}{os.sep}{series}{os.sep}"
    srt_filename = f"{srt_path}{series}_{part}.srt"
    ass_filename = f"{srt_path}{series}_{part}.ass"

    absolute_srt_path = Path(srt_filename).absolute()
    absolute_ass_path = Path(ass_filename).absolute()

    word_dict = {
        'Fontname': kwargs.get('font', 'Arial'),
        'Alignment': kwargs.get('sub_position', 5),
        'BorderStyle': '1',
        'Outline': '1',
        'Shadow': '2',
        'Blur': '21',
        'Fontsize': kwargs.get('font_size', 21),
        'MarginL': '0',
        'MarginR': '0',
    }

    transcribe = whisper_model.transcribe(
        filename, regroup=True, fp16=torch.cuda.is_available())
    transcribe.split_by_gap(0.5).split_by_length(
        38).merge_by_gap(0.15, max_words=2)
    transcribe.to_srt_vtt(str(absolute_srt_path), word_level=True)
    transcribe.to_ass(str(absolute_ass_path), word_level=True,
                      highlight_color=kwargs.get('font_color'), **word_dict)
    return ass_filename
