"""Main module for the Whisper TikTok application."""

import argparse
import asyncio
import json
import logging
import os
import platform
import sys
from pathlib import Path

from rich.console import Console

from .utils import rgb_to_bgr
from .video_creator import VideoCreator
from .voice_manager import VoicesManager

# Default directory
HOME = Path.cwd()
LOG_DIR = HOME / "logs"

# Rich Console
console = Console()

# Logging
os.makedirs(LOG_DIR, exist_ok=True)
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s",
    handlers=[
        logging.StreamHandler(sys.stdout),
        logging.FileHandler(LOG_DIR / "app.log"),
    ],
)
logger = logging.getLogger(__name__)

# JSON video file
video_json_path = HOME / "video.json"
jsonData = json.loads(video_json_path.read_text(encoding="utf-8"))


async def main() -> None:
    """
    Main entry point for the application.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--model",
        default="small",
        help="Model to use",
        choices=["tiny", "base", "small", "medium", "large"],
        type=str,
    )
    parser.add_argument("--non_english", action="store_true", help="Don't use the english model.")
    parser.add_argument(
        "--url",
        metavar="U",
        default="https://www.youtube.com/watch?v=intRX7BRA90",
        help="Youtube URL to download as background video.",
        type=str,
    )
    parser.add_argument(
        "--tts",
        default="en-US-ChristopherNeural",
        help="Voice to use for TTS",
        type=str,
    )
    parser.add_argument(
        "--list-voices",
        help="Use `edge-tts --list-voices` to list all voices",
        action="help",
    )
    parser.add_argument(
        "--random_voice",
        action="store_true",
        help="Random voice for TTS",
        default=False,
    )
    parser.add_argument(
        "--gender",
        choices=["Male", "Female"],
        help="Gender of the random TTS voice",
        type=str,
    )
    parser.add_argument(
        "--language",
        help="Language of the random TTS voice for example: en-US",
        type=str,
    )
    parser.add_argument(
        "--sub_format",
        help="Subtitle format",
        choices=["u", "i", "b"],
        default="b",
        type=str,
    )
    parser.add_argument(
        "--sub_position",
        help="Subtitle position",
        choices=list(range(1, 10)),
        default=5,
        type=int,
    )
    parser.add_argument("--font", help="Subtitle font", default="Lexend Bold", type=str)
    parser.add_argument(
        "--font_color",
        help="Subtitle font color in hex format: FFF000",
        default="FFF000",
        type=str,
    )
    parser.add_argument("--font_size", help="Subtitle font size", default=21, type=int)
    parser.add_argument(
        "--upload_tiktok",
        help="Upload to TikTok after creating the video",
        action="store_true",
        default=False,
    )
    args = parser.parse_args()

    if args.random_voice:  # Random voice
        args.tts = None
        if not args.gender:
            print("When using --random_voice, please specify both --gender and --language.")
            sys.exit(1)

        elif not args.language:
            print("When using --random_voice, please specify both --gender and --language.")
            sys.exit(1)

        elif args.gender and args.language:
            # Check if voice is valid
            voices_manager_obj = await VoicesManager().create()
            voices = await VoicesManager().find(voices_manager_obj, args.gender, args.language)
            args.tts = voices["Name"]

            # Check if language is english
            if not str(args.language).startswith("en"):
                args.non_english = True

    else:
        # Check if voice is valid
        voices = await VoicesManager().create()
        args.language = "-".join(i for i in args.tts.split("-")[0:2])
        voices = voices.find(Locale=args.language)
        if len(voices) == 0:
            # Voice not found
            print("Specified TTS voice not found. Use `edge-tts --list-voices` to list all voices.")
            sys.exit(1)

    # Extract language from TTS voice
    if args.tts:
        lang_prefix = args.tts.split("-")[0]
        if not lang_prefix.startswith("en"):
            args.non_english = True

    # Cast font color to lowercase
    args.font_color = args.font_color.lower()

    # Remove # from font color
    if args.font_color.startswith("#"):
        args.font_color = args.font_color[1:]

    # Convert font color from RGB to BGR
    args.font_color = rgb_to_bgr(args.font_color)

    # Clear terminal
    console.clear()

    console.print("[bold green]Starting video creation pipeline…[/bold green]")

    for video in jsonData:
        logger.info("Creating video")
        with console.status("Creating video\t") as _:

            video_creator = VideoCreator(args=args, logger=logger, video=video)

            full_text = (
                f"{video_creator.video['series']} - {video_creator.video['part']}.\n"
                f"{video_creator.video['text']}\n"
                f"{video_creator.video['outro']}"
            )

            status, info = video_creator.download_video(url=args.url, folder="background")
            if not status:
                console.print(f"[bold red]Error downloading video: {info}[/bold red]")
                sys.exit(1)

            await video_creator.text_to_speech(
                req_text=full_text,
                voice=str(args.tts),
            )

            video_creator.generate_transcription(model=args.model, non_english=args.non_english)

            video_creator.create_final_video()

            if args.upload_tiktok:
                video_creator.upload_to_tiktok()

        console.log(f"{str(video_creator.mp4_final_video)}")
    return


if __name__ == "__main__":

    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())  # type: ignore

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    loop.close()

    sys.exit(0)
