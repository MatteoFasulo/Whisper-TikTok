from pathlib import Path

import stable_whisper as whisper

# Local imports
from .subtitle_creator import srt_create
from .text_to_speech import tts
from .tiktok import upload_tiktok
from .video_prepare import prepare_background
from .video_downloader import download_video as youtube_download
from utils import *

HOME = Path.cwd()
media_folder = HOME / 'media'


class ClipMaker:
    def __init__(self, clip: dict, args):
        self.clip = clip
        self.args = args

        # Fetch clip data or set default values
        self.series = clip.get('series', 'Crazy facts that you did not know')
        self.part = clip.get('part', '1')
        self.text = clip.get('text', 'The first person to survive going over Niagara Falls in a barrel was a 63-year-old school teacher')
        self.tags = clip.get('tags', ['survive', 'Niagara Falls', 'facts'])
        self.outro = clip.get('outro', 'I hope you enjoyed this video. If you did, please give it a thumbs up and subscribe to my channel. I will see you in the next video.')

        # Set media folder path
        self.path = Path(media_folder).absolute()

    def download_background_video(self, folder='background') -> None:
        # Download background video for the clip
        youtube_download(url=self.args.url, folder=folder)

        console.log(f"{msg.OK}Video downloaded from {self.args.url} to {folder}")
        return None

    def load_model(self):
        # Load Whisper model
        model = self.args.model
        
        if self.args.model != "large" and not self.args.non_english:
            model = self.args.model + ".en"

        whisper_model = whisper.load_model(model)

        # Set model to class attribute
        self.model = whisper_model
        return whisper_model

    def merge_clip_text(self) -> tuple:
        # Merge clip series, part, text and outro to create a single text for the clip
        req_text = f"{self.series} - Part {self.part}.\n{self.text}\n{self.outro}" # TODO: allow user to customize this

        # Remove whitespaces from series name and create a folder for the series
        series = self.series.replace(' ', '_')
        filename = f"{self.path}{os.sep}{series}{os.sep}{series}_{self.part}.mp3"

        # Create series folder if it does not exist
        Path(f"{self.path}{os.sep}{series}").mkdir(parents=True, exist_ok=True)

        # Set class attributes for text and mp3 (audio) file
        self.req_text = req_text
        self.mp3_file = filename
        return req_text, filename

    async def text_to_speech(self) -> None:
        # Convert text to speech using the selected TTS voice
        await tts(self.req_text, outfile=self.mp3_file, voice=self.args.tts, args=self.args)
        return None

    def generate_transcription(self) -> Path:
        # Generate subtitles for the clip using the Whisper model
        ass_filename = srt_create(self.model,
                                  self.path, self.series, self.part, self.mp3_file, **vars(self.args))

        # Get the absolute path of .ass file
        ass_filename = Path(ass_filename).absolute()

        # Set class attribute for .ass style file of subtitles
        self.ass_file = ass_filename
        return ass_filename

    def select_background(self, random: bool = True) -> Path:
        # Select which background video to use for the clip
        try:
            # Background video selected with WebUI for Streamlit
            # Add to the path the parent folder (background)
            background_file = self.args.mp4_background
            background_mp4 = Path(HOME / 'background' / background_file) # Concat path
            background_mp4 = background_mp4.absolute()

        except AttributeError: # Local CLI execution
            if random:
                background_mp4 = random_background()
                
            else: # TODO: allow the user to select which background video to use
                pass

        # Set class attribute for mp4 background file
        self.mp4_background = background_mp4
        return background_mp4

    def integrate_subtitles(self) -> Path:
        # Use FFMPEG to integrate subtitles into background video and trim everything with fixed length of the audio file
        final_video = prepare_background(str(self.mp4_background), filename_mp3=self.mp3_file, filename_srt=str(self.ass_file), verbose=self.args.verbose)
        final_video = Path(final_video).absolute()

        # Set class attribute for mp4 final clip file
        self.mp4_final_video = final_video
        return final_video

    def upload_to_tiktok(self) -> bool: # TODO: check if still working with Cookie
        # Automatic upload on TikTok
        uploaded = upload_tiktok(str(self.mp4_final_video), title=f"{self.series} - {self.part}", tags=self.tags, headless=not self.args.verbose)
        return uploaded
