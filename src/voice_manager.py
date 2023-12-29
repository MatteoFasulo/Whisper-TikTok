import sys

import edge_tts


class VoicesManager:
    @staticmethod
    async def create():
        return await edge_tts.VoicesManager.create()

    @staticmethod
    def find(voices, Gender, Locale):
        voices = voices.find(Gender=Gender, Locale=Locale)
        if len(voices) == 0:
            print(f"Specified TTS language not found. Make sure you are using the correct format. For example: en-US")
            sys.exit(1)
        return voices['Name']
