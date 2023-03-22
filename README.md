# LLRT_whisper (Low Level Real Time whisper)
This is a not very efficient attemp to create a real time openai/whisper (Audio to Text Transcriber) But It work :)

## Audio to Text Transcriber

This project is a simple Python script that transcribes audio input from the microphone into text using the `whisper` library. The script records audio input, processes it in a queue, and transcribes the audio into text using the chosen language.

## Features

- Microphone selection
- Background noise and speech volume calibration (For speech detection)
- Language selection
- Audio queue system
- ~~Audio storage in RAM instead of on disk~~ (Fail)


## How It Works

The script follows these steps:

1. Microphone selection: Allows the user to choose the desired microphone to record audio input.
2. Threshold selection: Users can choose from using the previous calibration, start a new calibration, or manually set a threshold.
3. Language selection: Users can choose the language for transcription or use auto-detection.
4. Record audio input: The script records audio input from the microphone and stores it in a queue.
5. Process audio queue: Another thread processes the audio queue, transcribes the audio into text using the chosen language, and prints the result.

## Notes

- This script is compatible with Python 3.10
- The supported audio formats for the `whisper` library are .wav and .mp3.


## Requirements

- Python 3.10


## Setup (CPU Only version)

#### 1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.
#### 2. Create a new Conda environment:

  `conda create --name LLRT_whisper python=3.10`

  `conda activate LLRT_whisper`
  
#### 3. Install the required libraries:

`pip install pyaudio`

`pip install whisper`

#### 4. To ensure the `whisper` library functions correctly, you also need to have `ffmpeg` installed on your system. Below are instructions for installing `ffmpeg` on different platforms.

### Installing ffmpeg

```bash

# Ubuntu or Debian

`sudo apt update && sudo apt install ffmpeg`

# Arch Linux

sudo pacman -S ffmpeg

# MacOS (using Homebrew) If you don't have Homebrew installed, you can install it from https://brew.sh/.

brew install ffmpeg

# Windows (using Chocolatey) If you don't have Chocolatey installed, you can install it from https://chocolatey.org/.

choco install ffmpeg

# Windows (using Scoop) If you don't have Scoop installed, you can install it from https://scoop.sh/.

scoop install ffmpeg

```

#### 4. Clone the repository: 

`git clone https://github.com/Megumin6626/LLRT_whisper.git`

#### 5. Change to the project directory: 

`cd LLRT_whisper`

#### 6. Run the script to start: 

`python Whisper_RT_CPU_Only.py`

Follow the on-screen instructions to set up the microphone, threshold, and language.

After the initial setup, the script will continuously listen to your microphone and transcribe the audio in real-time.

# Enable GPU acceleration

#### Before continuous you should have the CPU version setup make sure it work.

This guide will help you set up and run the GPU version of the real-time transcription script using OpenAI's `whisper` library.

## Requirements

- CUDA Toolkit 11.7

## Setup

### Installing CUDA Toolkit 11.7

Follow the instructions on the NVIDIA website to install the [CUDA Toolkit 11.7](https://developer.nvidia.com/cuda-toolkit-archive).

### Installing Python Dependencies

In the same environment, run the following commands:

```bash
pip3 install torch torchvision torchaudio --index-url https://download.pytorch.org/whl/cu117
pip install torchaudio
pip install soundfile
```
## Testing GPU Support

After installing the dependencies, run the GPU_test.py script to check if your GPU is working properly:

`python GPU_test.py`

If the GPU is working, you should see the following output:

```bash
Torch version: 2.0.0+cu117
CUDA available: True
```

## Running the GPU-Enabled Transcription Script

Once your GPU is set up and working, run the Whisper_RT_GPU.py script to start the real-time transcription with GPU support:

`python Whisper_RT_GPU.py`

Follow the on-screen instructions to set up the microphone, threshold, and language.

After the initial setup, the script will continuously listen to your microphone and transcribe the audio in real-time using your GPU.

## Code explan

#### `get_unique_devices(p)`

This function takes a PyAudio object and returns a dictionary of unique audio devices (microphones) found on the system.

#### `save_microphone_index(mic_index)` and `load_microphone_index()`

These functions save and load the previously chosen microphone index to a file ("microphones_setting.txt").

#### `record_audio(threshold, audio_queue)`

This function records audio from the selected microphone and stores the recorded audio as a wave file. It uses a threshold value to determine when to start and stop recording. The recorded audio files are added to a queue for further processing.
How fast the recording will stop when it is silence can be chage here


`if silent_frames > 0.6 * RATE / CHUNK: # stop recording after 0.6 seconds of silence`

#### `process_audio_queue(audio_queue, language)`

This function takes the audio queue and language as input, loads the Whisper model, and transcribes the audio files in the queue. The transcribed text is then printed on the screen.

#### `measure_threshold()`

This function measures the sound intensity of background noise and speech levels to determine a suitable threshold for starting and stopping audio recording.
The threshold calculated using `threshold = (background + speech) / 2`


#### `save_threshold(threshold)` and `load_threshold()`

These functions save and load the previously measured threshold value to a file ("threshold.txt").

#### `choose_threshold()`

This function allows the user to choose how to set the threshold value: use the previously saved threshold, measure a new threshold, or enter a custom threshold value.

#### `save_language(language)` and `load_language()`

These functions save and load the previously chosen language for transcription to a file ("language_settings.txt").

#### `choose_language()`

This function allows the user to choose the input language for transcription.
