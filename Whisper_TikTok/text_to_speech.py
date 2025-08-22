import edge_tts


async def tts(
    final_text: str,
    voice: str = "en-US-ChristopherNeural",
    stdout: bool = False,
    outfile: str = "tts.mp3",
    args=None,
) -> bool:
    """
    Converts the given text to speech using the edge-tts library.

    Args:
        final_text (str): The text to be converted to speech.
        voice (str, optional): The voice to be used for speech synthesis. Defaults to "en-US-ChristopherNeural".
        stdout (bool, optional): Whether to output the audio to stdout instead of saving to a file. Defaults to False.
        outfile (str, optional): The name of the file to save the audio to. Defaults to "tts.mp3".
        args: Additional arguments. Defaults to None

    Returns:
        bool: True if the text was successfully converted to speech.
    """
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True
