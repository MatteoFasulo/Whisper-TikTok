import datetime
import os
from pathlib import Path
import random
import sys
import ffmpeg

from rich.console import Console

import msg
from src.logger import setup_logger


console = Console()
logger = setup_logger()


class KeepDir:
    def __init__(self):
        self.original_dir = os.getcwd()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_dir)

    def chdir(self, path):
        os.chdir(path)


def rich_print(text, style: str = ""):
    console.print(text, style=style)


def random_background(folder: str = "background") -> str:
    """
    Returns the filename of a random file in the specified folder.

    Args:
        folder(str): The folder containing the files.

    Returns:
        str: The filename of a randomly selected file in the folder.
    """
    directory = Path(folder).absolute()
    if not directory.exists():
        directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        files = os.listdir(".")
        random_file = random.choice(files)
        return Path(random_file).absolute()


def get_info(filename: str, verbose: bool = False):
    """
    Get information about a video file.

    Args:
        filename (str): The path to the video file.
        verbose (bool, optional): Whether to print verbose output. Defaults to False.

    Returns:
        dict: A dictionary containing information about the video file, including width, height, bit rate, and duration.
    """
    try:
        probe = ffmpeg.probe(filename)
        video_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
        audio_stream = next(
            (stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
        try:
            duration = float(audio_stream['duration'])
        except Exception:
            if verbose:
                console.log(
                    f"{msg.WARNING}MP4 default metadata not found")
                logger.warning('MP4 default metadata not found')
            duration = (datetime.datetime.strptime(
                audio_stream['DURATION'], '%H:%M:%S.%f') - datetime.datetime.min).total_seconds()
        if video_stream is None:
            if verbose:
                console.log(
                    f"{msg.WARNING}No video stream found")
                logger.warning('No video stream found')
            bit_rate = int(audio_stream['bit_rate'])
            return {'bit_rate': bit_rate, 'duration': duration}

        width = int(video_stream['width'])
        height = int(video_stream['height'])
        return {'width': width, 'height': height, 'duration': duration}

    except ffmpeg.Error as e:
        console.log(f"{msg.ERROR}{e.stderr}")
        logger.exception(e.stderr)
        sys.exit(1)


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
