# Introducing Whisper-TikTok 🤖🎥

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MatteoFasulo/Whisper-TikTok&type=Date)](https://star-history.com/#MatteoFasulo/Whisper-TikTok&Date)

## Table of Contents

- [Introduction](#introduction)
- [Video (demo)](#demo-video)
- [How it works?](#how-it-works)
- [Web App (Online)](#web-app-online)
- [Streamlit Web App](#streamlit-web-app)
- [Local Installation](#local-installation)
- [Dependencies](#dependencies)
- [Web-UI (Local)](#web-ui-local)
- [Command-Line](#command-line)
- [Usage Examples](#usage-examples)
- [Additional Resources](#additional-resources)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [Upcoming Features](#upcoming-features)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Introduction
Discover Whisper-TikTok, an innovative AI-powered tool that leverages the prowess of **Edge TTS**, **OpenAI-Whisper**, and **FFMPEG** to craft captivating TikTok videos. Harnessing the capabilities of OpenAI's Whisper model, Whisper-TikTok effortlessly generates an accurate **transcription** from provided audio files, laying the foundation for the creation of mesmerizing TikTok videos through the utilization of **FFMPEG**. Additionally, the program seamlessly integrates the **Microsoft Edge Cloud Text-to-Speech (TTS) API** to lend a vibrant **voiceover** to the video. Opting for Microsoft Edge Cloud TTS API's voiceover is a deliberate choice, as it delivers a remarkably **natural and authentic** auditory experience, setting it apart from the often monotonous and artificial voiceovers prevalent in numerous TikTok videos.

## Demo Video

<https://github.com/MatteoFasulo/Whisper-TikTok/assets/74818541/68e25504-c305-4144-bd39-c9acc218c3a4>

## Installation 🛠️

Whisper-TikTok has been tested in Windows 10, Windows 11 and Ubuntu 23.04 systems equipped with **Python versions 3.9, 3.10, and 3.11**.

If you want to run Whisper-TikTok locally, you can clone the repository using the following command:

```bash
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git
```

Install the required dependencies using pip:

```python
pip install -r requirements.txt
```

However, we encourage the adoption of astra `uv` to install the required dependencies. If you are using `uv`, you can install the dependencies with the following command:

```bash
uv sync
```

Then, install the repository as a package:

```bash
pip install -e .
```

or

```bash
uv pip install -e .
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

Please note that for optimal performance, it's advisable to have a GPU when using the OpenAI Whisper model for speech recognition. However, the program will work without a GPU, but it will run more slowly due to CPU limitations.

## Command-Line

To run the program from the command-line, execute the following command within your terminal:

```bash
python -m Whisper_TikTok.main
```

### CLI Options

Whisper-TikTok supports the following command-line options:

```text
python -m Whisper_TikTok.main [OPTIONS]

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

> If you use the --random_voice option, please specify both --gender and --language arguments. Also you will need to specify the --non_english argument if you want to use a non-English voice otherwise the program will use the English model. Whisper model will auto-detect the language of the audio file and use the corresponding model.

## Usage Examples

- Generate a TikTok video using a specific TTS model and voice:

```bash
python -m Whisper_TikTok.main --model medium --tts en-US-EricNeural
```

- Generate a TikTok video without using the English model:

```bash
python -m Whisper_TikTok.main --non_english --tts de-DE-KillianNeural
```

- Use a custom YouTube video as the background video:

```bash
python -m Whisper_TikTok.main --url https://www.youtube.com/watch?v=dQw4w9WgXcQ --tts en-US-JennyNeural
```

- Modify the font color of the subtitles:

```bash
python -m Whisper_TikTok.main --sub_format b --font_color #FFF000 --tts en-US-JennyNeural
```

- Generate a TikTok video with a random TTS voice:

```bash
python -m Whisper_TikTok.main --random_voice --gender Male --language en-US
```

- List all available voices:

```bash
edge-tts --list-voices
```

## Additional Resources

### Code of Conduct

Please review our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing to Whisper-TikTok.

### Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for more information.

## Acknowledgments

- We'd like to give a huge thanks to [@rany2](https://www.github.com/rany2) for their [edge-tts](https://github.com/rany2/edge-tts) package, which made it possible to use the Microsoft Edge Cloud TTS API with Whisper-TikTok.
- We also acknowledge the contributions of the Whisper model by [@OpenAI](https://github.com/openai/whisper) for robust speech recognition via large-scale weak supervision
- Also [@jianfch](https://github.com/jianfch/stable-ts) for the stable-ts package, which made it possible to use the OpenAI Whisper model with Whisper-TikTok in a stable manner with font color and subtitle format options.

### License

Whisper-TikTok is licensed under the [Apache License, Version 2.0](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/LICENSE).
