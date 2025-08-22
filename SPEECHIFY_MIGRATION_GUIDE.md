# Speechify TTS Migration Guide

This document outlines the migration from Microsoft Edge TTS (edge-tts) to Speechify API in the Whisper-TikTok project.

## Overview

The migration replaces the edge-tts library with the Speechify API while maintaining backward compatibility with existing voice configurations.

## Changes Made

### 1. Dependencies Updated

**requirements.txt**
```diff
+ speechify-api
```

### 2. Environment Variables

**example.env**
```diff
+ SPEECHIFY_API_KEY=
```

### 3. Core TTS Implementation

**src/text_to_speech.py**
- Replaced edge-tts with Speechify API
- Added voice conversion mapping for backward compatibility
- Added language detection and model selection
- Maintained the same function signature for compatibility

### 4. Voice Management

**src/voice_manager.py**
- Replaced edge-tts VoicesManager with Speechify implementation
- Added voice filtering functionality
- Maintained backward compatibility with existing voice selection logic

### 5. Argument Parser

**src/arg_parser.py**
- Updated voice listing functionality
- Added Speechify voice validation
- Maintained existing command-line interface

### 6. Streamlit Interface

**app.py**
- Updated voice selection to use Speechify voices
- Added fallback for when Speechify is unavailable
- Maintained existing UI structure

## Backward Compatibility

The migration maintains full backward compatibility with existing configurations:

### Voice Format Support

The system now supports both formats:

1. **Speechify Voice IDs**: Direct Speechify voice identifiers (e.g., "scott", "sarah")
2. **Edge-TTS Format**: Legacy edge-tts voice names (e.g., "en-US-ChristopherNeural")

### Voice Mapping

Common edge-tts voices are automatically mapped to Speechify equivalents:

| Edge-TTS Voice | Speechify Voice |
|----------------|-----------------|
| en-US-ChristopherNeural | scott |
| en-US-JennyNeural | sarah |
| en-US-GuyNeural | scott |
| en-US-AriaNeural | sarah |
| en-GB-RyanNeural | scott |
| en-GB-SoniaNeural | sarah |
| fr-FR-DeniseNeural | sarah |
| de-DE-KatjaNeural | sarah |
| es-ES-ElviraNeural | sarah |
| pt-BR-FranciscaNeural | sarah |

## New Features

### 1. Enhanced Language Support

Speechify supports more languages than edge-tts:

**Fully Supported Languages:**
- English (en)
- French (fr-FR)
- German (de-DE)
- Spanish (es-ES)
- Portuguese (Brazil) (pt-BR)
- Portuguese (Portugal) (pt-PT)

**Beta Languages:**
- Arabic, Danish, Dutch, Estonian, Finnish, Greek, Hebrew, Hindi, Italian, Japanese, Norwegian, Polish, Russian, Swedish, Turkish, Ukrainian, Vietnamese

### 2. Automatic Language Detection

When the `language` parameter is not specified, Speechify automatically detects the language in the input text.

### 3. Model Selection

The system automatically chooses the appropriate model:
- `simba-english` for English content
- `simba-multilingual` for other languages

### 4. Voice Filtering

Enhanced voice filtering capabilities:
- Filter by gender (male/female)
- Filter by locale (e.g., en-US, fr-FR)
- Filter by tags (e.g., timbre:deep, use-case:advertisement)

## Setup Instructions

### 1. Install Dependencies

```bash
pip install -r requirements.txt
```

### 2. Set Environment Variables

Create a `.env` file based on `example.env`:

```env
SPEECHIFY_API_KEY=your_speechify_api_key_here
```

### 3. Get Speechify API Key

1. Sign up at https://console.sws.speechify.com/signup
2. Generate an API key from your dashboard
3. Add the key to your `.env` file

## Usage Examples

### Command Line

**Basic usage (backward compatible):**
```bash
python main.py --tts "en-US-ChristopherNeural"
```

**Using Speechify voice ID:**
```bash
python main.py --tts "scott"
```

**Random voice selection:**
```bash
python main.py --random_voice --gender Male --language en-US
```

**List available voices:**
```bash
python main.py --list-voices
```

### Streamlit Interface

The web interface automatically loads available Speechify voices and provides a dropdown selection.

## Testing

Run the comprehensive test suite:

```bash
python test_speechify_migration.py
```

The test suite covers:
- Voice conversion functionality
- Language detection
- TTS generation
- Voice management
- Backward compatibility
- Error handling

## Migration Checklist

- [x] Update dependencies
- [x] Add Speechify API key to environment variables
- [x] Implement Speechify TTS functionality
- [x] Update voice management
- [x] Maintain backward compatibility
- [x] Update command-line interface
- [x] Update Streamlit interface
- [x] Create comprehensive test suite
- [x] Update documentation

## Potential Issues and Solutions

### 1. Missing API Key

**Error:** `ValueError: SPEECHIFY_API_KEY environment variable is required`

**Solution:** Set the `SPEECHIFY_API_KEY` environment variable in your `.env` file.

### 2. Voice Not Found

**Error:** `Specified TTS voice not found`

**Solution:** Use `python main.py --list-voices` to see available voices, or use a Speechify voice ID directly.

### 3. Language Detection Issues

**Issue:** Incorrect language detection for mixed-language content

**Solution:** Explicitly specify the `language` parameter when you know the content language.

### 4. Audio Quality Differences

**Issue:** Audio quality may differ from edge-tts

**Solution:** Speechify provides high-quality audio. Adjust the `loudness_normalization` and `text_normalization` options if needed.

## Performance Considerations

### API Rate Limits

Speechify has rate limits based on your plan. Monitor your usage to avoid hitting limits.

### Audio Format

The system uses MP3 format by default. Other formats (aac, ogg, wav) are supported but may require additional configuration.

### Caching

Consider implementing audio caching for frequently used text to reduce API calls and improve performance.

## Troubleshooting

### Common Issues

1. **Import Errors**: Ensure `speechify-api` is installed
2. **Authentication Errors**: Verify your API key is correct
3. **Voice Not Available**: Check if the voice is available in your Speechify plan
4. **Language Not Supported**: Use a supported language or enable auto-detection

### Debug Mode

Enable verbose output to see detailed error messages:

```bash
python main.py --verbose
```

## Support

For issues related to:
- **Speechify API**: Contact Speechify support
- **Migration Issues**: Check the test suite and migration guide
- **General Usage**: Refer to the main project documentation

## Future Enhancements

Potential improvements for future versions:
- Audio caching system
- Batch processing capabilities
- Custom voice training integration
- Advanced audio post-processing
- Multi-language video support 