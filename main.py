# utils.py
import asyncio
import platform
from dotenv import find_dotenv, load_dotenv
from utils import *

# msg.py
import msg

# logger.py
from src.logger import setup_logger

# arg_parser.py
from src.arg_parser import parse_args

# video_creator.py
from src.video_creator import VideoCreator

# Default directory
HOME = Path.cwd()

# Logging
logger = setup_logger()


#######################
#         CODE        #
#######################


async def main() -> bool:
    console.clear()  # Clear terminal

    args = await parse_args()

    logger.debug('Creating video')
    with console.status(msg.STATUS) as status:
        load_dotenv(find_dotenv())  # Optional

        console.log(
            f"{msg.OK}Finish loading environment variables")
        logger.info('Finish loading environment variables')

        video_creator = VideoCreator(args)
        video_creator.download_video()
        video_creator.load_model()
        video_creator.create_text()
        await video_creator.text_to_speech()
        video_creator.generate_transcription()
        video_creator.select_background()
        video_creator.integrate_subtitles()
        if args.upload_tiktok:
            video_creator.upload_to_tiktok()

    console.log(f'{msg.DONE}')
    return 0


if __name__ == "__main__":

    if platform.system() == 'Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

    loop = asyncio.get_event_loop()

    loop.run_until_complete(main())

    loop.close()

    sys.exit(0)
