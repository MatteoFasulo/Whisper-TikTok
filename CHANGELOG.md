# Changelog

## Unreleased (2026-01-25)

## v2.0.4 (2026-01-25)

### Fixes

- Fix: Update CI workflows to correct branch specifications and enhance pre-commit hooks.
    
- Fix: Update Python version in CI workflows to 3.12 and adjust MkDocs installation step.
    
- Fix: Update CI workflow to use uv for MkDocs deployment and clean up imports in __init__.py.
    
- Fix: Add version file with version 2.0.3.
    
  - update pre-commit hook with black, isort and flake
  - added changelog config for future changelogs
  - update pyproject toml with build backend, dynamic version, extra requirements, pytest args
- Fix emoji generator path in mkdocs.yml and add hex color validation in color_utils.py.
    
- Fix formatting in video.json by removing unnecessary whitespace and ensuring proper JSON structure.
    
  - added Streamlit dashboard
- Fix formatting inconsistencies in CI workflow files and update mkdocs deploy also on dev branch.
    
- Fix typos in documentation and improve command execution return handling.
    
- Fix text formatting and background selection in video creation.
    
- Fix TikTok upload error handling.
    
- Fixed chdir.
    
### New

- Add Docker support: create Dockerfile and docker-compose.yml, and configure .dockerignore.
    
- Add docker compose file.
    
- Add Docker documentation for Whisper-TikTok model.
    
- Add sidebar navigation and maximum words per line option.
    
- Add requests and openai to requirements.txt.
    
- Added reddit2json directly to whisper tiktok so video creation can be made muuch faster.
    
- Add error handling and information message in JSON saving function.
    
- Add JSON file handling functions in streamlit UI.
    
- Added Dockerfilr for Web-UI with dependeces.
    
- Add Reddit section to generate videos from subreddits.
    
- New WebUi image + Readme update.
    
- Add streamlit dashboard.
    
- Add pathlib module and update file handling in app.py.
    
- Add Gradio WebUI (experimental).
    
- Add subtitle position, font, and size options.
    
- Add stable-ts to requirements.txt and update video.json structure.
    
  Split main.py into multiple files
- Add TikTok video upload functionality.
    
- New folder structure, absolute path and minor fixes.
    
- Add Docs.
    
- New readme style.
    
- Add files via upload.
    
### Other

- Bump version: 2.0.3 → 2.0.4.
    
- Chore: remove Docker support and related documentation.
    
- Chore: remove changelog CI workflow and update versioning instructions in documentation.
    
- Enhance documentation and functionality across multiple files.
    
  - Updated mkdocs.yml to include mkdocstrings plugin for better documentation generation.
  - Revised section headers in 1-ffmpeg.md, 2-cuda.md, and 3-docker.md for clarity.
  - Added new API documentation in whisper_tiktok.md.
  - Improved type hints and docstrings in command_executor.py and main.py for better code understanding.
  - Enhanced color_utils.py with detailed docstrings for the rgb_to_bgr function.
  - Included voice_manager import in __init__.py for better module accessibility.
- Chore: Fix README typo.
    
- Chore: Update repository URL in GitHub Actions workflow.
    
- Feat: Add GitHub Actions workflow for syncing to Hugging Face hub.
    
- Chore: Update assignees in feature_request.md and other.md issue templates.
    
- README.md Update.
    
  New webui
- Webui update: Your Backgrounds.
    
  List of all your downloaded backgrounds in the webui.
- Part string missing in video.json.
    
- Bestvideo and bestaudio with yt-dlp using mp4 instead of vp9.
    
- Main args for language, tts, random voice.
    
- Json decode error, path removed from json, new media folder with .srt and .mp3 files.
    
- Absolute path.
    
- Ffprobe fix for "duration", width, height and bitrate.
    
- Pull request template.
    
- Create SECURITY.md.
    
- $Adding CI documentation files.
    
- Create FUNDING.yml.
    
- CLI Options; Console Log and Logging; Message file.
    
- Closes #2; Fixed missing background folder.
    
- Code refactoring, video.json and modified docs.
    
- Mp4 file gitignore.
    
- Readme update code refactor and fixed requirements.
    
- Utils.py, logging, console.log with status spinner.
    
- Rich and fixes.
    
- Stabilizing Timestamps for Whisper and json path change.
    
- OpenAI Whisper and Stable-TS.
    
- Single_word_cc - blur_cc - fixed_audio_duration.
    
- Series '_' spaces.
    
- Yt-dlp library.
    
