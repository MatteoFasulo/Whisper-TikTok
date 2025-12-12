from abc import ABC, abstractmethod
from pathlib import Path


class ITranscriptionService(ABC):
    """Interface for transcription services."""

    @abstractmethod
    def transcribe(
        self,
        audio_file: Path,
        srt_file: Path,
        ass_file: Path,
        model: str,
        options: dict,
    ) -> tuple[Path, Path]:
        """Transcribe audio and generate SRT/ASS files."""
