"""Module for preparing video files by adding background video and audio."""

import os
from pathlib import Path
import subprocess
import random

from .utils import get_info, convert_time

HOME = Path.cwd()


def prepare_background(
    mp4_background_filename: Path, mp3_filename: Path, ass_filename: Path, out_folder: Path, uuid: str
) -> Path:
    """Prepares a background video by overlaying audio and subtitles.

    This function takes a background video, an audio file, and a subtitle file as input.
    It randomly selects a starting point in the background video, crops and scales the video,
    applies a gaussian blur, overlays the subtitles, and combines it with the audio.

    Args:
        mp4_background_filename (Path): Path to the background video file (MP4).
        mp3_filename (Path): Path to the audio file (MP3).
        ass_filename (Path): Path to the subtitle file (ASS).
        out_folder (Path): Path to the output folder.
        uuid (str): UUID for the output file naming.

    Returns:
        Path: Path to the output video file (MP4).
    """
    video_info = get_info(str(mp4_background_filename), kind="video")
    video_duration = int(round(video_info.get("duration", 0), 0))

    audio_info = get_info(str(mp3_filename), kind="audio")
    audio_duration = int(round(audio_info.get("duration", 0), 0))

    ss = random.randint(0, (video_duration - audio_duration))
    audio_duration = convert_time(audio_duration)
    ss = max(ss, 0)

    outfile = out_folder / f"{uuid}.mp4"

    args = [
        "ffmpeg",
        "-ss",
        str(ss),
        "-t",
        str(audio_duration),
        "-i",
        str(mp4_background_filename),
        "-i",
        str(mp3_filename),
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-filter:v",
        f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=lanczos, gblur=sigma=2, ass={str(ass_filename)}",
        "-c:v",
        "libx264",
        "-crf",
        "23",
        "-c:a",
        "aac",
        "-ac",
        "2",
        "-b:a",
        "192K",
        f"{str(outfile)}",
        "-y",
        "-threads",
        f"{os.cpu_count()}",
    ]

    with subprocess.Popen(args, cwd=str(out_folder)) as process:
        process.wait()

    return outfile