- Requirements update with pytorch cuda 11.7.
    
- Code of conduct, contributing, ffmpeg command, chdir class.
    
- Subtitles style.
    
- Ffmpeg command.
    
- Ffmpeg for auto-editing.
    
- Format document and docstring.
    
- Tiktok api (commented) and removed + whisper model for SRT file.
    
- Docstring & json feature.
    
- Ignore .mp3 and async io support for edge-tts.
    
- No more default requirements.txt in favor of pipenv package.
    
- Pipevn package.
    
- License update.
    
- Moved.
    
- Initial commit.
    
### Updates

- Refactor contributing guidelines, remove Docker support, and update documentation.
    
  - Updated CONTRIBUTING.md to streamline contribution process and added new section for releasing a new version.
  - Removed Dockerfile and docker-compose.yml as part of the project restructuring.
  - Enhanced README.md and index.md for clarity and improved installation instructions.
  - Updated FFMPEG installation documentation across multiple files.
  - Added example Jupyter notebook for demonstrating usage.
  - Adjusted pyproject.toml for script naming and testing configurations.
  - Introduced new test_import.py to verify module import functionality.
  - Updated versioning in version.py to include a 'v' prefix.
- Refactor: Simplify CI workflows by removing redundant style checks and improving structure.
    
- Remove version information and version callback from main.py.
    
- Update release workflow: adjust push condition for pull requests and add branch support for dev.
    
- Refactor Dockerfile: simplify package installation and remove nonroot user setup.
    
- Update .dockerignore: remove *.toml file exclusion.
    
- Refactor Dockerfile: streamline package installation and environment variable setup.
    
- Refactor Dockerfile: remove unnecessary git clone command and adjust COPY instruction.
    
- Update CI workflow: refine mkdocs deployment process and enhance caching strategy.
    
- Update CI workflow and documentation links: streamline mkdocs deployment and enhance link accessibility.
    
- Update pull request template: enhance clarity by refining sections and improving structure.
    
- Update issue templates: streamline assignees, fix title formatting, and enhance documentation clarity.
    
- Refactor code structure and improve logging.
    
  - Removed `pycodestyle` from dependencies and added it to optional dependencies.
  - Updated logger configuration for better readability.
  - Refactored container service initialization for improved clarity.
  - Enhanced command executor with clearer execution result handling.
  - Improved video factory strategy building with better formatting.
  - Removed unnecessary `pass` statements in exception classes and interfaces.
  - Updated main application command to simplify version handling.
  - Enhanced logging messages for better context and clarity.
  - Refactored video processor path initialization for better readability.
  - Improved FFmpeg service error handling and media info extraction.
  - Added docstrings to processing strategies for better documentation.
  - Enhanced voice manager with clearer class documentation.
- Refactor dependency management: change optional-dependencies to dev-dependencies and restructure requires-dist for development packages.
    
- Update: Simplify project installation command and restructure optional dependencies in pyproject.toml.
    
- Update: Bump platformdirs to 4.5.1 and urllib3 to 2.6.0; add pycodestyle as a development dependency.
    
- Update: Add 'pycodestyle' to development dependencies in pyproject.toml.
    
- Update: Implement video processing pipeline with strategies for downloading, TTS, transcription, and video composition based on dependency injection and registry based design patterns.
    
  - Added VideoProcessor class to orchestrate video processing.
  - Introduced ProcessingContext and ProcessingResult data classes.
  - Created various processing strategies: DownloadBackgroundStrategy, TTSGenerationStrategy, TranscriptionStrategy, VideoCompositionStrategy, and TikTokUploadStrategy.
  - Implemented VideoRepository for audio file saving and background video retrieval.
  - Developed FFmpegService for video composition and media info extraction.
  - Added TranscriptionService for audio transcription using Whisper model.
  - Integrated TTSService for text-to-speech functionality.
  - Created VideoDownloaderService for downloading videos from YouTube.
  - Removed obsolete modules: subtitle_creator, text_to_speech, tiktok, video_creator, video_downloader, video_prepare, and utils.
  - Refactored voice management with VoicesManager for edge-tts.
  - Updated color utility functions to a dedicated module.
  - Removed streamlit (will be reintroduced later)
  - Removed tests (will be reintroduced later)
