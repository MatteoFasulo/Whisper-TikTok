from typing import Tuple
import os
import platform
import asyncio
import random

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
            "texts": ["Example 1", "Example 2", "Example 3"]}

#######################
#         CODE        #
#######################
async def main() -> bool:
    """
    Asynchronous function that generates and synthesizes speech from a list of text strings.

    Args:
        None. Assumes that the necessary data is stored in a global variable called `jsonData`.
        `jsonData` is expected to be a dictionary with the following keys:
            - 'series': an integer indicating the index of the series.
            - 'part': an integer indicating the index of the part.
            - 'outro': a string with the outro text.
            - 'path': a string with the path to store the synthesized audio files.
            - 'random': a boolean indicating whether to use a random voice or not.
            - 'texts': a list of strings with the text to synthesize.

    Returns:
        A boolean value indicating whether the function executed successfully (always True).

    Raises:
        This function does not raise any exceptions.

    Side effects:
        This function generates speech and saves it to disk. It also updates the `part` counter in `jsonData`.

    """
    series = jsonData['series']
    part = jsonData['part']
    outro = jsonData['outro']
    path = jsonData['path']
    random_voice = jsonData['random']

    for text in jsonData['texts']:
        final_text, outfile = create_full_text(path, series, part, text, outro)
        await tts(final_text, outfile=outfile, random_voice=random_voice)
        part += 1

    return True


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
    final_text = f"{series} Part {part}.\n{text}\n{outro}"
    outfile = f"{path}\\{series}\\{series.replace(' ', '')}_{part}.mp3"
    create_directory(path, directory=series)
    return final_text, outfile


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


if __name__ == "__main__":
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()