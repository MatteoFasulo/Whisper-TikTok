from abc import ABC, abstractmethod
from dataclasses import dataclass, field
from logging import Logger
from pathlib import Path

from whisper_tiktok.interfaces.transcription_service import ITranscriptionService
from whisper_tiktok.interfaces.tts_service import ITTSService
from whisper_tiktok.interfaces.video_downloader import IVideoDownloader
from whisper_tiktok.services.ffmpeg_service import FFmpegService


@dataclass
class ProcessingContext:
    """Context object passed through processing pipeline."""

    video_data: dict
    uuid: str
    media_path: Path
    output_path: Path
    config: dict
    artifacts: dict = field(default_factory=dict)


class ProcessingStrategy(ABC):
    """Base strategy for video processing steps."""

    @abstractmethod
    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        """Execute processing step and update context."""


class DownloadBackgroundStrategy(ProcessingStrategy):
    """Strategy for downloading background video."""

    def __init__(self, downloader: IVideoDownloader, logger: Logger):
        self.downloader = downloader
        self.logger = logger

    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        url = context.config["background_url"]
        background_path = self.downloader.download(url, Path("background"))
        context.artifacts["background_video"] = background_path
        self.logger.info(f"Downloaded background: {background_path}")
        return context


class TTSGenerationStrategy(ProcessingStrategy):
    """Strategy for generating TTS audio."""

    def __init__(self, tts_service: ITTSService, logger: Logger):
        self.tts_service = tts_service
        self.logger = logger

    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        """Integrates TTS into the pipeline"""
        text = f"{context.video_data['series']} - {context.video_data['part']}.\n"
        text += f"{context.video_data['text']}\n"
        text += f"{context.video_data['outro']}"

        output_file = context.media_path / f"{context.uuid}.mp3"
        voice = context.config.get("tts_voice", "en-US-ChristopherNeural")

        await self.tts_service.synthesize(text, output_file, voice)
        context.artifacts["audio_file"] = output_file

        self.logger.info(f"Generated TTS audio: {output_file}")
        return context


class TranscriptionStrategy(ProcessingStrategy):
    """Strategy for transcribing audio to generate subtitles."""

    def __init__(self, transcription_service: ITranscriptionService, logger: Logger):
        self.transcription_service = transcription_service
        self.logger = logger

    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        audio_file = context.artifacts.get("audio_file")
        if not audio_file:
            raise ValueError("Audio file not found in context artifacts.")

        srt_file = context.media_path / f"{context.uuid}.srt"
        ass_file = context.media_path / f"{context.uuid}.ass"
        self.transcription_service.transcribe(
            audio_file,
            srt_file,
            ass_file,
            model=context.config["model"],
            options=context.config,
        )
        context.artifacts["srt_file"] = srt_file
        context.artifacts["ass_file"] = ass_file
        self.logger.info(f"Generated transcription SRT: {srt_file}")
        self.logger.info(f"Generated transcription ASS: {ass_file}")
        return context


class VideoCompositionStrategy(ProcessingStrategy):
    """Strategy for composing the final video."""

    def __init__(self, ffmpeg_service: FFmpegService, logger: Logger):
        self.ffmpeg_service = ffmpeg_service
        self.logger = logger

    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        background_video = context.artifacts["background_video"]
        audio_file = context.artifacts["audio_file"]
        ass_file = context.artifacts["ass_file"]

        # Get video duration and audio duration to calculate start time
        audio_info = self.ffmpeg_service.get_media_info(file_path=audio_file)
        duration = audio_info.duration
        str_duration = audio_info.convert_time(time_in_seconds=duration)

        # Then compose video
        output_file = context.output_path / f"{context.uuid}.mp4"

        # Implementation using FFmpegService
        self.ffmpeg_service.compose_video(
            background=background_video,
            audio=audio_file,
            subtitles=ass_file,
            output=output_file,
            start_time=0,
            duration=str_duration,
        )

        context.artifacts["final_video"] = output_file
        self.logger.info(f"Composed video: {output_file}")
        return context


class TikTokUploadStrategy(ProcessingStrategy):
    """Strategy for uploading videos to TikTok."""

    def __init__(self, uploader, logger: Logger):
        self.uploader = uploader
        self.logger = logger

    async def execute(self, context: ProcessingContext) -> ProcessingContext:
        raise NotImplementedError("TikTok upload not implemented yet.")
