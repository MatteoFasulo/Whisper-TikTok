"""Test SRT creation."""

import pytest
import stable_whisper as whisper
from whisper_tiktok import text_to_speech, subtitle_creator


@pytest.mark.asyncio
async def test_srt_create(tmp_path):
    """Test the srt_create function.

    Args:
        tmp_path: pytest fixture for a temporary path.
    """

    model = whisper.load_model("small.en")

    input_text = "Hello, this is a test. It will take just a moment."
    await text_to_speech.tts(input_text, outfile=tmp_path / "output.mp3")

    mp3_filename = tmp_path / "output.mp3"

    subtitle_creator.srt_create(model, mp3_filename=mp3_filename, out_folder=tmp_path, uuid="test-uuid")
