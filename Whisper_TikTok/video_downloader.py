import os
import subprocess
from pathlib import Path

HOME = Path.cwd()


def download_video(url: str, folder: str = "background"):
    """
    Downloads a video from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the video to download.
        folder (str, optional): The name of the folder to save the video in. Defaults to 'background'.
    """
    directory = HOME / folder
    os.makedirs(directory, exist_ok=True)

    subprocess.Popen(["yt-dlp", "-f bestvideo[ext=mp4]", "--restrict-filenames", url], cwd=directory).wait()
    return
