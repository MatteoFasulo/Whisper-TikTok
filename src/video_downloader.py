import subprocess
from pathlib import Path

import msg
from utils import KeepDir

HOME = Path.cwd()


def download_video(url: str, folder: str = 'background'):
    """
    Downloads a video from the given URL and saves it to the specified folder.

    Args:
        url (str): The URL of the video to download.
        folder (str, optional): The name of the folder to save the video in. Defaults to 'background'.
    """
    directory = HOME / folder
    if not directory.exists():
        directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(folder)
        subprocess.run(['yt-dlp', '-f bestvideo[ext=mp4]',
                       '--restrict-filenames', url], check=True)
