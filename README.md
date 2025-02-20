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