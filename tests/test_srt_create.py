import os
import random
from pathlib import Path
import pytest
import stable_whisper as whisper
from Whisper_TikTok import subtitle_creator, text_to_speech, video_prepare

@pytest.mark.asyncio
async def test_srt_create(tmp_path):
    BACKGROUND_FOLDER = Path("background")
    series = "My Series"
    part = 1

    model = whisper.load_model("small.en")

    input_text = "Hello, this is a test. It will take just a moment."
    await text_to_speech.tts(input_text, outfile=str(tmp_path / "output.mp3"))
    
    mp3_filename = str(tmp_path / "output.mp3")

    ass_filename = subtitle_creator.srt_create(model, str(tmp_path), "My Series", 1, str(mp3_filename), font="Arial")

    return Path(ass_filename).absolute()