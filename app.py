from pathlib import Path
import asyncio
import json
import platform
import sys
from argparse import Namespace

import edge_tts

import gradio as gr

from src.video_creator import VideoCreator
from utils import rgb_to_bgr


async def generate_video(
        model,
        tts_voice,
        sub_position,
        font,
        font_color,
        font_size,
        url,
        non_english,
        upload_tiktok,
        verbose,
        video_json,
        background_tab,
        video_num,
        *args,
        **kwargs):

    args = Namespace(
        model=model,
        tts=tts_voice.split('|')[0].strip(),
        font=font,
        font_color=rgb_to_bgr(font_color.lower()),
        font_size=font_size,
        sub_position=sub_position,
        url=url,
        non_english=non_english,
        upload_tiktok=upload_tiktok,
        verbose=verbose,
        mp4_background=background_tab,
    )

    async def get_video(video_data, args):
        video_creator = VideoCreator(video_data, args)

        video_creator.download_video()

        video_creator.load_model()

        video_creator.create_text()

        await video_creator.text_to_speech()

        video_creator.generate_transcription()

        video_creator.select_background()

        video_creator.integrate_subtitles()

        if upload_tiktok:
            video_creator.upload_to_tiktok()

        return video_creator.mp4_final_video

    tasks = [get_video(video_json[i], args) for i in video_num]
    results = await asyncio.gather(*tasks)

    if len(results) == 1:
        return results[0]

    else:
        return results[-1]


async def main():

    # Model
    model = gr.Dropdown(["tiny", "base", "small", "medium"],
                        label="Whisper Model", value="small", interactive=True, info="The model used to generate the subtitles. The bigger the model, the better the results, but the slower the generation. The tiny model is recommended for testing purposes. Medium model is enough for good results in many languages.")

    # TTS
    tts_voice = gr.Dropdown(
        [f"{i['ShortName']} | {i['Gender']} | Tags: {i['VoiceTag']['VoicePersonalities']}" for i in await edge_tts.list_voices()], label="TTS Voice",
        value="en-US-ChristopherNeural | Male | Tags: ['Reliable', 'Authority']", interactive=True, info="The voice used to generate the audio. The voice must be in the same language as the subtitles.")

    # Subtitle position
    sub_position = gr.Slider(
        label="Subtitle alignment (position)", minimum=1, maximum=9, value=5, interactive=True, step=1, info="The position of the subtitles. 1 is the bottom left corner, 5 is the center, 9 is the top right corner. This is the alignment feature of FFMPEG subtitles.")

    # Subtitle font
    font = gr.Dropdown(
        ["Lexend Bold", "Lexend Regular", "Arial", "Roboto", "Big Condensed Black"], label="Font", value="Lexend Bold", interactive=True, info="The font used to generate the subtitles")

    # Subtitle font color
    font_color = gr.Textbox(
        label="Font Color", placeholder="FFF000", value="FFF000", interactive=True, info="The color of the subtitles in hexadecimal format. For example, FFF000 is yellow.")

    # Subtitle font size
    font_size = gr.Slider(
        label="Font Size", minimum=15, maximum=50, value=21, interactive=True, step=1, info="The font size for the subtitles. It is recommended to use a font size between 18 and 21.")

    # Background Video URL
    url = gr.Textbox(label="URL Background Video", placeholder="https://www.youtube.com/watch?v=intRX7BRA90",
                     value="https://www.youtube.com/watch?v=dQw4w9WgXcQ", interactive=True, info="The URL of the background video to use for the TikTok video")

    # Non-english
    non_english = gr.Checkbox(
        label="Non-english model", info="Use this if you are using a non-english model, otherwise leave it unchecked")

    # Upload to TikTok
    upload_tiktok = gr.Checkbox(label="Upload to TikTok", info="Upload the video to TikTok using the TikTok session cookie. For this step it is required to have a TikTok account and to be logged in on your browser. Then the required cookies.txt file can be generated using this guide (https://github.com/kairi003/Get-cookies.txt-LOCALLY). The cookies.txt file must be placed in the root folder of the project.")

    # Verbose
    verbose = gr.Checkbox(
        label="Verbose", info="Print the output of the commands used to create the video on your terminal. Useful for debugging.", interactive=True)

    video_json = gr.JSON(value=json.load(open("video.json", "r")),
                         label="video.json")

    # Get the list of files in "background"
    folder_path = Path("background").absolute()
    files = folder_path.glob('*.mp4')
    files = [file.name for file in files]

    # Create a Dropdown with the list of files
    background_tab = gr.Dropdown(
        label="Your Backgrounds", choices=files, info="List of all your downloaded backgrounds.", interactive=True)

    # Choose which video to generate
    videos = video_json.value

    video_num = gr.Dropdown(
        label="Video",
        choices=[f"{video['series']} - {video['part']}" for video in videos],
        info="Choose which video to generate from video.json file.",
        type="index",
        multiselect=True,
        value=[0],
        interactive=True
    )

    demo = gr.Interface(
        fn=generate_video,
        inputs=[
            model,
            tts_voice,
            sub_position,
            font,
            font_color,
            font_size,
            url,
            non_english,
            upload_tiktok,
            verbose,
            video_json,
            background_tab,
            video_num,
        ],
        outputs="video",
        title="🏆 Whisper-TikTok 🚀",
        description="Create a TikTok video with text-to-speech of Microsoft Edge's TTS and subtitles of Whisper model.",
        article="",
    )

    demo.launch(share=False)

if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    loop.close()

    sys.exit(0)
