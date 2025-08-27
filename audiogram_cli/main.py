import sys

import click
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from audiogram_client.asr.file_recognize import file_recognize
from audiogram_client.asr.recognize import recognize
from audiogram_client.audio_archive.__main__ import audio_archive
from audiogram_client.models_service import models_info
from audiogram_client.tts.stream_synthesize import stream_synthesize
from audiogram_client.tts.synthesize import synthesize

urllib3.disable_warnings(InsecureRequestWarning)


@click.group()
def audiogram_cli():
    """A CLI for interacting with Audiogram's ASR and TTS services."""
    pass


@click.group(help="Speech-To-Text (ASR) commands")
def asr_group():
    """Group for ASR commands."""
    pass


@click.group(help="Text-To-Speech (TTS) commands")
def tts_group():
    """Group for TTS commands."""
    pass


def models_group():
    """Group for model information commands."""
    pass


asr_group.add_command(recognize, "stream")
asr_group.add_command(file_recognize, "file")

tts_group.add_command(synthesize, "file")
tts_group.add_command(stream_synthesize, "stream")

audiogram_cli.add_command(asr_group, "asr")
audiogram_cli.add_command(tts_group, "tts")
audiogram_cli.add_command(models_info, "models")
audiogram_cli.add_command(audio_archive, "archive")


def main():
    audiogram_cli()


if __name__ == "__main__":
    main()
