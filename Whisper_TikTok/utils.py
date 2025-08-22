import os
import json
import random
import datetime
import subprocess
from pathlib import Path
from typing import NamedTuple

class FFProbeResult(NamedTuple):
    """Represents the result of running FFprobe.

        Attributes:
            return_code (int): The return code of the FFprobe process.
            json (str): The JSON output from FFprobe.
            error (str): The error message from FFprobe, if any.
        """
    return_code: int
    json: str
    error: str


def random_background(folder: str = "background") -> str:
    """
    Returns the filename of a random file in the specified folder.

    Args:
        folder(str): The folder containing the files.

    Returns:
        str: The filename of a randomly selected file in the folder.
    """
    directory = Path(folder).absolute()
    os.makedirs(directory, exist_ok=True)

    files = list(directory.glob("*"))

    random_file = random.choice(files)
    return Path(random_file).absolute()


def get_ffprobe_result(filename: str) -> FFProbeResult:
    """Executes ffprobe on the given file and returns the result.

        Args:
            filename (str): The path to the file to be analyzed.

        Returns:
            FFProbeResult: An FFProbeResult object containing the return code,
                             JSON output, and error message from ffprobe.
        """
    command_array = ["ffprobe", "-v", "quiet", "-print_format", "json", "-show_format", "-show_streams", filename]
    result = subprocess.run(command_array, stdout=subprocess.PIPE, stderr=subprocess.PIPE, universal_newlines=True)
    return FFProbeResult(return_code=result.returncode, json=result.stdout, error=result.stderr)


def get_info(filename: str, kind: str) -> dict:
    """Extracts media information from a file using ffprobe.

        Args:
            filename (str): The path to the media file.
            kind (str): The type of media to extract information for ("video" or "audio").

        Returns:
            dict: A dictionary containing media information.
                For video, it returns {"width": width, "height": height, "duration": duration}.
                For audio, it returns {"duration": duration}.
                Returns an empty dictionary if the media kind is unknown.

        Raises:
            RuntimeError: If ffprobe fails to execute.
        """
    result = get_ffprobe_result(filename)
    if result.return_code != 0:
        raise RuntimeError(f"ffprobe failed with error: {result.error}")

    d = json.loads(result.json)

    if kind == "video":
        streams = d.get("streams", [])
        for stream in streams:
            if stream["codec_type"] == "video":
                video_stream = stream
                break

        duration = float(video_stream["duration"])
        width = int(video_stream["width"])
        height = int(video_stream["height"])

        return {"width": width, "height": height, "duration": duration}

    elif kind == "audio":
        streams = d.get("streams", [])
        for stream in streams:
            if stream["codec_type"] == "audio":
                audio_stream = stream
                break

        duration = float(audio_stream["duration"])

        return {"duration": duration}

    else:
        logger.warning(f"Unknown media kind: {kind}")
        return {}


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
        "00F0FF"
    """
    r, g, b = rgb[0:2], rgb[2:4], rgb[4:6]
    return b + g + r
