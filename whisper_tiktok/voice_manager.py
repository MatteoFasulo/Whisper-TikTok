from typing import Any

import edge_tts


class VoicesManager:
    """Wrapper for edge_tts VoicesManager."""

    @staticmethod
    async def create():
        """Create and return voices manager object."""
        return await edge_tts.VoicesManager.create()

    @staticmethod
    def find(voices, gender: str, locale: str) -> Any:
        """Find a voice by gender and locale.

        Args:
            voices: Voices manager object from create()
            gender: Gender filter (Male/Female)
            locale: Language locale filter (e.g., en-US)

        Returns:
            Dictionary with voice information

        Raises:
            ValueError: If no voice found
        """
        result = voices.find(Gender=gender, Locale=locale)
        if not result or len(result) == 0:
            raise ValueError(f"No voice found for {gender} - {locale}")
        # Return the first result as a dict-like object
        return result[0]
