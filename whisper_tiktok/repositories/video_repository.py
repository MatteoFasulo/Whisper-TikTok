import random
from logging import Logger
from pathlib import Path


class VideoRepository:
    """Repository for video-related file operations."""

    def __init__(self, base_path: Path, logger: Logger):
        self.base_path = base_path
        self.logger = logger

    def save_audio(self, uuid: str, data: bytes) -> Path:
        """Save audio file."""
        path = self.base_path / uuid / f"{uuid}.mp3"
        path.parent.mkdir(parents=True, exist_ok=True)
        path.write_bytes(data)
        return path

    def get_background_videos(self) -> list[Path]:
        """Get list of available background videos."""
        bg_path = self.base_path / "background"
        return list(bg_path.glob("*.mp4"))

    def random_background(self) -> Path:
        """Get random background video."""
        videos = self.get_background_videos()
        if not videos:
            raise ValueError("No background videos available")
        return random.choice(videos)
