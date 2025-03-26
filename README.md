# Demo Clients

This project provides client implementations for various services, with a focus on Text-to-Speech (TTS) and Automatic Speech Recognition (ASR) functionality.

## Features

- Text-to-Speech (TTS) synthesis
  - File-based synthesis
  - Streaming synthesis
- Automatic Speech Recognition (ASR)
  - File-based recognition
  - Streaming recognition
- Model information retrieval
- Common utilities for authentication and configuration
- gRPC client implementations
- Audio Format Conversion
  - Multiple format support (MP4, MP3, WAV, M4A, AAC, OGG, FLAC)
  - Optimized output for speech recognition
  - Video audio extraction
  - Detailed media information

## Project Structure

```
.
├── clients/
│   ├── asr/                 # Automatic Speech Recognition implementation
│   ├── tts/                 # Text-to-Speech implementation
│   ├── genproto/           # Generated protocol buffers
│   ├── audio_archive/      # Audio archive functionality
│   ├── common_utils/       # Common utilities shared across clients
│   │   ├── auth.py        # Authentication utilities
│   │   ├── audio.py       # Audio processing utilities
│   │   ├── config.py      # Configuration management
│   │   └── grpc.py        # gRPC client utilities
│   └── main.py            # Main CLI implementation
├── TTSOutput/             # Directory for TTS output files
├── Replay/               # Directory for replay files
├── audio_converter.py    # Audio format converter utility
└── output/              # Default directory for converted audio files
```

## Prerequisites

- Python 3.8 or higher
- Required Python packages (specified in pyproject.toml)
- FFmpeg (required for audio conversion)

### Installing FFmpeg (for audio conversion)

#### Windows
```bash
# Using winget (Windows Package Manager)
winget install Gyan.FFmpeg

# Or download from the official website:
# https://ffmpeg.org/download.html#build-windows
```

#### Linux
```bash
# Ubuntu/Debian
sudo apt-get update
sudo apt-get install ffmpeg

# Fedora
sudo dnf install ffmpeg
```

## Installation

1. Clone the repository:
```bash
git clone [repository-url]
```

2. Create and activate a virtual environment:
```bash
python -m venv venv
# On Windows
.\venv\Scripts\activate
# On Unix or MacOS
source venv/bin/activate
```

3. Install dependencies

$ pip install -e .

## Configuration

1. Create a new configuration:
```

## Usage

### Automatic Speech Recognition (ASR)

Check your current directory:
```bash
pwd
```

Use the following command to transcribe an audio file:
```bash
python -m clients.main recognize file --audio-file path/to/audio/file.wav --config config.ini
```

Additional options:
- `--enable-antispoofing`: Enable anti-spoofing detection
- `--enable-punctuator`: Enable automatic punctuation

Example:
```bash
python -m clients.main recognize file --audio-file .\Replay\1297.wav --config config.ini --enable-antispoofing --enable-punctuator
```

### Text-to-Speech (TTS)

Check your current directory:
```bash
pwd
```

Use the following command to synthesize speech from text:
```bash
python -m clients.main synthesize file --text "Your text here" --config config.ini --save-to output.wav
```

Additional options:
- `--voice-name`: Specify the voice to use (e.g., borisova)
- `--sample-rate`: Set the output sample rate (e.g., 44100)
- `--model-type`: Specify the model quality (e.g., high_quality)
- `--voice-style`: Set the voice style (e.g., neutral)

Example:
```bash
python -m clients.main synthesize file --text "Привет, как дела?" --config config.ini --voice-name borisova --save-to output.wav --sample-rate 44100 --model-type high_quality --voice-style neutral
```

### SSML Support

The TTS system supports Speech Synthesis Markup Language (SSML) for more control over speech synthesis:

Basic emphasis:
```bash
python -m clients.main synthesize file --text "<speak>Почему <emphasis strength='strong'>они</emphasis> не согласны?</speak>" --config config.ini --save-to output.wav
```

Number formatting:
```bash
python -m clients.main synthesize file --text "<speak><say-as interpret-as='cardinal' format='feminine_nominative'>1</say-as> ложка</speak>" --config config.ini --save-to output.wav
```

Date formatting:
```bash
python -m clients.main synthesize file --text "<speak>Следующее списание произойдёт <say-as interpret-as='date' format='genitive' detail='d.m'>21.12</say-as>.</speak>" --config config.ini --save-to output.wav
```