# LLRT_whisper (Low Level Real Time whisper)
This is a not very efficient attemp to create a real time openai/whisper (Audio to Text Transcriber) But It work :)

# Audio to Text Transcriber

This project is a simple Python script that transcribes audio input from the microphone into text using the `whisper` library. The script records audio input, processes it in a queue, and transcribes the audio into text using the chosen language.

## Features

- Microphone selection
- Background noise and speech volume calibration
- Language selection
- Audio queue system
- ~~Audio storage in RAM instead of on disk~~ (Fail)

## Setup

1. Install [Miniconda](https://docs.conda.io/en/latest/miniconda.html) if you haven't already.
2. Create a new Conda environment:

`conda create --name LLRT_whisper python=3.10`

`conda activate LLRT_whisper`
