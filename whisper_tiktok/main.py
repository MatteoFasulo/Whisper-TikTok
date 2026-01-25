"""Main module for the Whisper TikTok application."""

import asyncio
import json
import logging
import platform
import shutil
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.table import Table

from whisper_tiktok.config.logger_config import setup_logger
from whisper_tiktok.container import Container
from whisper_tiktok.factories.video_factory import VideoCreatorFactory
from whisper_tiktok.utils.color_utils import rgb_to_bgr
from whisper_tiktok.voice_manager import VoicesManager

# Create Typer app
app = typer.Typer(
    name="whisper-tiktok",
    help="Whisper TikTok - Video generation pipeline",
    add_completion=False,
)
console = Console()


@app.callback()
def main():
    """Whisper TikTok - Create TikTok videos with AI-generated subtitles."""


@app.command()
def list_voices(
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Filter by language (e.g., en-US)",
    ),
    gender: Optional[str] = typer.Option(
        None,
        "--gender",
        "-g",
        help="Filter by gender (Male/Female)",
    ),
):
    """List available TTS voices."""

    async def _list_voices():
        voices_manager = VoicesManager()
        voices_obj = await voices_manager.create()

        # Get all voices
        voices = voices_obj.voices

        # Apply filters
        if language:
            voices = [v for v in voices if v.get("Locale", "").startswith(language)]
        if gender:
            voices = [v for v in voices if v.get("Gender", "") == gender]

        # Display in a table
        table = Table(title="Available TTS Voices")
        table.add_column("Name", style="cyan")
        table.add_column("Locale", style="green")
        table.add_column("Gender", style="magenta")
        table.add_column("Voice Personalities", style="blue")
        table.add_column("Scenarios", style="yellow")

        for voice in sorted(voices, key=lambda x: x.get("Locale", "")):
            table.add_row(
                voice.get("ShortName", ""),
                voice.get("Locale", ""),
                voice.get("Gender", ""),
                ", ".join(voice["VoiceTag"].get("VoicePersonalities", [])),
                ", ".join(voice["VoiceTag"].get("TailoredScenarios", [])),
            )

        console.print(table)
        console.print(f"\n[dim]Total: {len(voices)} voices[/dim]")

    asyncio.run(_list_voices())


@app.command()
def create(
    model: str = typer.Option(
        "turbo",
        "--model",
        "-m",
        help="Whisper model size [tiny|base|small|medium|large|turbo]",
    ),
    background_url: str = typer.Option(
        "https://www.youtube.com/watch?v=intRX7BRA90",
        "--background-url",
        "-u",
        help="YouTube URL for background video",
    ),
    tts_voice: str = typer.Option(
        "en-US-ChristopherNeural",
        "--tts",
        "-v",
        help="TTS voice to use",
    ),
    random_voice: bool = typer.Option(
        False,
        "--random-voice",
        help="Use random TTS voice",
    ),
    gender: Optional[str] = typer.Option(
        None,
        "--gender",
        "-g",
        help="Gender for random voice (Male/Female)",
    ),
    language: Optional[str] = typer.Option(
        None,
        "--language",
        "-l",
        help="Language for random voice (e.g., en-US)",
    ),
    font: str = typer.Option(
        "Lexend Bold",
        "--font",
        "-f",
        help="Subtitle font",
    ),
    font_size: int = typer.Option(
        21,
        "--font-size",
        help="Subtitle font size",
    ),
    font_color: str = typer.Option(
        "FFF000",
        "--font-color",
        "-c",
        help="Subtitle color (hex format)",
    ),
    sub_position: int = typer.Option(
        5,
        "--sub-position",
        "-p",
        help="Subtitle position (1-9)",
        min=1,
        max=9,
    ),
    upload_tiktok: bool = typer.Option(
        False,
        "--upload-tiktok",
        help="Upload to TikTok",
    ),
    clean: bool = typer.Option(
        False,
        "--clean",
        help="Clean media and output folders before processing",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        help="Enable verbose logging",
    ),
):
    """Create videos from text content."""

    # Setup logging
    log_dir = Path.cwd() / "logs"
    log_level = "DEBUG" if verbose else "INFO"
    logger = setup_logger(log_dir, log_level)

    async def _create():
        nonlocal tts_voice, language

        logger.info("=" * 60)
        logger.info("Starting Whisper TikTok video creation pipeline")
        logger.info("=" * 60)

        # Validate model choice
        valid_models = ["tiny", "base", "small", "medium", "large", "turbo"]
        if model not in valid_models:
            logger.error("Invalid model. Choose from: %s", ", ".join(valid_models))
            raise typer.Exit(code=1)

        # Handle random voice selection
        if random_voice:
            if not gender or not language:
                logger.error("Both --gender and --language required for random voice")
                raise typer.Exit(code=1)

            try:
                voices_manager = VoicesManager()
                voices_obj = await voices_manager.create()
                voice_result = voices_manager.find(voices_obj, gender, language)
                tts_voice = voice_result.get("Name") or voice_result.get("ShortName")
                logger.info("Selected random voice: %s", tts_voice)
            except Exception as e:
                logger.error("Failed to select random voice: %s", e)
                raise typer.Exit(code=1) from e
        else:
            # Validate specified voice
            try:
                voices_manager = VoicesManager()
                voices_obj = await voices_manager.create()
                extracted_language = "-".join(tts_voice.split("-")[0:2])
                voice_result = voices_obj.find(Locale=extracted_language)

                if not voice_result:
                    logger.error(
                        "Voice not found. Run 'whisper-tiktok list-voices' to see available voices"
                    )
                    raise typer.Exit(code=1)

                language = extracted_language
                logger.info("Using voice: %s", tts_voice)

            except Exception as e:
                logger.error("Voice validation failed: %s", e)
                raise typer.Exit(code=1) from e

        # Process font color
        processed_font_color = font_color.lower()
        if processed_font_color.startswith("#"):
            processed_font_color = processed_font_color[1:]
        processed_font_color = rgb_to_bgr(processed_font_color)

        # Clean folders if requested
        if clean:
            logger.info("Cleaning media and output folders...")
            media_path = Path.cwd() / "media"
            output_path = Path.cwd() / "output"

            if media_path.exists():
                shutil.rmtree(media_path)
                logger.info("Removed %s", media_path)

            if output_path.exists():
                shutil.rmtree(output_path)
                logger.info("Removed %s", output_path)
        # Display startup info
        console.print("\n[bold green]🎬 Starting video creation pipeline…[/bold green]")
        console.print(f"  [cyan]Model:[/cyan] {model}")
        console.print(f"  [cyan]Voice:[/cyan] {tts_voice}")
        console.print(f"  [cyan]Language:[/cyan] {language}\n")

        # Setup DI container
        container = Container()
        config_dict = {
            "model": model,
            "background_url": background_url,
            "tts_voice": tts_voice,
            "upload_tiktok": upload_tiktok,
            "Fontname": font,
            "Fontsize": font_size,
            "highlight_color": processed_font_color,
            "Alignment": sub_position,
            "BorderStyle": "1",
            "Outline": "1",
            "Shadow": "2",
            "Blur": "21",
            "MarginL": "0",
            "MarginR": "0",
        }
        container.config.from_dict(config_dict)

        # Run application
        app_instance = Application(container, logger)

        try:
            await app_instance.run()
            console.print(
                "\n[bold green]✅ Pipeline completed successfully![/bold green]"
            )
        except Exception as e:
            logger.exception("Pipeline failed")
            console.print(f"\n[bold red]❌ Pipeline failed: {e}[/bold red]")
            raise typer.Exit(code=1) from e

    # Run the async function
    asyncio.run(_create())


