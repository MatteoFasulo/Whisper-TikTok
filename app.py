import asyncio
import platform
import shutil
from pathlib import Path

import pandas as pd
import streamlit as st

from whisper_tiktok.config.logger_config import setup_logger
from whisper_tiktok.container import Container
from whisper_tiktok.main import Application
from whisper_tiktok.utils.color_utils import rgb_to_bgr
from whisper_tiktok.voice_manager import VoicesManager


def _setup_event_loop():
    """Setup event loop for Windows if needed."""
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())


def json_to_df(json_file):
    return pd.read_json(json_file)


def df_to_json(df):
    try:
        json_str = df.to_json(orient="records", indent=4, force_ascii=False)

        if df.shape[0] == 0:
            st.error("You must add at least one video to the JSON")
            return

        with open("video.json", "w", encoding="UTF-8") as f:
            f.write(json_str)

        st.success("JSON saved successfully!")

    except Exception as e:
        st.error(f"An error occurred while saving the JSON: {e}")


async def run_pipeline(
    model,
    background_url,
    tts_voice,
    random_voice,
    gender,
    language,
    font,
    font_size,
    font_color,
    sub_position,
    clean,
    verbose,
):
    """Run the video creation pipeline."""
    log_dir = Path.cwd() / "logs"
    log_level = "DEBUG" if verbose else "INFO"
    logger = setup_logger(log_dir, log_level)

    st_log = st.empty()
    st_log.info("Starting Whisper TikTok video creation pipeline...")

    try:
        # Validate model choice
        valid_models = ["tiny", "base", "small", "medium", "large", "turbo"]
        if model not in valid_models:
            st_log.error(f"Invalid model. Choose from: {', '.join(valid_models)}")
            return

        async def get_voice():
            nonlocal tts_voice, language
            # Handle random voice selection
            if random_voice:
                if not gender or not language:
                    st_log.error(
                        "Both --gender and --language required for random voice"
                    )
                    raise ValueError(
                        "Gender and language are required for random voice."
                    )

                voices_manager = VoicesManager()
                voices_obj = await voices_manager.create()
                voice_result = voices_manager.find(voices_obj, gender, language)
                tts_voice = voice_result.get("Name") or voice_result.get("ShortName")
                st_log.info(f"Selected random voice: {tts_voice}")
            else:
                # Validate specified voice
                voices_manager = VoicesManager()
                voices_obj = await voices_manager.create()
                extracted_language = "-".join(tts_voice.split("-")[0:2])
                voice_result = voices_obj.find(Locale=extracted_language)

                if not voice_result:
                    st_log.error(
                        "Voice not found. Run 'whisper-tiktok list-voices' to see available voices"
                    )
                    raise ValueError("Voice not found.")

                language = extracted_language
                st_log.info(f"Using voice: {tts_voice}")

        try:
            await asyncio.create_task(get_voice())
        except Exception as e:
            st_log.error(f"Voice validation failed: {e}")
            return

        # Process font color
        processed_font_color = font_color.lower()
        if processed_font_color.startswith("#"):
            processed_font_color = processed_font_color[1:]
        processed_font_color = rgb_to_bgr(processed_font_color)

        # Clean folders if requested
        if clean:
            st_log.info("Cleaning media and output folders...")
            media_path = Path.cwd() / "media"
            output_path = Path.cwd() / "output"

            if media_path.exists():
                shutil.rmtree(media_path)
                st_log.info(f"Removed {media_path}")

            if output_path.exists():
                shutil.rmtree(output_path)
                st_log.info(f"Removed {output_path}")

        # Setup DI container
        container = Container()
        config_dict = {
            "model": model,
            "background_url": background_url,
            "tts_voice": tts_voice,
            "Fontname": font,
            "Fontsize": font_size,
            "highlight_color": processed_font_color,
            "Alignment": sub_position,
            "BorderStyle": "1",
            "Outline": "1",
            "Shadow": "2",
            "Blur": "21",
            "MarginL": "0",
            "MarginR": "0",
        }
        container.config.from_dict(config_dict)

        # Run application
        app_instance = Application(container, logger)

        await app_instance.run()
        st_log.success("Pipeline completed successfully!")

    except Exception as e:
        logger.exception("Pipeline failed")
        st_log.error(f"Pipeline failed: {e}")


