# Getting Started

## Table of Contents

1. [Introduction](#introduction)
2. [Demo Video](#demo-video)
3. [Operating Principle](#operating-principle)
    - [In-Depth Insights](#in-depth-insights)
4. [Prerequisites](#prerequisites)
5. [Usage Guidelines](#usage-guidelines)
    - [Command-Line Options](#command-line-options)
6. [Usage Examples](#usage-examples)
7. [Code of Conduct](#code-of-conduct)
8. [Contributing](#contributing)
9. [Upcoming Features](#upcoming-features)
10. [OpenAI Whisper Forum Discussion](#openai-whisper-forum-discussion)
11. [Acknowledgments](#acknowledgments)

## 1. Introduction <a name="introduction"></a>

Welcome to Whisper-TikTok, an innovative AI-powered tool that utilizes Edge TTS, OpenAI-Whisper, and FFMPEG to create captivating TikTok videos. This documentation provides insights into how to use Whisper-TikTok effectively.

## 2. Demo Video <a name="demo-video"></a>

Explore Whisper-TikTok in action by watching our [Demo Video](https://github.com/MatteoFasulo/Whisper-TikTok/assets/74818541/68e25504-c305-4144-bd39-c9acc218c3a4).

## 3. Operating Principle <a name="operating-principle"></a>

Whisper-TikTok's operating principle involves several key steps:

- Modify the `video.json` file to specify video details.
- The program processes the JSON data and generates a TikTok video based on the provided information.
- The program leverages OpenAI's Whisper model for transcription and Microsoft Edge Cloud TTS API for voiceovers.

### In-Depth Insights <a name="in-depth-insights"></a>

Whisper-TikTok performs the following sequence of actions:

1. Retrieval of environment variables.
2. Validation of PyTorch and CUDA installation.
3. Downloading a background video from platforms like YouTube.
4. Loading the OpenAI Whisper model into memory.
5. Initiating a Text-to-Speech request to the Microsoft Edge Cloud TTS API.
6. Generating a detailed transcription of the audio.
7. Selecting a random background video.
8. Integrating subtitles into the background video using FFMPEG.
9. Voila! You've created a captivating TikTok video.

## 4. Prerequisites <a name="prerequisites"></a>

To use Whisper-TikTok, ensure you have the following prerequisites:

- Python versions 3.8 or 3.9
- ffmpeg command-line tool installed on your system
- A GPU for optimal performance (although the program can run without one)

## 5. Usage Guidelines <a name="usage-guidelines"></a>

To get started with Whisper-TikTok, follow these guidelines:

- Run the following command in your terminal to start the program:

  ```bash
  python main.py
  ```

### Command-Line Options <a name="command-line-options"></a>

Whisper-TikTok supports the following command-line options:

- `--model`: Choose the Whisper model size (e.g., small, medium).
- `--non_english`: Do not use the English model.
- `--url`: Specify a custom YouTube URL for the background video.
- `--tts`: Select the voice for Text-to-Speech.
- `--list-voices`: List all available voices.
- `--random_voice`: Use a random TTS voice (requires specifying gender and language).
- `--gender`: Specify the gender of the random TTS voice (Male or Female).
- `--language`: Specify the language of the random TTS voice.

## 6. Usage Examples <a name="usage-examples"></a>

Here are some usage examples of Whisper-TikTok:

- Generate a TikTok video with a specific TTS model and voice:

  ```bash
  python main.py --model medium --tts en-US-EricNeural
  ```

- Generate a TikTok video without using the English model:

  ```bash
  python main.py --non_english --tts de-DE-KillianNeural
  ```

- Use a custom YouTube video as the background:

  ```bash
  python main.py --url https://www.youtube.com/watch?v=dQw4w9WgXcQ --tts en-US-JennyNeural
  ```

- Generate a TikTok video with a random TTS voice:

  ```bash
  python main.py --random_voice --gender Male --language en-US
  ```

## 7. Code of Conduct <a name="code-of-conduct"></a>

Please review our [Code of Conduct](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/CODE_OF_CONDUCT.md) before contributing to Whisper-TikTok.

## 8. Contributing <a name="contributing"></a>

We welcome contributions from the community! Please see our [Contributing Guidelines](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/CONTRIBUTING.md) for more information.

## 9. Upcoming Features <a name="upcoming-features"></a>

Stay tuned for these upcoming features in Whisper-TikTok:

- Integration with the OpenAI API for advanced responses.
- Integration with the TikTok Developer API for direct uploads.
- Improved user interface for a seamless experience.

## 10. OpenAI Whisper Forum Discussion <a name="openai-whisper-forum-discussion"></a>

Join the discussion on OpenAI Whisper in our [Forum Discussion](https://github.com/openai/whisper/discussions/223).

## 11. Acknowledgments <a name="acknowledgments"></a>

We extend our thanks to the following contributors and packages that have made Whisper-TikTok possible:

- [@rany2](https://www.github.com/rany2) for the [edge-tts](https://github.com/rany2/edge-tts) package.
- [@OpenAI](https://github.com/openai/whisper) for the Whisper model.

## 12. License <a name="license"></a>

Whisper-TikTok is licensed under the [Apache License, Version 2.0](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/LICENSE).
