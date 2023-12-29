import edge_tts


async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", stdout: bool = False, outfile: str = "tts.mp3", args=None) -> bool:
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True