async def main():
    """Main function to run the Streamlit app."""
    # Streamlit Config
    st.set_page_config(
        page_title="Whisper-TikTok",
        page_icon="💬",
        layout="wide",
        initial_sidebar_state="expanded",
        menu_items={
            "Get Help": "https://github.com/MatteoFasulo/Whisper-TikTok",
            "Report a bug": "https://github.com/MatteoFasulo/Whisper-TikTok/issues",
            "About": """
                # Whisper-TikTok
                Whisper-TikTok is an innovative AI-powered tool that leverages the prowess of Edge TTS, OpenAI-Whisper, and FFMPEG to craft captivating TikTok videos also with a web application interface!

                Mantainer: https://github.com/MatteoFasulo

                If you find a bug or if you just have questions about the project feel free to reach me at https://github.com/MatteoFasulo/Whisper-TikTok
                Any contribution to this project is welcome to improve the quality of work!
                """,
        },
    )

    st.page_link(
        "https://github.com/MatteoFasulo/Whisper-TikTok", label="GitHub", icon="🔗"
    )

    st.title("🏆 Whisper-TikTok 🚀")
    st.write(
        "Create a TikTok video with text-to-speech of Microsoft Edge's TTS and subtitles of Whisper model."
    )

    st.subheader(
        "JSON Editor",
        help="Here you can edit the JSON file with the videos. Copy-and-paste is supported and compatible with Google Sheets, Excel, and others. You can do bulk-editing by dragging the handle on a cell (similar to Excel)!",
    )
    st.write(
        "ℹ️ The JSON file is saved automatically when you click the button below. Every time you edit the JSON file, you must click the button to save the changes otherwise they will be lost."
    )
    edited_df = st.data_editor(
        json_to_df("video.json"),
        num_rows="dynamic",
    )
    st.button(
        "Save JSON",
        on_click=df_to_json,
        args=(edited_df,),
        help="Save the JSON file with the videos",
    )

    st.divider()

    st.subheader("🚀 Run Pipeline")

    col1, col2 = st.columns(2)

    with col1:
        st.write("#### General Settings")
        model = st.selectbox(
            "Whisper model size",
            ["tiny", "base", "small", "medium", "large", "turbo"],
            index=5,
            help="Whisper model size [tiny|base|small|medium|large|turbo]",
        )
        background_url = st.text_input(
            "Background Video URL",
            "https://www.youtube.com/watch?v=dQw4w9WgXcQ",
            help="YouTube URL for background video",
        )
        clean = st.checkbox(
            "Clean Folders", help="Clean media and output folders before processing"
        )
        verbose = st.checkbox("Verbose Logging", help="Enable verbose logging")

    with col2:
        st.write("#### Voice Settings")
        random_voice = st.checkbox("Use Random Voice", help="Use random TTS voice")
        if random_voice:
            gender = st.selectbox(
                "Gender", ["Male", "Female"], help="Gender for random voice"
            )
            language = st.text_input(
                "Language", "en-US", help="Language for random voice (e.g., en-US)"
            )
            tts_voice = ""
        else:
            tts_voice = st.text_input(
                "TTS Voice",
                "en-US-ChristopherNeural",
                help="TTS voice to use. See available voices with `whisper-tiktok list-voices`",
            )
            gender = None
            language = None

    st.write("#### Subtitle Settings")
    col3, col4, col5 = st.columns(3)
    with col3:
        font = st.text_input("Font", "Lexend Bold", help="Subtitle font")
        font_size = st.number_input("Font Size", value=21, help="Subtitle font size")
    with col4:
        font_color = st.color_picker(
            "Font Color", "#FFF000", help="Subtitle color (hex format)"
        )
    with col5:
        sub_position = st.slider(
            "Subtitle Position",
            min_value=1,
            max_value=9,
            value=5,
            help="Subtitle position (1-9), refer to FFMPEG documentation and ASS subtitle format for positioning",
        )

    if st.button("Run Video Creation Pipeline", type="primary"):
        _setup_event_loop()
        asyncio.run(
            run_pipeline(
                model,
                background_url,
                tts_voice,
                random_voice,
                gender,
                language,
                font,
                font_size,
                font_color,
                sub_position,
                clean,
                verbose,
            )
        )


if __name__ == "__main__":
    asyncio.run(main())
