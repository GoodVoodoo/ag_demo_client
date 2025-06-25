import sys

import click
import urllib3
from urllib3.exceptions import InsecureRequestWarning

from clients import asr, tts
from clients.common_utils.config import create_config
from clients.models_service import models_info as comprehensive_models_info

# NB (k.zhovnovatiy): Disable warning from unsafe Keycloak connection (--verify-sso false)
urllib3.disable_warnings(InsecureRequestWarning)


@click.group()
def main() -> None:
    pass


@click.group(
    "recognize",
    help="Speech Recognition commands",
)
def asr_group() -> None:
    pass


@click.group(
    "models",
    help="Model info retrieval commands",
)
def models_group() -> None:
    pass


@click.group(
    "synthesize",
    help="Text-to-Speech (TTS) commands",
)
def tts_group() -> None:
    pass


asr_group.add_command(asr.file_recognize, "file")
asr_group.add_command(asr.recognize, "stream")

tts_group.add_command(tts.synthesize, "file")
tts_group.add_command(tts.stream_synthesize, "stream")

# Individual model info commands
models_group.add_command(asr.get_models_info, "recognize")
models_group.add_command(tts.get_models_info, "synthesize")

# Comprehensive model info command
models_group.add_command(comprehensive_models_info, "info")

main.add_command(asr_group)
main.add_command(tts_group)
main.add_command(models_group)
main.add_command(create_config, "create-config")


if __name__ == "__main__":
    sys.exit(main())