- Update CI style check with custom test requirements in plain python.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CI style check with uv requirements.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with pycodestyle, pylint, mypy, riff and black formatting checks and improved code structure.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update code with black formatting specs in CI.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CodeQL CI and Style Checks.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor README.md and index.md to streamline content and remove outdated sections.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor run_test.yml workflow triggers, update font in subtitle_creator.py, enhance error message in utils.py, add app.py for video generation, and remove unused reddit.py and __init__.py files.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update minimum python version to 3.9, added tests for 3.9 and 3.12 and relaxed version requirements.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with less strict torch and numpy version requirement and ffmpeg setup action.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update run_test.yml to remove Python 3.12 from the matrix and ensure consistent package installation.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor README.md to streamline structure and remove outdated sections.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update minimum python version to 3.10.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with new test setup using astra uv.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update code with new structure:.
    
  - main code inside Whisper_TikTok folder
  - removed msg and unused code
  - added test cases for testing single functions of the VideoCreator class
  - added CI/CD with pytest
  - improved docs with new CLI syntax
  - added black8 formatting on commit

  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CONTRIBUTING.md with new repo name.
    
- Update FUNDING.yml.
    
- Delete .github/workflows/hf.yml.
    
- Update Web App link to HuggingFace in README and docs.
    
- Removed demo video.
    
- Update demo file with smaller size.
    
