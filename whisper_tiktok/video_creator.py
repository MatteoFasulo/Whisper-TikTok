"""Module for creating videos from audio and subtitles."""

from argparse import Namespace
from logging import Logger
from pathlib import Path
import uuid

import stable_whisper as whisper

from .subtitle_creator import srt_create
from .text_to_speech import tts
from .tiktok import upload_tiktok
from .video_prepare import prepare_background
from .video_downloader import download_video as youtube_download
from .utils import random_background

HOME = Path.cwd()
media_folder = HOME / "media"
output_folder = HOME / "output"


class VideoCreator:
    """
    VideoCreator is responsible for creating videos from the provided metadata and arguments.
    """

    def __init__(self, video: dict, args: Namespace, logger: Logger):
        """
        Initializes the VideoCreator with video metadata, arguments, and a logger.

        Args:
            video (dict): The video metadata.
            args (Namespace): The command-line arguments.
            logger (Logger): The logger instance.
        """
        self.video = video
        self.args = args
        self.logger = logger

        self.uuid = str(uuid.uuid4())
        self.media_path = Path(media_folder / self.uuid).absolute()
        self.output_path = Path(output_folder / self.uuid).absolute()

        self.mp3_file = self.media_path / f"{self.uuid}.mp3"
        self.ass_file = self.media_path / f"{self.uuid}.ass"
        self.mp4_final_video = self.output_path / f"{self.uuid}.mp4"

        # Create media and output directories based on UUID
        self.media_path.mkdir(parents=True, exist_ok=True)
        self.output_path.mkdir(parents=True, exist_ok=True)

    def download_video(self, url: str, folder: str = "background"):
        """
        Downloads the video from the specified URL.

        Args:
            url (str): The URL of the video to download.
            folder (str): The folder to download the video to.
        """
        youtube_download(url=url, folder=folder)
        self.logger.info(f"Video downloaded from {url} to {folder}")

    async def text_to_speech(self, req_text: str, voice: str):
        """
        Generates the text content for the video and then converts it to speech via TTS.

        Args:
            req_text (str): The text to convert to speech.
            voice (str): The voice to use for TTS.
        """
        await tts(text=req_text, outfile=self.mp3_file, voice=voice)

    def generate_transcription(self, model: str, non_english: bool):
        """
        Generates the transcription for the video by using the Whisper model.

        Args:
            model (str): The Whisper model to use.
            non_english (bool): Whether the video is in a non-English language.
        """
        if model != "large" and not non_english:
            model = model + ".en"
        whisper_model = whisper.load_model(model)
        self.logger.info(f"Loaded Whisper model: {model}")

        srt_create(
            whisper_model,
            mp3_filename=self.mp3_file,
            out_folder=self.media_path,
            uuid=self.uuid,
            **vars(self.args),
        )
        self.logger.info("SRT and ASS subtitles created successfully.")

    def create_final_video(self):
        """
        Creates the final video by combining the background, audio, and subtitles.
        """
        # get background video
        mp4_background_filename = random_background()
        self.logger.info(f"Selected background video: {mp4_background_filename}")

        # create final video
        final_video = prepare_background(
            mp4_background_filename=mp4_background_filename,
            mp3_filename=self.mp3_file,
            ass_filename=self.ass_file,
            out_folder=self.output_path,
            uuid=self.uuid,
        )
        self.logger.info(f"Created final video: {final_video}")

    def upload_to_tiktok(self):
        """
        Uploads the final video to TikTok.
        """
        series = self.video.get("series", "")
        part = self.video.get("part", "")
        tags = self.video.get("tags", [])
        upload_tiktok(
            str(self.mp4_final_video),
            title=f"{series} - {part}",
            tags=tags,
            headless=False,
        )
        self.logger.info("Uploaded video to TikTok")
