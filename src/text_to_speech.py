import os
import base64
from typing import Optional
from speechify import Speechify
from speechify.tts import GetSpeechOptionsRequest


async def tts(final_text: str, voice: str = "en-US-ChristopherNeural", stdout: bool = False, outfile: str = "tts.mp3", args=None) -> bool:
    """
    Text-to-speech function using Speechify API with backward compatibility for edge-tts voice format.
    
    Args:
        final_text: Text to convert to speech
        voice: Voice ID (Speechify format) or edge-tts voice name (for backward compatibility)
        stdout: Whether to output to stdout (not supported in Speechify)
        outfile: Output file path
        args: Additional arguments (unused in Speechify implementation)
    
    Returns:
        bool: True if successful
    """
    # Get Speechify API key from environment
    api_key = os.getenv('SPEECHIFY_API_KEY')
    if not api_key:
        raise ValueError("SPEECHIFY_API_KEY environment variable is required")
    
    # Initialize Speechify client
    client = Speechify(token=api_key)
    
    # Convert edge-tts voice format to Speechify voice_id if needed
    voice_id = convert_edge_tts_voice_to_speechify(voice)
    
    # Determine language from voice or use auto-detection
    language = extract_language_from_voice(voice)
    
    # Choose model based on language
    model = "simba-multilingual" if language and language != "en" else "simba-english"
    
    try:
        # Generate speech using Speechify
        audio_response = client.tts.audio.speech(
            audio_format="mp3",
            input=final_text,
            language=language if language else None,  # None for auto-detection
            model=model,
            options=GetSpeechOptionsRequest(
                loudness_normalization=True,
                text_normalization=True
            ),
            voice_id=voice_id
        )
        
        # Decode and save audio
        audio_bytes = base64.b64decode(audio_response.audio_data)
        
        if not stdout:
            with open(outfile, 'wb') as f:
                f.write(audio_bytes)
        
        return True
        
    except Exception as e:
        print(f"Error generating speech: {e}")
        return False


def convert_edge_tts_voice_to_speechify(edge_tts_voice: str) -> str:
    """
    Convert edge-tts voice format to Speechify voice_id.
    Maps common edge-tts voices to Speechify voices.
    
    Args:
        edge_tts_voice: Voice name in edge-tts format
        
    Returns:
        str: Speechify voice_id
    """
    # Default mapping from edge-tts voices to Speechify voices
    voice_mapping = {
        "en-US-ChristopherNeural": "scott",  # Default male voice
        "en-US-JennyNeural": "sarah",        # Default female voice
        "en-US-GuyNeural": "scott",          # Male voice
        "en-US-AriaNeural": "sarah",         # Female voice
        "en-GB-RyanNeural": "scott",         # British male
        "en-GB-SoniaNeural": "sarah",        # British female
        "fr-FR-DeniseNeural": "sarah",       # French female
        "de-DE-KatjaNeural": "sarah",        # German female
        "es-ES-ElviraNeural": "sarah",       # Spanish female
        "pt-BR-FranciscaNeural": "sarah",    # Portuguese female
    }
    
    # If it's already a Speechify voice_id, return as is
    if edge_tts_voice in ["scott", "sarah"]:
        return edge_tts_voice
    
    # Try to map from edge-tts format
    if edge_tts_voice in voice_mapping:
        return voice_mapping[edge_tts_voice]
    
    # Default to scott if no mapping found
    return "scott"


def extract_language_from_voice(voice: str) -> Optional[str]:
    """
    Extract language code from edge-tts voice name.
    
    Args:
        voice: Voice name in edge-tts format
        
    Returns:
        Optional[str]: Language code or None if not found
    """
    # Extract language from edge-tts voice format (e.g., "en-US-ChristopherNeural")
    if "-" in voice:
        parts = voice.split("-")
        if len(parts) >= 2:
            lang_code = parts[0]
            region_code = parts[1]
            return f"{lang_code}-{region_code}"
    
    return None
