# utils.py
import asyncio
import csv
import platform
from dotenv import find_dotenv, load_dotenv
from utils import *

# msg.py
import msg

# arg_parser.py
from src.arg_parser import parse_args

# video_creator.py
from src.video_creator import ClipMaker

# Default directory
HOME = Path.cwd()

# List of clips to generate
video_csv = HOME / 'clips.csv'
video_data = csv.DictReader(open(video_csv, 'r', encoding='utf-8'), delimiter='|')


#######################
#         CODE        #
#######################


async def main(video_list) -> bool:
    console.clear()  # Clear terminal

    args = await parse_args()

    for video in video_list:
        with console.status(msg.STATUS) as status:

            # Load env vars (if any)
            load_dotenv(find_dotenv())

            console.log(f"{msg.OK}Finish loading environment variables")

            video_creator = ClipMaker(video, args)
            video_creator.download_background_video()
            video_creator.load_model()
            video_creator.merge_clip_text()
            await video_creator.text_to_speech()
            video_creator.generate_transcription()
            video_creator.select_background()
            video_creator.integrate_subtitles()
            if args.upload_tiktok:
                video_creator.upload_to_tiktok()

        console.log(f'{msg.DONE} {str(video_creator.mp4_final_video)}')
    return True


if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main(video_list=video_data))

    loop.close()

    sys.exit(0)
