import sys
import os
from typing import List, Optional
from speechify import Speechify


class VoicesManager:
    def __init__(self):
        self.api_key = os.getenv('SPEECHIFY_API_KEY')
        if not self.api_key:
            raise ValueError("SPEECHIFY_API_KEY environment variable is required")
        self.client = Speechify(token=self.api_key)
    
    @staticmethod
    async def create():
        """Create a VoicesManager instance (maintains backward compatibility)"""
        return VoicesManager()
    
    @staticmethod
    async def find(voices_manager, Gender: str, Locale: str) -> dict:
        """
        Find voices by gender and locale (maintains backward compatibility with edge-tts format).
        
        Args:
            voices_manager: VoicesManager instance
            Gender: Gender filter ('Male' or 'Female')
            Locale: Language locale (e.g., 'en-US')
            
        Returns:
            dict: Voice information in edge-tts compatible format
        """
        try:
            # Get all available voices from Speechify
            voices_response = voices_manager.client.tts.voices.list()
            voices = voices_response.voices
            
            # Filter voices based on gender and locale
            matching_voices = filter_voice_models(
                voices, 
                gender=Gender.lower(), 
                locale=Locale
            )
            
            if not matching_voices:
                print(f"Specified TTS language not found. Make sure you are using the correct format. For example: en-US")
                sys.exit(1)
            
            # Return the first matching voice in edge-tts compatible format
            voice_id = matching_voices[0]
            return {'Name': voice_id}
            
        except Exception as e:
            print(f"Error fetching voices: {e}")
            sys.exit(1)
    
    def get_available_voices(self) -> List[dict]:
        """
        Get all available voices from Speechify.
        
        Returns:
            List[dict]: List of voice information
        """
        try:
            voices_response = self.client.tts.voices.list()
            voices = voices_response.voices
            
            voice_list = []
            for voice in voices:
                for model in voice.models:
                    for lang in model.languages:
                        voice_info = {
                            'ShortName': model.name,
                            'Gender': voice.gender,
                            'VoiceTag': {
                                'VoicePersonalities': ', '.join(voice.tags) if voice.tags else 'None'
                            },
                            'Locale': lang.locale,
                            'Language': lang.language
                        }
                        voice_list.append(voice_info)
            
            return voice_list
            
        except Exception as e:
            print(f"Error fetching voices: {e}")
            return []


def filter_voice_models(voices, *, gender=None, locale=None, tags=None):
    """
    Filter Speechify voices by gender, locale, and/or tags,
    and return the list of model IDs for matching voices.

    Args:
        voices (list): List of GetVoice objects.
        gender (str, optional): e.g. 'male', 'female'.
        locale (str, optional): e.g. 'en-US'.
        tags (list, optional): list of tags, e.g. ['timbre:deep', 'use-case:advertisement'].

    Returns:
        list[str]: IDs of matching voice models.
    """
    results = []

    for voice in voices:
        # gender filter
        if gender and voice.gender.lower() != gender.lower():
            continue

        # locale filter (check across models and languages)
        if locale:
            if not any(
                any(lang.locale == locale for lang in model.languages)
                for model in voice.models
            ):
                continue

        # tags filter
        if tags:
            if not all(tag in voice.tags for tag in tags):
                continue

        # If we got here, the voice matches -> collect model ids
        for model in voice.models:
            results.append(model.name)

    return results
