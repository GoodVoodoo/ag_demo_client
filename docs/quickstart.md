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

Alternatively, you can configure the client using environment variables. All settings in the `config.ini` file can be overridden by environment variables prefixed with `AUDIOGRAM_`. For example, to set the API address, you would use an environment variable named `AUDIOGRAM_API_ADDRESS`.

## Usage

The main entry point for the CLI is `audiogram`. You can see a list of available commands by running:

```bash
audiogram --help
```

Here are some examples of how to use the ASR, TTS, and Voice Cloning clients:

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

### Voice Cloning

Voice cloning allows you to create personalized voices from audio samples. The process involves three main steps:

#### 1. Clone a Voice

First, create a voice cloning task from an audio sample:

```bash
audiogram vc clone --audio-file /path/to/voice/sample.wav
```

This returns a task ID that you'll use to check the status.

#### 2. Check Cloning Status

Monitor the cloning progress using the task ID:

```bash
audiogram vc get-task-info --task-id YOUR_TASK_ID
```

Wait until the status shows "Ready" and note the voice ID.

#### 3. Use Your Cloned Voice

Once ready, use the cloned voice for speech synthesis:

```bash
audiogram tts file --text "Hello from my cloned voice!" --voice-name YOUR_VOICE_ID --save-to cloned_speech.wav
```

#### Optional: Delete a Cloned Voice

When no longer needed, delete the cloned voice:

```bash
audiogram vc delete --voice-id YOUR_VOICE_ID
```

**Important:** Voice cloning involves personal data. Ensure you have proper consent before cloning someone's voice and comply with applicable privacy laws.
