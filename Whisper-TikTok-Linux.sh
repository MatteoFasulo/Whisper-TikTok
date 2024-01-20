#!/bin/bash

# Check if conda is installed
if command -v conda &> /dev/null
then
    echo "Conda is already installed."
else
    # If not installed, install the latest version of conda
    echo "Installing Conda..."
    wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh
    bash miniconda.sh -b -p $HOME/miniconda3
    rm miniconda.sh
fi

# Create a conda environment with Python 3.11
conda create -n WhisperTikTok python=3.11 -y

# Activate the conda environment
source $HOME/miniconda3/bin/activate WhisperTikTok

# Clone the repository
git clone https://github.com/MatteoFasulo/Whisper-TikTok.git

# Enter the repository
cd Whisper-TikTok

# Install dependencies
pip install -U -r requirements.txt

# Check if ffmpeg is installed
if command -v ffmpeg &> /dev/null
then
    echo "FFmpeg is already installed."
else
    # Check if scoop is installed
    if command -v scoop &> /dev/null
    then
        # Install ffmpeg with scoop
        scoop install ffmpeg
    else
        # Install scoop
        echo "Installing Scoop..."
        powershell -command "Set-ExecutionPolicy -ExecutionPolicy RemoteSigned -Scope CurrentUser; Invoke-RestMethod -Uri https://get.scoop.sh | Invoke-Expression"
        scoop install ffmpeg
    fi
fi

# Check that everything is installed
python --version
conda --version
ffmpeg --version

# Ask what to run
read -p "What would you like to run (the webui or the script): " choice
if [ "$choice" = "webui" ]; then
    python app.py
else
    python main.py
fi