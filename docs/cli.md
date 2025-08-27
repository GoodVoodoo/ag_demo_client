# CLI Reference

This document provides a detailed reference for the `audiogram` command-line interface.

## Main Commands

The `audiogram` CLI is organized into several command groups:

- `asr`: Speech-to-Text (ASR) commands
- `tts`: Text-to-Speech (TTS) commands
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
