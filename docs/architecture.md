# Architecture Overview

This document provides a high-level overview of the Audiogram Demo Clients architecture.

## Project Structure

The project is organized into the following main directories:

- `clients/`: Contains the source code for the ASR, TTS, and other clients.
  - `asr/`: ASR-specific commands and utilities.
  - `tts/`: TTS-specific commands and utilities.
  - `common_utils/`: Shared utilities for configuration, authentication, and gRPC communication.
  - `genproto/`: Generated Python code from the `.proto` files.
- `docs/`: Project documentation.
- `proto/`: The original `.proto` files that define the gRPC service contracts.
- `tests/`: The test suite for the project.

## Core Components

- **CLI (`clients/main.py`):** The main entry point for the command-line interface, built using `click`.
- **ModelService (`clients/models_service.py`):** A service that provides a unified interface for fetching model information from the ASR and TTS services.
- **gRPC Clients:** The clients use `grpcio` to communicate with the backend gRPC services.
- **Configuration:** The clients are configured using a `config.ini` file, with settings that can be overridden by command-line arguments.
