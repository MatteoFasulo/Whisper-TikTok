from logging import Logger
from pathlib import Path

import edge_tts

from whisper_tiktok.interfaces.tts_service import ITTSService


class TTSService(ITTSService):
    """Text-to-Speech service using a hypothetical TTS engine."""

    def __init__(self, logger: Logger):
        self.logger = logger

    async def synthesize(
        self,
        text: str,
        output_file: Path,
        voice: str = "en-US-ChristopherNeural",
    ) -> None:
        """
        Synthesize speech from text and save to output file.

        Args:
            text (str): The text to be converted to speech.
            output_path (Path): The path to save the synthesized audio file.
            voice (str): The voice to be used for synthesis.
        """
        self.logger.debug(f"Synthesizing speech to {output_file} using voice {voice}")
        communicate = edge_tts.Communicate(text, voice)
        await communicate.save(output_file.as_posix())
