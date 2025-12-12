from logging import Logger
from pathlib import Path

from whisper_tiktok.execution.command_executor import CommandExecutor
from whisper_tiktok.interfaces.video_downloader import IVideoDownloader


class VideoDownloadError(Exception):
    """Custom exception for video download errors."""


class VideoDownloaderService(IVideoDownloader):
    """YouTube video downloader using yt-dlp."""

    def __init__(self, executor: CommandExecutor, logger: Logger):
        self.executor = executor
        self.logger = logger

    def download(self, url: str, output_dir: Path) -> Path:
        """Download video from URL."""
        output_dir.mkdir(parents=True, exist_ok=True)

        command = rf"yt-dlp -f bestvideo[ext=mp4] --restrict-filenames -o %(id)s.%(ext)s {url}"
        result = self.executor.execute(command, cwd=output_dir)

        if result.returncode != 0:
            raise VideoDownloadError(f"Failed to download: {result.stderr}")

        # Find downloaded file
        videos = list(output_dir.glob("*.mp4"))
        if not videos:
            raise VideoDownloadError("No video file found after download")

        return videos[-1]  # Most recent
