import os
from pathlib import Path
import random
import sys
import ffmpeg

from rich.console import Console

import msg

console = Console()


def rich_print(text, style: str = ""):
    console.print(text, style=style)


def random_background(folder: str = "background") -> Path:
    """
    Returns the filename of a random file in the specified folder.

    Args:
        folder(str): The folder containing the files.

    Returns:
        Path: The absolute path of the random file.
    """
    # Get the absolute path of the folder
    directory = Path(folder).absolute()

    # Create the folder if it does not exist
    if not directory.exists():
        directory.mkdir()

    # Select a random background video for the clip inside the folder
    random_file = random.choice(os.listdir(directory))

    # Return the absolute path of the random file adding the folder path
    # Concat the folder path with the random file name
    return directory / random_file

def get_info(filename: str, kind: str):
    global probe

    try:
        probe = ffmpeg.probe(filename)
    except ffmpeg.Error as e:
        console.log(f"{msg.ERROR}{e.stderr}")
        sys.exit(1)

    if kind == 'video':
        global video_stream

        # Extract
        for stream in probe['streams']:
            if stream['codec_type'] == 'video':
                video_stream = stream
                break

        duration = float(video_stream['duration'])
        width = int(video_stream['width'])
        height = int(video_stream['height'])

        return {'width': width, 'height': height, 'duration': duration}

    elif kind == 'audio':
        global audio_stream

        # Extract
        for stream in probe['streams']:
            if stream['codec_type'] == 'audio':
                audio_stream = stream
                break

        duration = float(audio_stream['duration'])

        return {'duration': duration}


def convert_time(time_in_seconds):
    """
    Converts time in seconds to a string in the format "hh:mm:ss.mmm".

    Args:
        time_in_seconds (float): The time in seconds to be converted.

    Returns:
        str: The time in the format "hh:mm:ss.mmm".
    """
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"


def rgb_to_bgr(rgb: str) -> str:
    """
    Converts a color from RGB to BGR.

    Args:
        rgb (str): The color in RGB format.

    Returns:
        str: The color in BGR format.

    Example:
        >>> rgb_to_bgr("FFF000")
        "000FFF"
    """

    return rgb[4:6] + rgb[2:4] + rgb[0:2]
