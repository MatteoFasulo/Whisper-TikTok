import platform
import os
import random
import re
import sys
import subprocess
import asyncio
import multiprocessing
from typing import Tuple
import datetime

import torch

# Rich
from rich.console import Console

# ENV
from dotenv import load_dotenv, find_dotenv

# OpenAI Whisper Model PyTorch
#import whisper
import stable_whisper as whisper

# MicrosoftEdge TTS
import edge_tts
from edge_tts import VoicesManager

# FFMPEG (Python)
import ffmpeg

HOME = os.getcwd()
console = Console()

#######################
#        STATIC       #
#######################
jsonData = {"series": "Crazy facts that you did not know",
            "part": 4,
            "outro": "Follow us for more",
            "random": False,
            "path": "F:\\PremiereTrash",
            "texts": ["Did you know that there are more possible iterations of a game of chess than there are atoms in the observable universe? The number of possible legal moves in a game of chess is around 10^120, while the estimated number of atoms in the observable universe is 10^80. This means that if every atom in the universe were a chess game being played out simultaneously, there still wouldn't be enough atoms to represent every possible iteration of the game!", "Example2", "Example 3"]}

#######################
#         CODE        #
#######################


async def main() -> bool:
    load_dotenv(find_dotenv())

    assert(torch.cuda.is_available())
    rich_print('[PyTorch] GPU version found', style='bold green')

    series = jsonData['series']
    part = jsonData['part']
    outro = jsonData['outro']
    path = jsonData['path']

    download_video(url='https://www.youtube.com/watch?v=intRX7BRA90')
    model = whisper.load_model("small.en")

    # Text 2 Speech (Edge TTS API)
    for text in jsonData['texts']:
        req_text, filename = create_full_text(path, series, part, text, outro)
        await tts(req_text, outfile=filename)

        # Whisper Model to create SRT file from Speech recording
        srt_filename = srt_create(model, path, series, part, text, filename)

        background_mp4 = random_background()
        file_info = get_info(background_mp4)
        prepare_background(background_mp4, filename_mp3=filename, filename_srt=srt_filename, W=file_info.get(
            'width'), H=file_info.get('height'), duration=int(file_info.get('duration')))

        # Increment part so it can fetch the next text in JSON
        break   #TODO: Remove this break
        part += 1

    return True

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


def download_video(url: str, resolution: str = "1080p"):
    with KeepDir() as keep_dir:
        keep_dir.chdir('background')
        rich_print("Downloading the backgrounds videos... please be patient 🙏 ")
        with subprocess.Popen(['yt-dlp', '--restrict-filenames', '--merge-output-format', 'mp4', url]) as process:
            pass
        rich_print("Background video downloaded successfully! 🎉", style="bold green")
    return


def random_background(folder_path: str = "background"):
    with KeepDir() as keep_dir:
        keep_dir.chdir(f"{HOME}{os.sep}{folder_path}")
        files = os.listdir(".")
        random_file = random.choice(files)
    return random_file


def get_info(filename: str):
    try:
        with KeepDir() as keep_dir:
            keep_dir.chdir("background")
            probe = ffmpeg.probe(filename)
            video_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'video'), None)
            audio_stream = next((stream for stream in probe['streams'] if stream['codec_type'] == 'audio'), None)
            try:
                duration = float(audio_stream['duration'])
            except Exception:
                duration = (datetime.datetime.strptime(audio_stream['DURATION'], '%H:%M:%S.%f') - datetime.datetime.min).total_seconds()
            if video_stream is None:
                rich_print('No video stream found', style="bold red")
                bit_rate = int(audio_stream['bit_rate'])
                return {'bit_rate': bit_rate, 'duration': duration}

            width = int(video_stream['width'])
            height = int(video_stream['height'])
            return {'width': width, 'height': height, 'duration': duration}
    except ffmpeg.Error as e:
        rich_print(e.stderr, style="bold red")
        sys.exit(1)


