from pathlib import Path

import stable_whisper
import torch

from whisper_tiktok.interfaces.transcription_service import ITranscriptionService


class TranscriptionService(ITranscriptionService):
    def __init__(self, logger):
        self.logger = logger

    def transcribe(
        self,
        audio_file: Path,
        srt_file: Path,
        ass_file: Path,
        model: str,
        options: dict,
    ) -> tuple[Path, Path]:
        self.logger.debug(f"Transcribing {audio_file} with model {model} and options {options}")

        whisper_model = stable_whisper.load_model(
            model, device=torch.device("cuda" if torch.cuda.is_available() else "cpu")
        )
        self.logger.debug(f"Loaded Whisper model: {model}")

        transcription = whisper_model.transcribe(
            audio_file.as_posix(),
            regroup=True,
            fp16=False,
            word_timestamps=True,
        )
        transcription.to_srt_vtt(srt_file.as_posix(), word_level=True)
        transcription.to_ass(ass_file.as_posix(), word_level=True, **options)
        return (srt_file, ass_file)
