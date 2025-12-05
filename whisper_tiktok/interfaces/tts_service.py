from abc import ABC, abstractmethod
from pathlib import Path


class ITTSService(ABC):
    """Interface for text-to-speech services."""

    @abstractmethod
    async def synthesize(self, text: str, output_file: Path, voice: str) -> None:
        """Synthesize speech from text."""
        pass