def prepare_background(background_mp4, filename_mp3, filename_srt, W: int, H: int, duration: int):
    # Get length of MP3 file to be merged with
    audio_info = get_info(filename_mp3)

    # Get starting time:
    audio_duration = int(round(audio_info.get('duration'),0))
    # print(duration-audio_duration)
    ss = random.randint(0, (duration-audio_duration))
    audio_duration = convert_time(audio_info.get('duration'))
    if ss < 0:
        ss = 0

    srt_filename = filename_srt.split('\\')[-1]
    create_directory(os.getcwd(), "output")
    output_path = f"{os.getcwd()}{os.sep}output{os.sep}"
    with KeepDir() as keep_dir:
        keep_dir.chdir("background")
        mp4_absolute_path = os.path.abspath(background_mp4)
    srt_path = "\\".join(filename_srt.split('\\')[:-1])
    rich_print(f"{filename_srt = }\n{mp4_absolute_path = }\n{filename_mp3 = }\n", style='bold green')   #
                                                                            #'Alignment=9,BorderStyle=3,Outline=5,Shadow=3,Fontsize=15,MarginL=5,MarginV=25,FontName=Lexend Bold,ShadowX=-7.1,ShadowY=7.1,ShadowColour=&HFF000000,Blur=141'Outline=5
    args = ["ffmpeg", "-ss", str(ss), "-t", str(audio_duration), "-i", mp4_absolute_path, "-i", filename_mp3, "-map", "0:v", "-map", "1:a", "-filter:v", f"crop=ih/16*9:ih, scale=w=1080:h=1920:flags=bicubic, gblur=sigma=2, subtitles={srt_filename}:force_style=',Alignment=8,BorderStyle=7,Outline=3,Shadow=5,Blur=15,Fontsize=15,MarginL=45,MarginR=55,FontName=Lexend Bold'", "-c:v", "libx265", "-preset", "5", "-b:v", "5M", "-c:a", "aac", "-ac", "1", "-b:a", "96K", f"{output_path}output_{ss}.mp4", "-y", "-threads", f"{multiprocessing.cpu_count()-6}"]
    rich_print('FFMPEG Command:\n'+' '.join(args)+'\n', style='yellow')
    with KeepDir() as keep_dir:
        keep_dir.chdir(srt_path)
        with subprocess.Popen(args, stdin=subprocess.PIPE, stdout=subprocess.PIPE) as process:
            pass
    
    return True


def srt_create(model, path: str, series: str, part: int, text: str, filename: str) -> bool:
    """
    Srt_create is a function that takes in five arguments: a model for speech-to-text conversion, a path to a directory, a series name, a part number, text content, and a filename for the audio file. The function uses the specified model to convert the audio file to text, and creates a .srt file with the transcribed text and timestamps.

    Args:
        model: A model object used for speech-to-text conversion.
        path (str): A string representing the path to the directory where the .srt file will be created.
        series (str): A string representing the name of the series.
        part (int): An integer representing the part number of the series.
        text (str): A string representing the main content of the audio file.
        filename (str): A string representing the name of the audio file.

    Returns:
        bool: A boolean indicating whether the creation of the .srt file was successful or not.

    """
    transcribe = model.transcribe(filename, regroup=True)
    transcribe.split_by_gap(0.5).split_by_length(38).merge_by_gap(0.15, max_words=2)
    series = series.replace(' ', '_')
    srtFilename = os.path.join(f"{path}{os.sep}{series}{os.sep}", f"{series}_{part}")
    transcribe.to_srt_vtt(srtFilename+'.srt', word_level=True)
    transcribe.to_ass(srtFilename+'.ass', word_level=True)
    os.chdir(HOME)
    return srtFilename+".srt"
    series = series.replace(' ', '_')
    srtFilename = os.path.join(f"{path}{os.sep}{series}{os.sep}", f"{series}_{part}.srt")
    if os.path.exists(srtFilename):
        os.remove(srtFilename)

    segments = transcribe['segments']

    for index,segment in enumerate(segments, start=1):
        startTime = convert_time(segment['start'])
        endTime = convert_time(segment['end'])
        text = segment['text']
        segmentId = segment['id']+1

        if index == 1 or index == len(segments):
            segment = f"{segmentId}\n{startTime} --> {endTime}\n<font color=#FFFF00>{text[1:].upper() if text[0] == ' ' else text.upper()}</font>\n\n"
        else:
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:].upper() if text[0] == ' ' else text.upper()}\n\n"

        with open(srtFilename, 'a', encoding='utf-8') as srtFile:
            srtFile.write(segment)

    os.chdir(HOME)
    return srtFilename


