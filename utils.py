import os

# Rich
from rich.console import Console

console = Console()

class KeepDir:
    def __init__(self):
        self.original_dir = os.getcwd()
    def __enter__(self):
        return self
    def __exit__(self, exc_type, exc_val, exc_tb):
        os.chdir(self.original_dir)
    def chdir(self, path):
        os.chdir(path)

def rich_print(text, style: str = ""):
    console.print(text, style=style)