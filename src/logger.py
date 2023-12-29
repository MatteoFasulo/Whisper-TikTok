import os
import datetime
import logging
from pathlib import Path


class KeepDir:
    def __init__(self):
        self.original_dir = os.getcwd()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_dir)

    def chdir(self, path):
        os.chdir(path)


def setup_logger():
    HOME = Path.cwd()
    log_directory = HOME / 'log'
    if not log_directory.exists():
        log_directory.mkdir()

    with KeepDir() as keep_dir:
        keep_dir.chdir(log_directory)
        log_filename = f'{datetime.date.today()}.log'
        logging.basicConfig(
            level=logging.INFO,
            format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
            handlers=[
                logging.FileHandler(log_filename),
            ]
        )
        logger = logging.getLogger(__name__)
    return logger
