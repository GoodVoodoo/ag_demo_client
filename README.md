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
└── Replay/               # Directory for replay files
```

## Prerequisites

- Python 3.x
- Required Python packages (specified in pyproject.toml)

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