from collections.abc import Sequence
from typing import cast

import click

from clients.common_utils.arguments import options_wrapper, OptionsWrapper

from .option_types import TTSVoiceStyle


def common_tts_options() -> OptionsWrapper:
    """Inject common list of TTS-related click options to a command.

    Options:
        - text: str - text to synthesize (required)
        - output_file: str - path to output file
        - is_ssml: bool - process text as SSML
        - sample_rate: int - output audio sample rate
        - voice_name: str - voice name
        - model_type: str | None - TTS model type
        - model_sample_rate: int | None - model sample rate (optional)
        - voice_style: TTSVoiceStyle - TTS voice style
    """
    options: list = [
        click.option(
            "--text",
            required=True,
            help="text or SSML (if --read-ssml enabled) for speech synthesis",
            metavar="<text>",
        ),
        click.option(
            "--save-to",
            "output_file",
            type=click.Path(file_okay=True, dir_okay=False, writable=True),
            default="synthesized_audio.wav",
            help="output audio file path",
            metavar="<file path>",
            show_default=True,
        ),
        click.option(
            "--read-ssml",
            "is_ssml",
            is_flag=True,
            default=False,
            help="process --text as SSML (with speech markup)",
        ),
        click.option(
            "--sample-rate",
            type=int,
            default=16000,
            help="sample rate of output audio file (in hertz)",
            metavar="<hertz>",
            show_default=True,
        ),
        click.option(
            "--voice-name",
            required=True,
            help="voice name for speech synthesis (choices can be fetched via get_models_info)",
            metavar="<name>",
        ),
        click.option(
            "--model-type",
            default=None,
            help="model type for speech synthesis (choices can be fetched via get_models_info)",
            metavar="<type>",
            show_default="<auto>",
        ),
        click.option(
            "--model-sample-rate",
            type=int,
            default=None,
            help="sample rate of a model (auto by default)",
            metavar="<hertz>",
        ),
        click.option(
            "--voice-style",
            type=click.Choice(cast(Sequence[str], TTSVoiceStyle)),
            default="neutral",
            help="emotion style for speech synthesis",
            show_default=True,
        ),
    ]

    return options_wrapper(options)
