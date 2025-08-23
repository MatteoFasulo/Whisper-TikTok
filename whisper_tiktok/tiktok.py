"""Module for uploading videos to TikTok."""

import logging
import os

from tiktok_uploader.upload import upload_video

logger = logging.getLogger(__name__)


def upload_tiktok(file, title: str, tags: list, headless: bool = False):
    """Uploads a video to TikTok using the TikTok Uploader library.

    Args:
        file (str): Path to the video file.
        title (str): Title of the video.
        tags (list): List of tags to include in the description.
        headless (bool, optional): Whether to run the browser in headless mode.
    """
    if not os.path.isfile("cookies.txt"):
        logger.error("Cookie file not found")

    else:
        logger.info("Cookie file found")

        if len(tags) > 0:
            tags_string = " ".join([f"#{tag}" for tag in tags])
            description = f"{title} {tags_string}"
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
