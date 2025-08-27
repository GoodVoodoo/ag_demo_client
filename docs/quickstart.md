# Quickstart

This guide will help you get up and running with the Audiogram Demo Clients.

## Installation

You can install the clients directly from the source repository:

```bash
git clone <repository_url>
cd audiogram-demo-clients
pip install -e .
```

## Configuration

Before you can use the clients, you need to create a `config.ini` file. A template is provided in `clients/common_utils/config_files/settings_template.ini`. Copy this file to the root of the project and rename it to `config.ini`, then fill in your credentials.

## Usage

The main entry point for the CLI is `audiogram`. You can see a list of available commands by running:

```bash
audiogram --help
```

Here are some examples of how to use the ASR and TTS clients:

### ASR (Speech-to-Text)

To transcribe an audio file:

```bash
audiogram asr file --audio-file /path/to/your/audio.wav
```

### TTS (Text-to-Speech)

To synthesize speech from text:

```bash
audiogram tts file --text "Hello, world!" --save-to output.wav --voice-name elena
```
