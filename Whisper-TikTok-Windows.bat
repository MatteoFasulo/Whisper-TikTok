@echo off
setlocal enabledelayedexpansion

REM Check if conda is installed
conda --version > nul 2>&1
if %errorlevel% neq 0 (
    REM If not installed, install the latest version of conda
    echo Installing Conda...
    curl -O https://repo.anaconda.com/miniconda/Miniconda3-latest-Windows-x86_64.exe
    start /wait Miniconda3-latest-Windows-x86_64.exe /InstallationType=JustMe /RegisterPython=0 /S /D=%UserProfile%\Miniconda3
    del Miniconda3-latest-Windows-x86_64.exe
)

REM Create a conda environment with Python 3.11
conda create -n WhisperTikTok python=3.11 -y

REM Activate the conda environment
conda activate WhisperTikTok

REM Clone the repository
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git

REM Enter the repository
cd Whisper-TikTok

REM Install dependencies
pip install -U -r requirements.txt

REM Check if ffmpeg is installed
ffmpeg -version > nul 2>&1
if %errorlevel% neq 0 (
    REM Check if scoop is installed
    scoop help > nul 2>&1
    if %errorlevel% neq 0 (
        REM Install scoop
        echo Installing Scoop...
        Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser
        Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression
    fi
    
    REM Install ffmpeg with scoop
    scoop install ffmpeg
)

REM Check that everything is installed
python -V
conda -V
ffmpeg -version

REM Ask what to run
set /p choice=What would you like to run (the webui or the script): 
if "%choice%" equ "webui" (
    python app.py
) else (
    python main.py
)

exit /b 0
