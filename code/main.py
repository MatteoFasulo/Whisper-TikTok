import platform
import asyncio
import random
import sys

import edge_tts
from edge_tts import VoicesManager

#######################
#        STATIC       #
#######################
series = "Crazy facts that you did not know"
part = 4
outro = "Follow us for more"
outfile = f"text_{part}.mp3"
path = f"{outfile}"

#######################
#         CODE        #
#######################
async def main():
    text = get_file_text()
    final_text = create_full_text(text)
    await tts(final_text, outfile=outfile)
    return True

def get_file_text(filename: str = "script.txt") -> str:
    with open(filename, 'r') as file:
        text = file.read().rstrip().replace('"',"'") # fix for "" in text
    return text

def create_full_text(text: str) -> str:
    final_text = f"{series} Part {part}.\n{text}\n{outro}"
    return final_text

async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", random_voice: bool = False, stdout: bool = False, outfile: str = "tts.mp3"):
    voices = await VoicesManager.create()
    if random_voice:
        voices = voices.find(Gender="Male", Locale="en-US")
        voice = random.choice(voices)["Name"]
    communicate = edge_tts.Communicate(final_text, voice)
    if not stdout:
        await communicate.save(outfile)
    return True

if __name__ == "__main__":
    if platform.system()=='Windows':
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    loop = asyncio.get_event_loop()
    try:
        loop.run_until_complete(main())
    finally:
        loop.close()