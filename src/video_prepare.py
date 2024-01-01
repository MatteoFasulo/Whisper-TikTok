import multiprocessing
import os
import subprocess
import random

from utils import *

HOME = Path.cwd()


def prepare_background(background_mp4: str, filename_mp3: str, filename_srt: str, verbose: bool = False) -> str:
    video_info = get_info(background_mp4, kind='video')
    video_duration = int(round(video_info.get('duration'), 0))

    audio_info = get_info(filename_mp3, kind='audio')
    audio_duration = int(round(audio_info.get('duration'), 0))

    ss = random.randint(0, (video_duration-audio_duration))
    audio_duration = convert_time(audio_duration)
    if ss < 0:
        ss = 0

    srt_filename = filename_srt.name
    srt_path = filename_srt.parent.absolute()

    directory = HOME / 'output'
    if not directory.exists():
        directory.mkdir()

    outfile = f"{HOME}{os.sep}output{os.sep}output_{ss}.mp4"

    if verbose:
        rich_print(
            f"{filename_srt = }\n{background_mp4 = }\n{filename_mp3 = }\n", style='bold green')

    args = [
        "ffmpeg",
        "-ss", str(ss),
        "-t", str(audio_duration),
        "-i", background_mp4,
        "-i", filename_mp3,
        "-map", "0:v",
        "-map", "1:a",
        "-filter:v", f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=lanczos, gblur=sigma=2, ass={srt_filename}",
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

    with KeepDir() as keep_dir:
        keep_dir.chdir(srt_path)
        subprocess.run(args, check=True)

    return outfile
