import os
from pathlib import Path


def srt_create(
    whisper_model, path: str, series: str, part: int, filename: str, **kwargs
) -> bool:
    """Generates .srt and .ass subtitle files from an audio/video file using a Whisper model.

    Args:
        whisper_model: The Whisper model object used for transcription.
        path (str): The base directory where the subtitles will be saved.
        series (str): The name of the series or project. Spaces will be replaced with underscores.
        part (int): The part number of the video.
        filename (str): The path to the audio/video file to transcribe.
        **kwargs: Additional keyword arguments for customization.
            - font (str): The font name for the .ass file (default: "Arial").
            - sub_position (int): The alignment/position of the subtitles (default: 5, center-bottom).
            - font_size (int): The font size for the .ass file (default: 21).
            - font_color: The highlight color for the .ass file.

    Returns:
        bool: The filename of the generated .ass file.
    """
    series = series.replace(" ", "_")

    srt_path = f"{path}{os.sep}{series}{os.sep}"
    srt_filename = f"{srt_path}{series}_{part}.srt"
    ass_filename = f"{srt_path}{series}_{part}.ass"

    absolute_srt_path = Path(srt_filename).absolute()
    absolute_ass_path = Path(ass_filename).absolute()

    absolute_srt_path.parent.mkdir(parents=True, exist_ok=True)
    absolute_ass_path.parent.mkdir(parents=True, exist_ok=True)

    word_dict = {
        "Fontname": kwargs.get("font", "Lexend Bold"),
        "Alignment": kwargs.get("sub_position", 5),
        "BorderStyle": "1",
        "Outline": "1",
        "Shadow": "2",
        "Blur": "21",
        "Fontsize": kwargs.get("font_size", 21),
        "MarginL": "0",
        "MarginR": "0",
    }

    transcribe = whisper_model.transcribe(filename, regroup=True, fp16=True)
    transcribe.split_by_gap(0.5).split_by_length(38).merge_by_gap(0.15, max_words=2)
    transcribe.to_srt_vtt(str(absolute_srt_path), word_level=True)
    transcribe.to_ass(
        str(absolute_ass_path),
        word_level=True,
        highlight_color=kwargs.get("font_color"),
        **word_dict,
    )
    return ass_filename
