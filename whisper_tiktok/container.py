import logging
from pathlib import Path

from dependency_injector import containers, providers

from whisper_tiktok.execution.command_executor import CommandExecutor
from whisper_tiktok.services.ffmpeg_service import FFmpegService
from whisper_tiktok.services.transcription_service import TranscriptionService
from whisper_tiktok.services.tts_service import TTSService
from whisper_tiktok.services.video_downloader import VideoDownloaderService


class Container(containers.DeclarativeContainer):
    """IoC container for dependency injection."""

    config = providers.Configuration()

    # Path providers
    workspace_path = providers.Singleton(lambda: Path.cwd())

    media_path = providers.Factory(
        lambda workspace, uuid: workspace / "media" / uuid,
        workspace=workspace_path,
        uuid=providers.Dependency(),
    )

    output_path = providers.Factory(
        lambda workspace, uuid: workspace / "output" / uuid,
        workspace=workspace_path,
        uuid=providers.Dependency(),
    )

    # Service providers
    logger = providers.Singleton(lambda: logging.getLogger("whisper_tiktok"))

    command_executor = providers.Factory(CommandExecutor, logger=logger)

    ffmpeg_service = providers.Factory(
        FFmpegService, executor=command_executor, logger=logger
    )  # Changed

    video_downloader = providers.Factory(
        VideoDownloaderService,
        executor=command_executor,  # Changed from ffmpeg_service
        logger=logger,
    )

    tts_service = providers.Factory(TTSService, logger=logger)

    transcription_service = providers.Factory(TranscriptionService, logger=logger)

    # Additional service providers can be added here
