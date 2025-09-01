# CLI Reference

This document provides a detailed reference for the `audiogram` command-line interface.

## Main Commands

The `audiogram` CLI is organized into several command groups:

- `asr`: Speech-to-Text (ASR) commands
- `tts`: Text-to-Speech (TTS) commands
- `vc`: Voice Cloning commands
- `models`: Commands for listing available models
- `archive`: Commands for interacting with the audio archive

You can get more help for any command or subcommand by using the `--help` flag.

## Global Options

The following options are available for all commands:

- `--config`: Path to the `.ini` config file.
- `--api-address`: The address of the gRPC API service.
- `--secure`: Enable/disable SSL for the gRPC connection.
- `--timeout`: Timeout in seconds for gRPC responses.

For a full list of options, run `audiogram --help`.

## Voice Cloning Commands

### `audiogram vc clone`

Creates a voice cloning task from an audio sample.

**Required Options:**
- `--audio-file PATH`: Path to the audio file containing voice samples for cloning

**Example:**
```bash
audiogram vc clone --audio-file voice_sample.wav
```

### `audiogram vc get-task-info`

Retrieves information about a voice cloning task, including its status and resulting voice ID.

**Required Options:**
- `--task-id TEXT`: The ID of the voice cloning task to query

**Example:**
```bash
audiogram vc get-task-info --task-id task_abc123
```

**Status Values:**
- `Creating`: Voice cloning is in progress
- `Ready`: Voice cloning completed successfully (voice ID will be available)
- `Error`: Voice cloning failed
- `Undefined`: Unknown status

### `audiogram vc delete`

Deletes a previously cloned voice from the system.

**Required Options:**
- `--voice-id TEXT`: The ID of the voice to delete

**Example:**
```bash
audiogram vc delete --voice-id voice_xyz789
```

## Using Cloned Voices with TTS

Once you have a voice ID from a successful cloning operation, you can use it with the TTS commands by specifying it as the `--voice-name`:

```bash
audiogram tts file --text "Your text here" --voice-name YOUR_VOICE_ID --save-to output.wav
```
