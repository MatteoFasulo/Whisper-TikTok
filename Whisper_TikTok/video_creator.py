import os
import json
from pathlib import Path

import stable_whisper as whisper
from .subtitle_creator import srt_create
from .text_to_speech import tts
from .tiktok import upload_tiktok
from .video_prepare import prepare_background
from .video_downloader import download_video as youtube_download
from .utils import random_background

HOME = Path.cwd()
media_folder = HOME / "media"


class VideoCreator:
    def __init__(self, video, args, logger):
        """
        Initializes the VideoCreator with video metadata, arguments, and a logger.

        Args:
            video (dict): The video metadata.
            args (Namespace): The command-line arguments.
            logger (Logger): The logger instance.
        """
        self.args = args
        self.video = video
        self.logger = logger

        self.series = video.get("series", "")
        self.part = video.get("part", "")
        self.text = video.get("text", "")
        self.tags = video.get("tags", list())
        self.outro = video.get("outro", "")
        self.path = Path(media_folder).absolute()

    def download_video(self, folder: str = "background"):
        """
        Downloads the video from the specified URL.

        Args:
            folder (str): The folder to download the video to.
        """
        youtube_download(url=self.args.url, folder=folder)
        self.logger.info(f"Video downloaded from {self.args.url} to {folder}")

    def load_model(self):
        """
        Loads the Whisper model based on the specified arguments.
        """
        model = self.args.model
        if self.args.model != "large" and not self.args.non_english:
            model = self.args.model + ".en"
        whisper_model = whisper.load_model(model)
        self.logger.info(f"Loaded Whisper model: {model}")

        self.model = whisper_model
        return whisper_model

    def create_text(self):
        """
        Creates the text and audio file for the video.
        """
        req_text = f"{self.series} - {self.part}.\n{self.text}\n{self.outro}"
        series = self.series.replace(" ", "_")
        filename = f"{self.path}{os.sep}{series}{os.sep}{series}_{self.part}.mp3"

        Path(f"{self.path}{os.sep}{series}").mkdir(parents=True, exist_ok=True)
        self.logger.info(f"Created directory: {self.path}{os.sep}{series}")

        self.req_text = req_text
        self.mp3_file = filename
        return req_text, filename

    async def text_to_speech(self):
        """
        Converts the text to speech and saves it as an audio file.
        """
        await tts(
            self.req_text, outfile=self.mp3_file, voice=self.args.tts, args=self.args
        )

    def generate_transcription(self):
        """
        Generates the transcription for the video.
        """
        ass_filename = srt_create(
            self.model,
            self.path,
            self.series,
            self.part,
            self.mp3_file,
            **vars(self.args),
        )
        ass_filename = Path(ass_filename).absolute()
        self.logger.info(f"Generated transcription: {ass_filename}")

        self.ass_file = ass_filename
        return ass_filename

    def select_background(self):
        """
        Selects a random background video from the specified folder.
        """
        background_mp4 = random_background()
        self.logger.info(f"Selected background video: {background_mp4}")
        self.mp4_background = background_mp4
        return background_mp4

    def integrate_subtitles(self):
        """
        Integrates the subtitles into the video.
        """
        final_video = prepare_background(
            self.mp4_background,
            filename_mp3=self.mp3_file,
            filename_srt=self.ass_file,
            verbose=self.args.verbose,
        )
        final_video = Path(final_video).absolute()
        self.logger.info(f"Integrated subtitles into video: {final_video}")

        self.mp4_final_video = final_video
        return final_video

    def upload_to_tiktok(self):
        """
        Uploads the final video to TikTok.
        """
        uploaded = upload_tiktok(
            str(self.mp4_final_video),
            title=f"{self.series} - {self.part}",
            tags=self.tags,
            headless=not self.args.verbose,
        )
        self.logger.info(f"Uploaded video to TikTok: {uploaded}")
        return uploaded
