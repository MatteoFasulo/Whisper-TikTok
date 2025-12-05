import uuid

from whisper_tiktok.container import Container
from whisper_tiktok.processors.video_processor import VideoProcessor
from whisper_tiktok.strategies.processing_strategy import (
    DownloadBackgroundStrategy,
    ProcessingStrategy,
    TikTokUploadStrategy,
    TranscriptionStrategy,
    TTSGenerationStrategy,
    VideoCompositionStrategy,
)


class VideoCreatorFactory:
    """Factory for creating video processor instances."""

    def __init__(self, container: Container):
        self.container = container

    def create_processor(self, video_data: dict, config: dict) -> VideoProcessor:
        """Create a configured video processor."""
        uuid_str = str(uuid.uuid4())

        return VideoProcessor(
            uuid=uuid_str,
            video_data=video_data,
            config=config,
            strategies=self._build_strategies(config),
            logger=self.container.logger(),
        )

    def _build_strategies(self, config: dict) -> list[ProcessingStrategy]:
        """Build processing pipeline based on config."""
        strategies = [
            DownloadBackgroundStrategy(self.container.video_downloader(), self.container.logger()),
            TTSGenerationStrategy(self.container.tts_service(), self.container.logger()),
            TranscriptionStrategy(self.container.transcription_service(), self.container.logger()),
            VideoCompositionStrategy(self.container.ffmpeg_service(), self.container.logger()),
        ]

        if config.get("upload_tiktok"):
            strategies.append(TikTokUploadStrategy(self.container.uploader(), self.container.logger()))

        return strategies
