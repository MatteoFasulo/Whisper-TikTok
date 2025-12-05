from dataclasses import dataclass
from logging import Logger
from pathlib import Path

from whisper_tiktok.strategies.processing_strategy import (
    ProcessingContext,
    ProcessingStrategy,
)


@dataclass
class ProcessingResult:
    """Result of video processing."""

    uuid: str
    output_path: Path
    success: bool = True


class VideoProcessor:
    """Main orchestrator for video processing pipeline."""

    def __init__(
        self,
        uuid: str,
        video_data: dict,
        config: dict,
        strategies: list[ProcessingStrategy],
        logger: Logger,
    ):
        self.uuid = uuid
        self.video_data = video_data
        self.config = config
        self.strategies = strategies
        self.logger = logger

    async def process(self) -> ProcessingResult:
        """Execute the processing pipeline."""

        # Initialize context
        media_path = Path(self.config.get("workspace_path", ".")) / "media" / self.uuid
        output_path = Path(self.config.get("workspace_path", ".")) / "output" / self.uuid

        media_path.mkdir(parents=True, exist_ok=True)
        output_path.mkdir(parents=True, exist_ok=True)

        context = ProcessingContext(
            video_data=self.video_data,
            uuid=self.uuid,
            media_path=media_path,
            output_path=output_path,
            config=self.config,
        )

        # Execute each strategy
        try:
            for strategy in self.strategies:
                self.logger.info(f"Executing strategy: {strategy.__class__.__name__}")
                context = await strategy.execute(context)

            output_file = context.output_path / f"{self.uuid}.mp4"

            return ProcessingResult(
                uuid=self.uuid,
                output_path=output_file,
                success=True,
            )
        except Exception:
            self.logger.exception(f"Processing failed for video {self.uuid}")
            raise
