"""Module for text-to-speech conversion using edge-tts."""

from pathlib import Path
import edge_tts


async def tts(
    text: str,
    outfile: Path,
    voice: str = "en-US-ChristopherNeural",
) -> None:
    """
    Converts the given text to speech using the edge-tts library.

    Args:
        text (str): The text to be converted to speech.
        outfile (str): The name of the file to save the audio to.
        voice (str, optional): The voice to be used for speech.
    """
    communicate = edge_tts.Communicate(text, voice)
    await communicate.save(str(outfile))
