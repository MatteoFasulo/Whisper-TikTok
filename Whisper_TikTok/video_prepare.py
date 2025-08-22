import os
from pathlib import Path
import subprocess
import random

from .utils import get_info, convert_time

HOME = Path.cwd()


def prepare_background(
    background_mp4: str, filename_mp3: str, filename_srt: str, verbose: bool = False
) -> str:
    """Prepares a background video by overlaying audio and subtitles.

    This function takes a background video, an audio file, and a subtitle file as input.
    It randomly selects a starting point in the background video, crops and scales the video,
    applies a gaussian blur, overlays the subtitles, and combines it with the audio.

    Args:
        background_mp4 (str): Path to the background video file (MP4).
        filename_mp3 (str): Path to the audio file (MP3).
        filename_srt (str): Path to the subtitle file (SRT).
        verbose (bool, optional): If True, prints verbose output. Defaults to False.

    Returns:
        str: Path to the output video file (MP4).
    """
    video_info = get_info(background_mp4, kind="video")
    video_duration = int(round(video_info.get("duration"), 0))

    audio_info = get_info(filename_mp3, kind="audio")
    audio_duration = int(round(audio_info.get("duration"), 0))

    ss = random.randint(0, (video_duration - audio_duration))
    audio_duration = convert_time(audio_duration)
    if ss < 0:
        ss = 0

    srt_filename = filename_srt.name
    srt_path = filename_srt.parent.absolute()

    directory = HOME / "output"
    os.makedirs(directory, exist_ok=True)

    outfile = directory / f"output_{ss}.mp4"

    if verbose:
        print(f"{filename_srt = }\n{background_mp4 = }\n{filename_mp3 = }\n")

    args = [
        "ffmpeg",
        "-ss",
        str(ss),
        "-t",
        str(audio_duration),
        "-i",
        background_mp4,
        "-i",
        filename_mp3,
        "-map",
        "0:v",
        "-map",
        "1:a",
        "-filter:v",
        f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=lanczos, gblur=sigma=2, ass={srt_filename}",
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
        f"{outfile}",
        "-y",
        "-threads",
        f"{os.cpu_count() // 2}",
    ]

    if verbose:
        print("[i] FFMPEG Command:\n" + " ".join(args) + "\n")

    subprocess.Popen(args, cwd=srt_path).wait()

    return outfile