- Update requirements.txt.
    
  Removed index for CUDA since latest CUDA version is already included in plain PyTorch (https://pytorch.org/get-started/locally/) with CUDA 12.1
- Update README.md.
    
- Update supported version in SECURITY.md.
    
- Update issue templates.
    
- Update README and docs.
    
- Update README.md and arg_parser.py.
    
- Update maximum number of words per line for subtitles.
    
- Refactor translation and optimization process for Reddit posts.
    
- Changed placing of reddit2json readme placement so it fits better.
    
- Update app.py.
    
- Update README.md.
    
- Update README.md.
    
- Update README.md.
    
- Refactor generate_video function to handle multiple results.
    
- Refactor video generation process with asyncio.
    
- Refactor generate_video function and add video selection.
    
- Refactor video creation process.
    
- Remove mention of improved user interface.
    
- Refactor video downloading code.
    
- Update subtitle position and font size.
    
  This commit updates the `--sub_position` and `--font_size` options in the code to use integer values instead of text values. This ensures consistency and improves readability.
- Update font color and subtitle format options.
    
- Update subtitle format default value.
    
- Update default font color in main.py.
    
- Update main.py.
    
  Fix default value for argument 'sub_format'
- Update README.md.
    
- Update subtitle format and word highlighting.
    
- Update README.md.
    
  Removed path in video.json,.ass file description and explained that fp16 is only supported by GPUs
- Update README.md.
    
- Update requirements.txt.
    
- Removed 'stable_whisper' dependency from project.
    
- Update issue templates.
    
- Update README.md.
    
- Changed repo name.
    
- Removed break, all good.
    
- Removed chdir.
    
- Updated path with KeepDir class.
    
- Update.
    
- Removed build status.
    
- Update README.md.
    
- Update README.md.
    
- Update README.md.
    
## v2.0.3 (2025-12-12)

### Fixes

- Fix emoji generator path in mkdocs.yml and add hex color validation in color_utils.py.
    
- Fix formatting in video.json by removing unnecessary whitespace and ensuring proper JSON structure.
    
  - added Streamlit dashboard
- Fix formatting inconsistencies in CI workflow files and update mkdocs deploy also on dev branch.
    
- Fix typos in documentation and improve command execution return handling.
    
### New

- Add Docker support: create Dockerfile and docker-compose.yml, and configure .dockerignore.
    
- Add docker compose file.
    
- Add Docker documentation for Whisper-TikTok model.
    
### Other

- Chore: Fix README typo.
    
- Chore: Update repository URL in GitHub Actions workflow.
    
- Feat: Add GitHub Actions workflow for syncing to Hugging Face hub.
    
- Chore: Update assignees in feature_request.md and other.md issue templates.
    
### Updates

- Remove version information and version callback from main.py.
    
- Update release workflow: adjust push condition for pull requests and add branch support for dev.
    
- Refactor Dockerfile: simplify package installation and remove nonroot user setup.
    
- Update .dockerignore: remove *.toml file exclusion.
    
- Refactor Dockerfile: streamline package installation and environment variable setup.
    
- Refactor Dockerfile: remove unnecessary git clone command and adjust COPY instruction.
    
- Update CI workflow: refine mkdocs deployment process and enhance caching strategy.
    
- Update CI workflow and documentation links: streamline mkdocs deployment and enhance link accessibility.
    
- Update pull request template: enhance clarity by refining sections and improving structure.
    
- Update issue templates: streamline assignees, fix title formatting, and enhance documentation clarity.
    
- Refactor code structure and improve logging.
    
  - Removed `pycodestyle` from dependencies and added it to optional dependencies.
  - Updated logger configuration for better readability.
  - Refactored container service initialization for improved clarity.
  - Enhanced command executor with clearer execution result handling.
  - Improved video factory strategy building with better formatting.
  - Removed unnecessary `pass` statements in exception classes and interfaces.
  - Updated main application command to simplify version handling.
  - Enhanced logging messages for better context and clarity.
  - Refactored video processor path initialization for better readability.
  - Improved FFmpeg service error handling and media info extraction.
  - Added docstrings to processing strategies for better documentation.
  - Enhanced voice manager with clearer class documentation.
- Refactor dependency management: change optional-dependencies to dev-dependencies and restructure requires-dist for development packages.
    
- Update: Simplify project installation command and restructure optional dependencies in pyproject.toml.
    
- Update: Bump platformdirs to 4.5.1 and urllib3 to 2.6.0; add pycodestyle as a development dependency.
    
- Update: Add 'pycodestyle' to development dependencies in pyproject.toml.
    
- Update: Implement video processing pipeline with strategies for downloading, TTS, transcription, and video composition based on dependency injection and registry based design patterns.
    
  - Added VideoProcessor class to orchestrate video processing.
  - Introduced ProcessingContext and ProcessingResult data classes.
  - Created various processing strategies: DownloadBackgroundStrategy, TTSGenerationStrategy, TranscriptionStrategy, VideoCompositionStrategy, and TikTokUploadStrategy.
  - Implemented VideoRepository for audio file saving and background video retrieval.
  - Developed FFmpegService for video composition and media info extraction.
  - Added TranscriptionService for audio transcription using Whisper model.
  - Integrated TTSService for text-to-speech functionality.
  - Created VideoDownloaderService for downloading videos from YouTube.
  - Removed obsolete modules: subtitle_creator, text_to_speech, tiktok, video_creator, video_downloader, video_prepare, and utils.
  - Refactored voice management with VoicesManager for edge-tts.
  - Updated color utility functions to a dedicated module.
  - Removed streamlit (will be reintroduced later)
  - Removed tests (will be reintroduced later)
- Update CI style check with custom test requirements in plain python.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CI style check with uv requirements.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with pycodestyle, pylint, mypy, riff and black formatting checks and improved code structure.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update code with black formatting specs in CI.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CodeQL CI and Style Checks.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor README.md and index.md to streamline content and remove outdated sections.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor run_test.yml workflow triggers, update font in subtitle_creator.py, enhance error message in utils.py, add app.py for video generation, and remove unused reddit.py and __init__.py files.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update minimum python version to 3.9, added tests for 3.9 and 3.12 and relaxed version requirements.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with less strict torch and numpy version requirement and ffmpeg setup action.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update run_test.yml to remove Python 3.12 from the matrix and ensure consistent package installation.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Refactor README.md to streamline structure and remove outdated sections.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update minimum python version to 3.10.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update with new test setup using astra uv.
    
  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update code with new structure:.
    
  - main code inside Whisper_TikTok folder
  - removed msg and unused code
  - added test cases for testing single functions of the VideoCreator class
  - added CI/CD with pytest
  - improved docs with new CLI syntax
  - added black8 formatting on commit

  **signed-off-by:** Matteo Fasulo <mat.fasulo@gmail.com>

- Update CONTRIBUTING.md with new repo name.
    
- Update FUNDING.yml.
    
- Delete .github/workflows/hf.yml.
    
- Update Web App link to HuggingFace in README and docs.
    
- Removed demo video.
    
- Update demo file with smaller size.
    
- Update requirements.txt.
    
  Removed index for CUDA since latest CUDA version is already included in plain PyTorch (https://pytorch.org/get-started/locally/) with CUDA 12.1
## v2.0.2 (2024-03-05)

### Fixes

- Fix text formatting and background selection in video creation.
    
### New

- Add sidebar navigation and maximum words per line option.
    
- Add requests and openai to requirements.txt.
    
- Added reddit2json directly to whisper tiktok so video creation can be made muuch faster.
    
- Add error handling and information message in JSON saving function.
    
- Add JSON file handling functions in streamlit UI.
    
### Updates

- Update README.md.
    
- Update supported version in SECURITY.md.
    
- Update issue templates.
    
- Update README and docs.
    
- Update README.md and arg_parser.py.
    
- Update maximum number of words per line for subtitles.
    
- Refactor translation and optimization process for Reddit posts.
    
- Changed placing of reddit2json readme placement so it fits better.
    
## v2.0.1 (2024-01-28)

### New

- Added Dockerfilr for Web-UI with dependeces.
    
- Add Reddit section to generate videos from subreddits.
    
- New WebUi image + Readme update.
    
- Add streamlit dashboard.
    
### Updates

- Update app.py.
    
- Update README.md.
    
- Update README.md.
    
- Update README.md.
    
- Refactor generate_video function to handle multiple results.
    
- Refactor video generation process with asyncio.
    
- Refactor generate_video function and add video selection.
    
- Refactor video creation process.
    
## v2.0.0 (2023-12-31)

### Fixes

- Fix TikTok upload error handling.
    
### New

- Add pathlib module and update file handling in app.py.
    
- Add Gradio WebUI (experimental).
    
- Add subtitle position, font, and size options.
    
- Add stable-ts to requirements.txt and update video.json structure.
    
  Split main.py into multiple files
- Add TikTok video upload functionality.
    
### Other

- README.md Update.
    
  New webui
- Webui update: Your Backgrounds.
    
  List of all your downloaded backgrounds in the webui.
### Updates

- Remove mention of improved user interface.
    
- Refactor video downloading code.
    
- Update subtitle position and font size.
    
  This commit updates the `--sub_position` and `--font_size` options in the code to use integer values instead of text values. This ensures consistency and improves readability.
- Update font color and subtitle format options.
    
- Update subtitle format default value.
    
- Update default font color in main.py.
    
- Update main.py.
    
  Fix default value for argument 'sub_format'
## v1.0.4 (2023-11-25)

### Updates

- Update README.md.
    
- Update subtitle format and word highlighting.
    
- Update README.md.
    
  Removed path in video.json,.ass file description and explained that fp16 is only supported by GPUs
## v1.0.3 (2023-11-08)

### New

- New folder structure, absolute path and minor fixes.
    
### Other

- Part string missing in video.json.
    
- Bestvideo and bestaudio with yt-dlp using mp4 instead of vp9.
    
- Main args for language, tts, random voice.
    
- Json decode error, path removed from json, new media folder with .srt and .mp3 files.
    
- Absolute path.
    
- Ffprobe fix for "duration", width, height and bitrate.
    
### Updates

- Update README.md.
    
- Update requirements.txt.
    
## v1.0.2 (2023-10-11)

### Updates

- Removed 'stable_whisper' dependency from project.
    
## v1.0.1 (2023-09-10)

### New

- Add Docs.
    
### Other

- Pull request template.
    
- Create SECURITY.md.
    
- $Adding CI documentation files.
    
- Create FUNDING.yml.
    
### Updates

- Update issue templates.
    
## v1.0.0 (2023-08-26)

### Other

- CLI Options; Console Log and Logging; Message file.
    
- Closes #2; Fixed missing background folder.
    
## v0.4 (2023-08-23)

### Other

- Code refactoring, video.json and modified docs.
    
## v0.3 (2023-08-17)

### Other

- Mp4 file gitignore.
    
- Readme update code refactor and fixed requirements.
    
### Updates

- Update README.md.
    
- Changed repo name.
    
## v0.2 (2023-05-02)

### Fixes

- Fixed chdir.
    
### New

- New readme style.
    
- Add files via upload.
    
### Other

- Utils.py, logging, console.log with status spinner.
    
- Rich and fixes.
    
- Stabilizing Timestamps for Whisper and json path change.
    
- OpenAI Whisper and Stable-TS.
    
- Single_word_cc - blur_cc - fixed_audio_duration.
    
- Series '_' spaces.
    
- Yt-dlp library.
    
- Requirements update with pytorch cuda 11.7.
    
- Code of conduct, contributing, ffmpeg command, chdir class.
    
- Subtitles style.
    
- Ffmpeg command.
    
- Ffmpeg for auto-editing.
    
- Format document and docstring.
    
- Tiktok api (commented) and removed + whisper model for SRT file.
    
- Docstring & json feature.
    
- Ignore .mp3 and async io support for edge-tts.
    
- No more default requirements.txt in favor of pipenv package.
    
- Pipevn package.
    
- License update.
    
- Moved.
    
- Initial commit.
    
### Updates

- Removed break, all good.
    
- Removed chdir.
    
- Updated path with KeepDir class.
    
- Update.
    
- Removed build status.
    
- Update README.md.
    
- Update README.md.
    
- Update README.md.
    

