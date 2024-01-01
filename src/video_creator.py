import json
from pathlib import Path

import stable_whisper as whisper
from .logger import setup_logger
from .subtitle_creator import srt_create
from .text_to_speech import tts
from .tiktok import upload_tiktok
from .video_prepare import prepare_background
from .video_downloader import download_video as youtube_download
from utils import *

HOME = Path.cwd()
logger = setup_logger()
media_folder = HOME / 'media'


class VideoCreator:
    def __init__(self, video, args):
        self.args = args
        self.video = video

        self.series = video.get('series', '')
        self.part = video.get('part', '')
        self.text = video.get('text', '')
        self.tags = video.get('tags', list())
        self.outro = video.get('outro', '')
        self.path = Path(media_folder).absolute()

    def download_video(self, folder='background'):
        youtube_download(url=self.args.url, folder=folder)
        console.log(
            f"{msg.OK}Video downloaded from {self.args.url} to {folder}")
        logger.info(f"Video downloaded from {self.args.url} to {folder}")

    def load_model(self):
        model = self.args.model
        if self.args.model != "large" and not self.args.non_english:
            model = self.args.model + ".en"
        whisper_model = whisper.load_model(model)

        self.model = whisper_model
        return whisper_model

    def create_text(self):
        req_text = f"{self.series} - {self.part}.\n{self.text}\n{self.outro}"
        series = self.series.replace(' ', '_')
        filename = f"{self.path}{os.sep}{series}{os.sep}{series}_{self.part}.mp3"

        Path(f"{self.path}{os.sep}{series}").mkdir(parents=True, exist_ok=True)

        self.req_text = req_text
        self.mp3_file = filename
        return req_text, filename

    async def text_to_speech(self):
        await tts(self.req_text, outfile=self.mp3_file, voice=self.args.tts, args=self.args)

    def generate_transcription(self):
        ass_filename = srt_create(self.model,
                                  self.path, self.series, self.part, self.text, self.mp3_file, **vars(self.args))
        ass_filename = Path(ass_filename).absolute()

        self.ass_file = ass_filename
        return ass_filename

    def select_background(self):
        background_mp4 = random_background()

        self.mp4_backgroung = background_mp4
        return background_mp4

    def integrate_subtitles(self):
        final_video = prepare_background(
            self.mp4_backgroung, filename_mp3=self.mp3_file, filename_srt=self.ass_file, verbose=self.args.verbose)
        final_video = Path(final_video).absolute()

        self.mp4_final_video = final_video
        return final_video

    def upload_to_tiktok(self):
        uploaded = upload_tiktok(str(
            self.mp4_final_video), title=f"{self.series} - {self.part}", tags=self.tags, headless=not self.args.verbose)
        return uploaded
