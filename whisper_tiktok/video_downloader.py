"""Module for downloading videos using yt-dlp from YouTube."""

import subprocess
from pathlib import Path

HOME = Path.cwd()


def download_video(url: str, folder: str = "background", timeout: int = 600) -> tuple[bool, str | Path]:
    """
    Downloads a video from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the video to download.
        folder (str, optional): The name of the folder to save the video in. Defaults to "background".
        timeout (int, optional): The timeout for the download process in seconds. Defaults to 600.

    Returns:
        tuple[bool, str | Path]: A tuple containing a boolean indicating success
                                 and the path to the downloaded file or an error message.
    """
    directory = HOME / folder
    directory.mkdir(parents=True, exist_ok=True)

    output_template = "%(title)s.%(ext)s"
    cmd = [
        "yt-dlp",
        "-f",
        "bestvideo[ext=mp4]+bestaudio[ext=m4a]/mp4",
        "--restrict-filenames",
        "--convert-subs",
        "vtt",
        "-o",
        output_template,
        url,
    ]

    try:
        subprocess.run(
            cmd,
            cwd=directory,
            check=True,
            timeout=timeout,
            encoding="utf-8",
        )
    except FileNotFoundError:
        return False, "yt-dlp not found. Please ensure it is installed and in your PATH."
    except subprocess.TimeoutExpired:
        return False, f"Download timed out after {timeout} seconds."
    except subprocess.CalledProcessError as e:
        error_message = str(e)
        return False, f"yt-dlp failed: {error_message}"

    return True, str(directory)