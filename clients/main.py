import sys

import click
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from clients.asr.file_recognize import file_recognize
from clients.asr.get_models_info import get_models_info as asr_get_models_info
from clients.asr.recognize import recognize
from clients.audio_archive.__main__ import audio_archive
from clients.tts.get_models_info import get_models_info as tts_get_models_info
from clients.tts.stream_synthesize import stream_synthesize
from clients.tts.synthesize import synthesize

urllib3.disable_warnings(InsecureRequestWarning)


@click.group()
def audiogram_cli():
    pass


@click.group(help="Speech-To-Text (ASR) commands")
def asr_group():
    """Group for ASR commands."""
    pass


@click.group(help="Text-To-Speech (TTS) commands")
def tts_group():
    """Group for TTS commands."""
    pass


@click.group(help="Get information about available models")
def models_group():
    """Group for model information commands."""
    pass


asr_group.add_command(recognize, "stream")
asr_group.add_command(file_recognize, "file")
models_group.add_command(asr_get_models_info, "asr")

tts_group.add_command(synthesize, "file")
tts_group.add_command(stream_synthesize, "stream")
models_group.add_command(tts_get_models_info, "tts")

audiogram_cli.add_command(asr_group, "asr")
audiogram_cli.add_command(tts_group, "tts")
audiogram_cli.add_command(models_group, "models")
audiogram_cli.add_command(audio_archive, "archive")


def main():
    audiogram_cli()


if __name__ == "__main__":
    main()
