"""Module for creating subtitles from audio/video files using a Whisper model."""

from pathlib import Path


def srt_create(whisper_model, mp3_filename: Path, out_folder: Path, uuid: str, **kwargs) -> None:
    """Generates .srt and .ass subtitle files from an audio/video file using a Whisper model.

    Args:
        whisper_model: The Whisper model object used for transcription.
        mp3_filename (Path): The path to the audio file to transcribe.
        out_folder (Path): The base directory where the subtitles will be saved.
        uuid (str): The unique identifier for the video.
        **kwargs: Additional keyword arguments for customization.
            - font (str): The font name for the .ass file (default: "Arial").
            - sub_position (int): The position of the subtitles (default: 5, center-bottom).
            - font_size (int): The font size for the .ass file (default: 21).
            - font_color: The highlight color for the .ass file.
    """
    srt_filename = out_folder / f"{uuid}.srt"
    ass_filename = out_folder / f"{uuid}.ass"

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

    transcribe = whisper_model.transcribe(str(mp3_filename), regroup=True, fp16=True)
    transcribe.split_by_gap(0.5).split_by_length(38).merge_by_gap(0.15, max_words=2)
    transcribe.to_srt_vtt(str(srt_filename), word_level=True)
    transcribe.to_ass(
        str(ass_filename),
        word_level=True,
        highlight_color=kwargs.get("font_color"),
        **word_dict,
    )
