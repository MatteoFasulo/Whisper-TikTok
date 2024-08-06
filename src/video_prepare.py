import multiprocessing
import os
import subprocess
import random

from utils import *

HOME = Path.cwd()


def prepare_background(background_mp4: str, filename_mp3: str, filename_srt: str, verbose: bool = False) -> str:

    # Check if the input files are strings
    assert isinstance(background_mp4, str)
    assert isinstance(filename_srt, str)
    assert isinstance(filename_mp3, str)

    # Get the duration of the video and audio files
    video_info = get_info(background_mp4, kind='video')
    video_duration = int(round(video_info.get('duration'), 0))

    audio_info = get_info(filename_mp3, kind='audio')
    audio_duration = int(round(audio_info.get('duration'), 0))

    # Randomly select a start time for the audio file
    ss = random.randint(0, (video_duration-audio_duration))

    # Convert the time to HH:MM:SS format
    audio_duration = convert_time(audio_duration)
    if ss < 0:
        ss = 0

    # Create the output directory if it does not exist
    directory = HOME / 'output'
    if not directory.exists():
        directory.mkdir()

    # Set the output file path
    outfile = f"{HOME}{os.sep}output{os.sep}output_{ss}.mp4"

    if verbose:
        rich_print(
            f"{filename_srt = }\n{background_mp4 = }\n{filename_mp3 = }\n", style='bold green')

    # Switch inside the subtitle file directory
    old_dir = os.getcwd()
    os.chdir(Path(filename_srt).parent)

    # Extract only the filename from the path
    # This is to avoid any issues with the path (see https://stackoverflow.com/questions/71597897/unable-to-parse-option-value-xxx-srt-as-image-size-in-ffmpeg)
    # First we switch inside the directory of the subtitle file and then we execute the FFMPEG command with the filename only (not the full path)
    filename_srt_name = Path(filename_srt).name

    # FFMPEG Command
    args = [
        "ffmpeg",
        "-ss", str(ss),
        "-t", str(audio_duration),
        "-i", background_mp4,
        "-i", filename_mp3,
        "-map", "0:v",
        "-map", "1:a",
        "-vf", f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=lanczos, gblur=sigma=2, ass='{filename_srt_name}'",
        "-c:v", "libx264",
        "-crf", "23",
        "-c:a", "aac",
        "-ac", "2",
        "-b:a", "192K",
        f"{outfile}",
        "-y",
        "-threads", f"{multiprocessing.cpu_count()}"]

    if verbose:
        rich_print('[i] FFMPEG Command:\n'+' '.join(args)+'\n', style='yellow')

    # Execute the FFMPEG command
    subprocess.run(args, check=True)

    # Go back to old dir
    os.chdir(old_dir)

    return outfile
