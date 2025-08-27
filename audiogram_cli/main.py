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
from audiogram_client.voice_cloning.clone_voice import clone_voice
from audiogram_client.voice_cloning.delete_voice import delete_voice
from audiogram_client.voice_cloning.get_task_info import get_task_info

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


@click.group(help="Voice Cloning commands")
def voice_cloning_group():
    """Group for Voice Cloning commands."""
    pass


def models_group():
    """Group for model information commands."""
    pass


asr_group.add_command(recognize, "stream")
asr_group.add_command(file_recognize, "file")

tts_group.add_command(synthesize, "file")
tts_group.add_command(stream_synthesize, "stream")

voice_cloning_group.add_command(clone_voice, "clone")
voice_cloning_group.add_command(get_task_info, "get-task-info")
voice_cloning_group.add_command(delete_voice, "delete")

audiogram_cli.add_command(asr_group, "asr")
audiogram_cli.add_command(tts_group, "tts")
audiogram_cli.add_command(voice_cloning_group, "vc")
audiogram_cli.add_command(models_info, "models")
audiogram_cli.add_command(audio_archive, "archive")


def main():
    audiogram_cli()


if __name__ == "__main__":
    main()
