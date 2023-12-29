import json
import subprocess
from pathlib import Path

import stable_whisper as whisper
from .logger import setup_logger
from .subtitle_creator import srt_create, highlight_words
from .text_to_speech import tts
from .tiktok import upload_tiktok
from .video_prepare import prepare_background
from utils import *

HOME = Path.cwd()
logger = setup_logger()
video_json_path = HOME / 'video.json'
jsonData = json.loads(video_json_path.read_text(encoding='utf-8'))
media_folder = HOME / 'media'


class VideoCreator:
    def __init__(self, args):
        self.args = args

        self.series = jsonData.get('series', '')
        self.part = jsonData.get('part', '')
        self.text = jsonData.get('text', '')
        self.tags = jsonData.get('tags', list())
        self.outro = jsonData.get('outro', '')
        self.path = Path(media_folder).absolute()

    def download_video(self, folder: str = 'background'):
        directory = HOME / folder
        if not directory.exists():
            directory.mkdir()

        with KeepDir() as keep_dir:
            keep_dir.chdir(folder)
            subprocess.run(['yt-dlp', '-f bestvideo[ext=mp4]+bestaudio[ext=m4a]',
                            '--restrict-filenames', self.args.url], check=True)
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
        srt_filename = srt_create(
            self.model, self.path, self.series, self.part, self.text, self.mp3_file)
        srt_filename = Path(srt_filename).absolute()

        self.srt_file = srt_filename

        highlight_words(self.srt_file, subtitle_format=self.args.sub_format,
                        font_color=self.args.font_color)
        return srt_filename

    def select_background(self):
        background_mp4 = random_background()

        self.mp4_backgroung = background_mp4
        return background_mp4

    def integrate_subtitles(self):
        final_video = prepare_background(
            self.mp4_backgroung, filename_mp3=self.mp3_file, filename_srt=self.srt_file, verbose=self.args.verbose)
        final_video = Path(final_video).absolute()

        self.mp4_final_video = final_video
        return final_video

    def upload_to_tiktok(self):
        uploaded = upload_tiktok(str(
            self.mp4_final_video), title=f"{self.series} - {self.part}", tags=self.tags, headless=not self.args.verbose)
        return uploaded
