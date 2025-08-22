# Introducing Whisper-TikTok 🤖🎥

## Table of Contents

1. [Introduction](#introduction)
2. [Demo Video](#demo-video)
3. [Operating Principle](#operating-principle)
    - [In-Depth Insights](#in-depth-insights)
4. [Installation](#installation)
5. [Usage Guidelines](#usage-guidelines)
    - [Command-Line Options](#command-line-options)
6. [Usage Examples](#usage-examples)
7. [Code of Conduct](#code-of-conduct)
8. [Contributing](#contributing)
9. [Upcoming Features](#upcoming-features)
10. [OpenAI Whisper Forum Discussion](#openai-whisper-forum-discussion)
11. [Acknowledgments](#acknowledgments)

## Introduction
Discover Whisper-TikTok, an innovative AI-powered tool that leverages the prowess of **Edge TTS**, **OpenAI-Whisper**, and **FFMPEG** to craft captivating TikTok videos. Harnessing the capabilities of OpenAI's Whisper model, Whisper-TikTok effortlessly generates an accurate **transcription** from provided audio files, laying the foundation for the creation of mesmerizing TikTok videos through the utilization of **FFMPEG**. Additionally, the program seamlessly integrates the **Microsoft Edge Cloud Text-to-Speech (TTS) API** to lend a vibrant **voiceover** to the video. Opting for Microsoft Edge Cloud TTS API's voiceover is a deliberate choice, as it delivers a remarkably **natural and authentic** auditory experience, setting it apart from the often monotonous and artificial voiceovers prevalent in numerous TikTok videos.

## Streamlit Web App

![Webui](docs/WebuiDemo.png)

## Demo Video

<https://github.com/MatteoFasulo/Whisper-TikTok/assets/74818541/68e25504-c305-4144-bd39-c9acc218c3a4>

## How it Works

Employing Whisper-TikTok is a breeze: simply modify the [clips.csv](clips.csv). The CSV file contains the following attributes:

- `series`: The name of the series.
- `part`: The part number of the video.
- `text`: The text to be spoken in the video.
- `tags`: The tags to be used for the video.
- `outro`: The outro text to be spoken in the video.

<details>
<summary>Details</summary>

The program conducts the **sequence of actions** outlined below:

## 4. Installation <a name="installation"></a>

Whisper-TikTok has been tested in Windows 10, Windows 11 and Ubuntu 23.04 systems equipped with **Python versions 3.9, 3.10, and 3.11**.

First clone the repository

```bash
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git
```

Then, navigate to the Whisper-TikTok directory:

```bash
cd Whisper-TikTok
```

It is highly recommended to use a virtual environment. Create one using:

```bash
python -m venv whisper-tiktok-env
```

Activate the virtual environment:

- On Windows:

  ```bash
  whisper-tiktok-env\Scripts\activate
  ```

- On Ubuntu:

  ```bash
  source whisper-tiktok-env/bin/activate
  ```

Install the required dependencies:

```bash
pip install -r requirements.txt
```

There is a Web App hosted thanks to Streamlit which is public available in HuggingFace, just click on the link that will take you directly to the Web App.
> https://huggingface.co/spaces/MatteoFasulo/Whisper-TikTok-Demo

To use Whisper-TikTok, follow these guidelines:

- Ensure you have a stable internet connection for downloading videos and uploading to TikTok.
- Have your TikTok session cookie ready for video uploads.
- Familiarize yourself with the command-line options for advanced usage.

```bash
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git
```

> However, there is also a Docker image available for Whisper-TikTok which can be used to run the program in a containerized environment.

# Dependencies

To streamline the installation of necessary dependencies, execute the following command within your terminal:

```python
pip install -U -r requirements.txt
```

It also requires the command-line tool [**FFMPEG**](https://ffmpeg.org/) to be installed on your system, which is available from most package managers:

```bash
# on Ubuntu or Debian

sudo apt update && sudo apt install ffmpeg

# on Arch Linux

sudo pacman -S ffmpeg

# on MacOS using Homebrew (<https://brew.sh/>)

brew install ffmpeg

# on Windows using Chocolatey (<https://chocolatey.org/>)

choco install ffmpeg

# on Windows using Scoop (<https://scoop.sh/>)

scoop install ffmpeg
```

> Please note that for optimal performance, it's advisable to have a GPU when using the OpenAI Whisper model for Automatic Speech Recognition (ASR). However, the program will also work without a GPU, but it will run more slowly.

## Web-UI (Local)

To run the Web-UI locally, execute the following command within your terminal:

```bash
streamlit run app.py
```

## Command-Line

To run the program from the command-line, execute the following command within your terminal:

```bash
python main.py 
```

### CLI Options

Whisper-TikTok offers several command-line options:

- `--help`: Show help message and exit.
- `--version`: Show program's version number and exit.
- `--input INPUT`: Specify the input JSON file. Default is `video.json`.
- `--output OUTPUT`: Specify the output video file. Default is `output.mp4`.
- `--tiktok-cookie TIKTOK_COOKIE`: Specify your TikTok session cookie.

Options:
  --model TEXT              Model to use [tiny|base|small|medium|large] (Default: small)
  --non_english             Use general model, not the English one specifically. (Flag)
  --url TEXT                YouTube URL to download as background video. (Default: <https://www.youtube.com/watch?v=intRX7BRA90>)
  --tts TEXT                Voice to use for TTS (Default: en-US-ChristopherNeural)
  --list-voices             Use `edge-tts --list-voices` to list all voices.
--random_voice              Random voice for TTS (Flag)
  --gender TEXT             Gender of the random TTS voice [Male|Female].
  --language TEXT           Language of the random TTS voice(e.g., en-US)
  --sub_format TEXT         Subtitle format to use [u|i|b] (Default: b) | b (Bold), u (Underline), i (Italic)
  --sub_position INT        Subtitle position to use [1-9] (Default: 5)
  --font TEXT               Font to use for subtitles (Default: Lexend Bold)
  --font_color TEXT         Font color to use for subtitles in HEX format (Default: #FFF000).
  --font_size INT           Font size to use for subtitles (Default: 21)
  --max_characters INT      Maximum number of characters per line (Default: 38)
  --max_words INT           Maximum number of words per segment (Default: 2)
  --upload_tiktok           Upload the video to TikTok (Flag)
  -v, --verbose             Verbose (Flag)
```

Here are some examples of how to use Whisper-TikTok:

- Basic usage with default settings:

  ```bash
  python -m Whisper_TikTok.main
  ```

- Specifying a custom input file and output file:

  ```bash
  python -m Whisper_TikTok.main --input my_video.json --output my_video.mp4
  ```

- Using your TikTok session cookie:

  ```bash
  python -m Whisper_TikTok.main --tiktok-cookie my_tiktok_cookie
  ```

- List all available voices:

This project adheres to a Code of Conduct. By participating, you are expected to uphold this code. Please report any unacceptable behavior to the project maintainers.

## Additional Resources

Contributions are welcome! Please follow these steps to contribute:

1. Fork the repository.
2. Create a new branch for your feature or bugfix.
3. Make your changes and commit them.
4. Push to your forked repository.
5. Submit a pull request.

Please ensure your code adheres to the project's coding standards and includes appropriate tests.

Please review our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing to Whisper-TikTok.

Planned features for future releases include:

- Enhanced video editing capabilities.
- Support for additional languages in voiceovers.
- Improved error handling and recovery.
- User-friendly GUI for easier usage.

### Upcoming Features

Join the discussion on the OpenAI Whisper forum to share your thoughts, ask questions, and connect with other users: [OpenAI Whisper Forum](https://community.openai.com/c/whisper).

### Acknowledgments

Whisper-TikTok acknowledges the following resources and contributors:

- [OpenAI Whisper](https://openai.com/research/whisper/) for the transcription model.
- [Microsoft Edge Cloud TTS API](https://docs.microsoft.com/en-us/microsoft-edge/web-api/tts-api/) for the text-to-speech service.
- [FFMPEG](https://ffmpeg.org/) for video processing.
- All contributors and users who provide feedback and support.
