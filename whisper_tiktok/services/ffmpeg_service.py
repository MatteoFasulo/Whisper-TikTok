import json
import os
from logging import Logger
from pathlib import Path
from typing import NamedTuple

from whisper_tiktok.execution.command_executor import CommandExecutor, ExecutionResult


class FFmpegError(Exception):
    """Custom exception for FFmpeg errors."""

    pass


class MediaInfo(NamedTuple):
    """Represents the result of running FFprobe.

    Attributes:
        return_code (int): The return code of the FFprobe process.
        json (str): The JSON output from FFprobe.
        error (str): The error message from FFprobe, if any.
    """

    return_code: int
    json: str
    error: str

    @staticmethod
    def from_json(result: ExecutionResult) -> "MediaInfo":
        return MediaInfo(return_code=result.returncode, json=result.stdout, error=result.stderr)

    @staticmethod
    def convert_time(time_in_seconds: float) -> str:
        """
        Converts time in seconds to a string in the format "hh:mm:ss.mmm".

        Args:
            time_in_seconds (float): The time in seconds to be converted.

        Returns:
            str: The time in the format "hh:mm:ss.mmm".
        """
        hours = int(time_in_seconds // 3600)
        minutes = int((time_in_seconds % 3600) // 60)
        seconds = int(time_in_seconds % 60)
        milliseconds = int((time_in_seconds - int(time_in_seconds)) * 1000)
        return f"{hours:02d}:{minutes:02d}:{seconds:02d}.{milliseconds:03d}"

    @property
    def duration(self) -> float:
        d = json.loads(self.json)

        streams = d.get("streams", [])
        audio_stream = None
        for stream in streams:
            if stream["codec_type"] == "audio":
                audio_stream = stream
                break

        if audio_stream is None:
            raise ValueError("No audio stream found")

        return float(audio_stream["duration"])


class FFmpegService:
    """Service for FFmpeg operations."""

    def __init__(self, executor: CommandExecutor, logger: Logger):
        self.executor = executor
        self.logger = logger

    def _build_video_filters(self, subtitles: Path) -> str:
        return rf"crop=ih/16*9:ih,scale=w=1080:h=1920:flags=lanczos,gblur=sigma=2,ass={subtitles.as_posix()}"

    def _build_ffmpeg_command(
        self,
        background: Path,
        audio: Path,
        output: Path,
        start_time: int,
        duration: str,
        filters: str,
    ) -> str:
        return rf"ffmpeg -ss {start_time} -t {duration} -i {background.as_posix()} -i {audio.as_posix()} -map 0:v -map 1:a -filter:v {filters} -c:v libx264 -crf 23 -c:a aac -ac 2 -b:a 192K {output.as_posix()} -y -threads {os.cpu_count()}"

    def compose_video(
        self,
        background: Path,
        audio: Path,
        subtitles: Path,
        output: Path,
        start_time: int,
        duration: str,
    ) -> Path:
        """Compose final video with background, audio, and subtitles."""

        # Build filter complex
        filters = self._build_video_filters(subtitles)

        command = self._build_ffmpeg_command(background, audio, output, start_time, duration, filters)
        result = self.executor.execute(command)

        if result.returncode != 0:
            raise FFmpegError(f"Failed to compose video: {result.stderr}")

        return output

    def get_media_info(self, file_path: Path) -> MediaInfo:
        """Get media information using ffprobe."""
        command = f"ffprobe -v quiet -print_format json -show_format -show_streams {file_path.as_posix()}"
        result = self.executor.execute(command)

        if result.returncode != 0:
            raise FFmpegError(f"Failed to probe media: {result.stderr}")

        return MediaInfo.from_json(result)
