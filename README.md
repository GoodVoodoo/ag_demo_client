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

3. Install dependencies:
```bash
pip install .
```

## Configuration

1. Create a new configuration:
```bash
python -m clients create-config
```

2. Update the generated configuration file with your settings

## Usage

The client provides a command-line interface with the following main commands:

### Text-to-Speech (TTS)
```bash
# Synthesize text to an audio file
python -m clients synthesize file [OPTIONS]

# Stream synthesis
python -m clients synthesize stream [OPTIONS]

# Get available TTS models
python -m clients models synthesize
```

### Speech Recognition (ASR)
```bash
# Recognize speech from an audio file
python -m clients recognize file [OPTIONS]

# Stream recognition
python -m clients recognize stream [OPTIONS]

# Get available ASR models
python -m clients models recognize
```

For detailed options for each command, use the --help flag:
```bash
python -m clients --help
python -m clients synthesize --help
python -m clients recognize --help
```

### Audio Format Conversion

The project includes an audio converter utility that prepares audio files for speech recognition:

```bash
# Convert any supported audio/video file to WAV
python audio_converter.py input_file.mp4

# Specify custom output directory
python audio_converter.py input_file.mp3 --output-dir my_output

# List supported formats
python audio_converter.py --list-formats
```

#### Supported Audio Formats
- `.mp4` - Video files with audio
- `.mp3` - MP3 audio
- `.wav` - WAV audio
- `.m4a` - M4A audio
- `.aac` - AAC audio
- `.ogg` - OGG audio
- `.flac` - FLAC audio

#### Output Format
All audio is converted to a standardized format suitable for speech recognition:
- Mono channel
- 16kHz sample rate
- 16-bit PCM WAV encoding

#### Example Conversion Output
```
Processing file: input.mp4
Input format: .mp4

Video information:
Resolution: 1920x1080
Duration: 65.3 seconds
Bitrate: 2500 kbps

Audio information:
Codec: aac
Sample rate: 48000 Hz
Channels: 2
Bit rate: 128 kbps

Converting to speech recognition format...
Extracting and converting audio from video...
Processing audio to speech recognition format...
Converted to: C:\path\to\output\output.wav

Success! Final WAV file: C:\path\to\output\output.wav
The WAV file is now ready for speech recognition
```