def convert_time(time_in_seconds):
    hours = int(time_in_seconds // 3600)
    minutes = int((time_in_seconds % 3600) // 60)
    seconds = int(time_in_seconds % 60)
    milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
    return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"



def batch_create(filename: str) -> None:
    """
    Batch_create is a function that takes in a filename as input and creates a new file with the concatenated contents of all the files in the './batch/' directory, sorted in alphanumeric order.

    Args:
    filename (str): A string representing the name of the output file to be created.

    Returns:
    None: This function does not return anything, but creates a new file with the contents of all the files in the './batch/' directory sorted in alphanumeric order.

    """
    with open(filename, 'wb') as out:
        def sorted_alphanumeric(data):
            def convert(text): return int(
                text) if text.isdigit() else text.lower()
            def alphanum_key(key): return [convert(c)
                                           for c in re.split('([0-9]+)', key)]
            return sorted(data, key=alphanum_key)

        for item in sorted_alphanumeric(os.listdir('./batch/')):
            filestuff = open('./batch/' + item, 'rb').read()
            out.write(filestuff)


def create_directory(path: str, directory: str) -> bool:
    """
    Create_directory is a function that takes in two arguments: a path to a directory and a name for a new directory. The function creates a new directory with the specified name in the specified path if it doesn't already exist, and returns a boolean indicating whether the directory was created.

    Args:
    path (str): A string representing the path to the directory where the new directory will be created.
    directory (str): A string representing the name of the new directory.

    Returns:
    bool: Returns True if a new directory was created, False otherwise.

    """
    current_dir = os.getcwd()
    os.chdir(path)
    if not os.path.isdir(directory):
        os.mkdir(directory)
        os.chdir(current_dir)
        return True
    return False


def create_full_text(path: str = '', series: str = '', part: int = 1, text: str = '', outro: str = '') -> Tuple[str, str]:
    """
    Create_full_text is a function that takes in four arguments: a path to a directory, a series name, a part number, text content, and outro content. The function creates a new text with series, part number, text, and outro content and returns a tuple containing the resulting text and the filename.

    Args:
        path (str): A string representing the path to the directory where the new text file will be created. Default value is an empty string.
        series (str): A string representing the name of the series. Default value is an empty string.
        part (int): An integer representing the part number of the series. Default value is 1.
        text (str): A string representing the main content of the text file. Default value is an empty string.
        outro (str): A string representing the concluding remarks of the text file. Default value is an empty string.

    Returns:
        Tuple[str, str]: A tuple containing the resulting text and the filename of the text file.

    """
    req_text = f"{series} Part {part}.\n{text}\n{outro}"
    series = series.replace(' ', '_')
    filename = f"{path}{os.sep}{series}{os.sep}{series}_{part}.mp3"
    create_directory(path, directory=series)
    return req_text, filename


async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", random_voice: bool = False, stdout: bool = False, outfile: str = "tts.mp3") -> bool:
    """
    Tts is an asynchronous function that takes in four arguments: a final text string, a voice string, a boolean value for random voice selection, a boolean value to indicate if output should be directed to standard output or not, and a filename string for the output file. The function uses Microsoft Azure Cognitive Services to synthesize speech from the input text using the specified voice, and saves the output to a file or prints it to the console.

    Args:
        final_text (str): A string representing the text to be synthesized into speech.
        voice (str): A string representing the name of the voice to be used for speech synthesis. Default value is "en-US-ChristopherNeural".
        random_voice (bool): A boolean value indicating whether to randomly select a male voice for speech synthesis. Default value is False.
        stdout (bool): A boolean value indicating whether to output the speech to the console or not. Default value is False.
        outfile (str): A string representing the name of the output file. Default value is "tts.mp3".

    Returns:
        bool: A boolean indicating whether the speech synthesis was successful or not.

    """
    voices = await VoicesManager.create()
    if random_voice:
        voices = voices.find(Gender="Male", Locale="en-US")
        voice = random.choice(voices)["Name"]
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True

if __name__ == "__main__":
    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    except Exception as e:
        print(e)
        loop.close()
        exit()
    finally:
        loop.close()
