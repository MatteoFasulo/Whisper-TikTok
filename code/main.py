import platform
import os
import random
import re
import asyncio
from datetime import timedelta
from typing import Tuple

# ENV
from dotenv import load_dotenv, find_dotenv

# OpenAI Whisper Model PyTorch
import whisper

# MicrosoftEdge TTS 
import edge_tts
from edge_tts import VoicesManager

#######################
#        STATIC       #
#######################
jsonData = {"series": "Crazy facts that you did not know", 
            "part": 4,
            "outro": "Follow us for more",
            "random": False,
            "path": "F:\\Vari Progetti\\AI_YouTube\\source",
            "texts": ["Did you know that there are more possible iterations of a game of chess than there are atoms in the observable universe? The number of possible legal moves in a game of chess is around 10^120, while the estimated number of atoms in the observable universe is 10^80. This means that if every atom in the universe were a chess game being played out simultaneously, there still wouldn't be enough atoms to represent every possible iteration of the game!","Example2","Example 3"]}

#######################
#         CODE        #
#######################
async def main() -> bool:
    load_dotenv(find_dotenv())

    series = jsonData['series']
    part = jsonData['part']
    outro = jsonData['outro']
    path = jsonData['path']

    model = whisper.load_model("base")

    # Text 2 Speech (TikTok API) Batched
    for text in jsonData['texts']:
        req_text, filename = create_full_text(path, series, part, text, outro)
        #textlist = textwrap.wrap(req_text, width=150, break_long_words=True, break_on_hyphens=False)
        #os.makedirs('./batch/')
        #for i, item in enumerate(textlist):
        #    tts(session_id, req_text=item, filename=f'./batch/{i}.mp3')
#
        #batch_create(filename)
#
        #for item in os.listdir('./batch/'):
        #    pass
        #    os.remove('./batch/' + item)
        #os.removedirs('./batch/')
        await tts(req_text, outfile=filename)

        # Whisper Model to create SRT file from Speech recording
        transcribe = model.transcribe(filename)
        segments = transcribe['segments']
        for segment in segments:
            startTime = str(0)+str(timedelta(seconds=int(segment['start'])))+',000'
            endTime = str(0)+str(timedelta(seconds=int(segment['end'])))+',000'
            text = segment['text'].upper()
            segmentId = segment['id']+1
            segment = f"{segmentId}\n{startTime} --> {endTime}\n{text[1:] if text[0] == ' ' else text}\n\n"

            srtFilename = os.path.join(f"{path}\\{series}\\", f"{series.replace(' ', '')}_{part}.srt")
            with open(srtFilename, 'a', encoding='utf-8') as srtFile:
                srtFile.write(segment)
        
        # Increment part so it can fetch the next text in JSON
        part += 1

    return True

def batch_create(filename: str) -> None:
    with open(filename, 'wb') as out:
        def sorted_alphanumeric(data):
            convert = lambda text: int(text) if text.isdigit() else text.lower()
            alphanum_key = lambda key: [convert(c) for c in re.split('([0-9]+)', key)]
            return sorted(data, key=alphanum_key)
            
        for item in sorted_alphanumeric(os.listdir('./batch/')):
            filestuff = open('./batch/' + item, 'rb').read()
            out.write(filestuff)


def create_directory(path: str, directory: str) -> bool:
    """
    Create a new directory at the given path, if it does not already exist.

    Args:
        path (str): The path where the new directory should be created.
        directory (str): The name of the directory to be created.

    Returns:
        bool: True if the directory was created, False otherwise.

    Raises:
        This function does not raise any exceptions.

    Side effects:
        This function creates a new directory at the specified path, if one does not already exist.

    Example:
        >>> create_directory('/home/user/', 'my_dir')
        True
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
    This function takes in several parameters and returns a tuple of two strings: the final text and the outfile.

    Args:
        path (str): The path where the file will be saved. Default is an empty string.
        series (str): The name of the series. Default is an empty string.
        part (int): The part number of the series. Default is 1.
        text (str): The main text to be included in the file. Default is an empty string.
        outro (str): The concluding text to be included in the file. Default is an empty string.

    Returns:
        Tuple[str, str]: A tuple of two strings - the final text and the outfile.

    Example:
        >>> create_full_text(path='audio', series='My Series', part=2, text='This is some text', outro='Thanks for listening!')
        ("My Series Part 2.\nThis is some text\nThanks for listening!", 'audio\\MySeries\\MySeries_2.mp3')

    """
    req_text = f"{series} Part {part}.\n{text}\n{outro}"
    filename = f"{path}\\{series}\\{series.replace(' ', '')}_{part}.mp3"
    create_directory(path, directory=series)
    return req_text, filename


#def tts(session_id: str, text_speaker: str = 'en_us_010', req_text: str = 'TikTok Text to Speech', filename: str = 'voice.mp3'):
#    req_text = req_text.replace("+", "plus").replace("&", "and").replace("r/", "")
#
#    headers = {
#        'User-Agent': 'com.zhiliaoapp.musically/2022600030 (Linux; U; Android 7.1.2; es_ES; SM-G988N; Build/NRD90M;tt-ok/3.12.13.1)',
#        'Cookie': f'sessionid={session_id}'
#    }
#    url = f"https://api16-normal-c-useast1a.tiktokv.com/media/api/text/speech/invoke/"
#
#    params = {"req_text": req_text, "speaker_map_type": 0, "aid": 1233, "text_speaker": text_speaker}
#
#    r = requests.post(url, headers=headers, params=params)
#
#    if r.json()["message"] == "Couldn't load speech. Try again.":
#        output_data = {"status": "Session ID is invalid", "status_code": 5}
#        print(output_data)
#        return output_data
#
#    vstr = [r.json()["data"]["v_str"]][0]
#    msg = [r.json()["message"]][0]
#    scode = [r.json()["status_code"]][0]
#    log = [r.json()["extra"]["log_id"]][0]
#    
#    dur = [r.json()["data"]["duration"]][0]
#    spkr = [r.json()["data"]["speaker"]][0]
#
#    b64d = base64.b64decode(vstr)
#    
#    with open(filename, "wb") as out:
#        out.write(b64d)
#
#    output_data = {
#        "status": msg.capitalize(),
#        "status_code": scode,
#        "duration": dur,
#        "speaker": spkr,
#        "log": log
#    }
#
#    print(output_data)
#
#    return output_data

async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", random_voice: bool = False, stdout: bool = False, outfile: str = "tts.mp3") -> bool:
    """
    This function takes in a string of text, and generates speech audio using the Microsoft Edge Text-to-Speech API.

    Args:
        final_text (str): The text to be converted to speech audio.
        voice (str): The name of the voice to be used. Default is "en-US-ChristopherNeural".
        random_voice (bool): If True, a random male English voice will be selected. Overrides the voice argument. Default is False.
        stdout (bool): If True, the audio will be printed to standard output instead of being saved to a file. Default is False.
        outfile (str): The name of the output file. Default is "tts.mp3".

    Returns:
        bool: Returns True if the audio was successfully generated and saved to a file (if stdout=False).

    Example:
        >>> await tts("Hello world!", stdout=True)
        True

    """
    voices = await VoicesManager.create()
    if random_voice:
        voices = voices.find(Gender="Male", Locale="en-US")
        voice = random.choice(voices)["Name"]
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True

#if __name__ == "__main__":
#    main()

if __name__ == "__main__":
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()