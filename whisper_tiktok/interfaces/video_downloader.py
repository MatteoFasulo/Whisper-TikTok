from abc import ABC, abstractmethod
from pathlib import Path


class IVideoDownloader(ABC):
    """Interface for video downloading services."""

    @abstractmethod
    def download(self, url: str, output_dir: Path) -> Path:
        """Download video from URL to output directory."""
        pass
