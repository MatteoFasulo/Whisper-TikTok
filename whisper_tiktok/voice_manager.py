"""Module for managing voice synthesis using edge-tts."""

import sys
import edge_tts


class VoicesManager:
    """
    A class for managing voices using edge-tts.

    This class provides methods for creating and finding voices based on gender and locale.
    """

    @staticmethod
    async def create():
        """Asynchronously retrieves available voices using edge-tts.

        Returns:
            typing.List[edge_tts.Voice]: A list of available voices.
        """
        return await edge_tts.VoicesManager.create()

    @staticmethod
    def find(voices, gender, locale):
        """Finds a voice based on gender and locale.

        Args:
            voices: A list of available voices.
            gender: The desired gender of the voice.
            locale: The desired locale of the voice.

        Returns:
            The name of the found voice.

        Raises:
            SystemExit: If no voice is found with the specified gender and locale.
        """
        voices = voices.find(Gender=gender, Locale=locale)
        if len(voices) == 0:
            print("Specified TTS language not found. Make sure you are using the correct format!")
            sys.exit(1)
        return voices["Name"]