class Application:
    """Main application class responsible for orchestrating the video creation pipeline.
    This class loads video data from a JSON file, builds configuration from a container,
    and processes each video asynchronously using a factory-created processor.

    Attributes:
        container (Container): Dependency injection container.
        logger (logging.Logger): Logger instance for logging operations.

    Methods:
        run(): Main method to run the video creation pipeline.
    """

    def __init__(self, container: Container, logger: logging.Logger):
        self.container = container
        self.logger = logger
        self.factory = VideoCreatorFactory(container)

    def _load_video_data(self) -> list[dict]:
        """Load video data from video.json file.
        Returns:
            List of video data dictionaries.
        """
        video_json_path = Path.cwd() / "video.json"

        try:
            data: list[dict] = json.loads(video_json_path.read_text(encoding="utf-8"))
            self.logger.info(f"Loaded {len(data)} videos from video.json")
            return data
        except FileNotFoundError:
            self.logger.error(f"video.json not found at {video_json_path}")
            raise
        except json.JSONDecodeError as e:
            self.logger.error(f"Invalid JSON in video.json: {e}")
            raise

    def _build_config(self) -> dict:
        """Build configuration from container.

        Returns:
            Configuration dictionary.
        """
        return dict(self.container.config())

    async def run(self) -> None:
        """Run the video creation pipeline.

        Returns:
            None
        """

        # Load video data
        video_data = self._load_video_data()
        config = self._build_config()

        # Process each video
        for idx, video in enumerate(video_data, 1):
            self.logger.info(
                f"Processing video {idx}/{len(video_data)}: {video.get('series', 'Unknown')}"
            )
            await self._process_video(video, config)

    async def _process_video(self, video: dict, config: dict) -> None:
        """Process a single video.

        Args:
            video (dict): Video data dictionary.
            config (dict): Configuration dictionary.

        Returns:
            None
        """

        processor = self.factory.create_processor(video, config)

        try:
            result = await processor.process()
            self.logger.info(f"✓ Video created: {result.output_path}")
        except Exception:
            self.logger.exception(
                f"✗ Failed to process video: {video.get('series', 'Unknown')}"
            )
            raise


def _setup_event_loop():
    """Setup event loop for Windows if needed.

    Returns:
        None
    """
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


if __name__ == "__main__":
    _setup_event_loop()
    app()
