# Introducing ChatGPT-TikTok 🤖🎥

Discover ChatGPT-TikTok, an innovative AI-powered tool that leverages the prowess of **Edge TTS**, **OpenAI-Whisper**, and **FFMPEG** to craft captivating TikTok videos. Harnessing the capabilities of OpenAI's Whisper model, ChatGPT-TikTok effortlessly generates an accurate **transcription** from provided audio files, laying the foundation for the creation of mesmerizing TikTok videos through the utilization of **FFMPEG**. Additionally, the program seamlessly integrates the **Microsoft Edge Cloud Text-to-Speech (TTS) API** to lend a vibrant **voiceover** to the video. Opting for Microsoft Edge Cloud TTS API's voiceover is a deliberate choice, as it delivers a remarkably **natural and authentic** auditory experience, setting it apart from the often monotonous and artificial voiceovers prevalent in numerous TikTok videos.

## Demo Video 🎬

<https://github.com/MatteoFasulo/ChatGPT-TikTok/blob/main/demo.mp4>

## Operating Principle

Employing ChatGPT-TikTok is a breeze: simply complete the JSON-formatted dictionary located at the outset of the `main.py` file.

Summarizing the program's functionality:

> Furnished with a structured JSON dataset containing details such as the **series name**, **video part number**, **video text**, **outro text**, and **path**, the program orchestrates the synthesis of a video incorporating the provided text and outro. Subsequently, the generated video is stored within the designated `output` folder.

### In-Depth Insights

The program conducts the **sequence of actions** outlined below:

1. Retrieve **environment variables** from the optional .env file.
2. Validate the presence of **PyTorch** with **CUDA** installation.
3. Download a random video from platforms like YouTube, e.g., a Minecraft parkour gameplay clip.
4. Load the OpenAI Whisper model into memory.
5. Extract the video text from the provided JSON file and initiate a **Text-to-Speech** request to the Microsoft Edge Cloud TTS API, preserving the response as an .mp3 audio file.
6. Utilize the OpenAI Whisper model to generate a detailed **transcription** of the .mp3 file, available in both .srt and .ass formats.
7. Select a **random background** video from the dedicated folder.
8. Integrate the srt and ass files into the chosen video using FFMPEG, creating a final .mp4 output.
9. Voila! In a matter of minutes, you've crafted a captivating TikTok video while sipping your favorite coffee ☕️.

> Upon reviewing the code, you'll observe the implementation of `stable_whisper`, a variant of the OpenAI Whisper model with specific enhancements. This adaptation accommodates the creation of a karaoke-like effect, wherein spoken words are highlighted at precise timestamps. Recognizing the limitations of the original OpenAI Whisper model in achieving the desired granularity, we transitioned to Stable Whisper. This evolved model empowers users with both word-level and segment-level timestamps, enriching the experience.

## Prerequisites 🛠️

ChatGPT-TikTok has undergone rigorous testing on Windows 10 systems equipped with Python versions 3.8 and 3.9. To streamline the installation of necessary dependencies, execute the following command within your terminal:

```python
pip install -r requirements.txt
```

Keep in mind that, due to the utilization of the OpenAI Whisper model for speech recognition, a GPU is indispensable for program execution. PyTorch will evaluate the availability of the CUDA driver and harness the GPU's capabilities whenever feasible.

## Usage Guidelines 📝

To embark on your ChatGPT-TikTok journey, initiate the following command within your terminal:

```python
python main.py
```

## Code of Conduct

Please review our [Code of Conduct](./CODE_OF_CONDUCT.md) before contributing to ChatGPT-TikTok.

## Contributing

We welcome contributions from the community! Please see our [Contributing Guidelines](./CONTRIBUTING.md) for more information.

## Upcoming Features 🔮

- Integration with the OpenAI API to generate more advanced responses.
- Integration with the TikTok Developer API to upload videos directly to the platform.
- Improved user interface for a more seamless experience.

## OpenAI Whisper Forum Discussion

- <https://github.com/openai/whisper/discussions/223>

## Acknowledgments

- We'd like to give a huge thanks to [@rany2](https://www.github.com/rany2) for their [edge-tts](https://github.com/rany2/edge-tts) package, which made it possible to use the Microsoft Edge Cloud TTS API with ChatGPT-TikTok.
- We also acknowledge the contributions of the Whisper model by [@OpenAI](https://github.com/openai/whisper) for robust speech recognition via large-scale weak supervision and [jianfch/ stable-ts](https://github.com/jianfch/stable-ts) for a script that modifies OpenAI's Whisper to produce more reliable timestamps.
