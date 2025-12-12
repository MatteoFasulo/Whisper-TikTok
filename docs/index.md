# Introducing Whisper-TikTok 🤖🎥

## Star History

[![Star History Chart](https://api.star-history.com/svg?repos=MatteoFasulo/Whisper-TikTok&type=Date)](https://star-history.com/#MatteoFasulo/Whisper-TikTok&Date)

## Table of Contents

- [Introduction](#introduction)
- [Video (demo)](#demo-video)
- [Command-Line](#command-line)
- [Usage Examples](#usage-examples)
- [Additional Resources](#additional-resources)
- [Code of Conduct](#code-of-conduct)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Introduction

Discover Whisper-TikTok, an innovative AI-powered tool that leverages the prowess of **Edge TTS**, **OpenAI-Whisper**, and **FFMPEG** to craft captivating TikTok videos. Harnessing the capabilities of OpenAI's Whisper model, Whisper-TikTok effortlessly generates an accurate **transcription** from provided audio files, laying the foundation for the creation of mesmerizing TikTok videos through the utilization of **FFMPEG**. Additionally, the program seamlessly integrates the **Microsoft Edge Cloud Text-to-Speech (TTS) API** to lend a vibrant **voiceover** to the video. Opting for Microsoft Edge Cloud TTS API's voiceover is a deliberate choice, as it delivers a remarkably **natural and authentic** auditory experience, setting it apart from the often monotonous and artificial voiceovers prevalent in numerous TikTok videos.

## Demo Video

<https://github.com/MatteoFasulo/Whisper-TikTok/assets/74818541/68e25504-c305-4144-bd39-c9acc218c3a4>

## Installation 🛠️

Whisper-TikTok has been tested in Windows 10, Windows 11 and Ubuntu 24.04 systems equipped with **Python versions 3.11, and 3.12**.

If you want to run Whisper-TikTok locally, you can clone the repository using the following command:

```bash
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git
```

Install the required dependencies using pip:

```python
pip install -r requirements.txt
```

However, we encourage the adoption of astral [`uv`](https://docs.astral.sh/uv/) to install the required dependencies. If you are using `uv`, you can install the dependencies with the following command:

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

Binaries for [**FFMPEG**](https://ffmpeg.org/) are not included in the repository and must be installed separately. Make sure to have FFMPEG installed and accessible in your system's PATH. For convenience, here are the installation instructions for various package managers:

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

Please note that for optimal performance, it's advisable to have a GPU when using the OpenAI Whisper model for Automatic Speech Recognition (ASR). However, the program will work without a GPU, but it will run more slowly due to CPU limitations.

## Command-Line

To run the program from the command-line, execute the following command within your terminal:

```bash
python -m whisper_tiktok.main --help
```

which will provide you with a list of available commands.

### CLI Options

Whisper-TikTok supports many command-line options to customize the generated TikTok video. Just to name a few, you can choose the Whisper model to use, the TTS voice, subtitle format, subtitle position, font size, font color, and many more.

To browse all available options, run the following command:

```bash
python -m whisper_tiktok.main create --help
```

> If you use the --random_voice option, please specify both --gender and --language arguments. Whisper model will auto-detect the language of the audio file and use the corresponding model.

## Usage Examples

- Generate a TikTok video using a specific TTS voice:

```bash
python -m whisper_tiktok.main create --tts en-US-EricNeural
```

- Use a custom YouTube video as the background video:

```bash
python -m whisper_tiktok.main create --background-url https://www.youtube.com/watch?v=dQw4w9WgXcQ
```

- Modify the font color of the subtitles:

```bash
python -m whisper_tiktok.main create --font_color FFF000
```

- Generate a TikTok video with a random TTS voice:

```bash
python -m whisper_tiktok.main create --random_voice --gender Male --language en-US
```

- List all available voices:

```bash
python -m whisper_tiktok.main list-voices
```

you will find a list of available voices together with some information about each voice, such as the tone, style, and suitable scenarios.

## Additional Resources

### Code of Conduct

Please review our [Code of Conduct](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/CODE_OF_CONDUCT.md) before contributing to Whisper-TikTok.

### Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/CONTRIBUTING.md) for more information.

## Acknowledgments

- We'd like to give a huge thanks to [@rany2](https://www.github.com/rany2) for their [edge-tts](https://github.com/rany2/edge-tts) package, which made it possible to use the Microsoft Edge Cloud TTS API with Whisper-TikTok.
- We also acknowledge the contributions of the Whisper model by [@OpenAI](https://github.com/openai/whisper) for robust speech recognition via large-scale weak supervision
- Also [@jianfch](https://github.com/jianfch/stable-ts) for the stable-ts package, which made it possible to use the OpenAI Whisper model with Whisper-TikTok in a stable manner with font color and subtitle format options.

### License

Whisper-TikTok is licensed under the [Apache License, Version 2.0](https://github.com/MatteoFasulo/Whisper-TikTok/blob/main/LICENSE).
