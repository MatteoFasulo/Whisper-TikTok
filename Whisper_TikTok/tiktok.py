import logging
import os

from tiktok_uploader.upload import upload_video

logger = logging.getLogger(__name__)


def upload_tiktok(file, title: str, tags: list, headless: bool = False):
    if not os.path.isfile("cookies.txt"):
        logger.error("Cookie file not found")

    else:
        logger.info("Cookie file found")

        if len(tags) > 0:
            tags = " ".join([f"#{tag}" for tag in tags])
            description = f"{title} {tags}"
        else:
            description = title

        try:
            upload_video(
                file,
                description=description,
                cookies="cookies.txt",
                comment=True,
                stitch=False,
                duet=False,
                headless=headless,
            )

        except Exception as e:
            logger.exception(e)
            return False

        return True
