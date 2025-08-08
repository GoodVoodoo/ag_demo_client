from collections.abc import Iterable, Sequence
from typing import cast

import click

from clients.common_utils.arguments import OptionCallable, options_wrapper, OptionsWrapper

from .definitions import DEFAULT_DEP_SMOOTHED_WINDOW_MS, DEFAULT_DEP_SMOOTHED_WINDOW_THRESHOLD
from .option_types import ASAttackType, VADAlgo, VADMode, VAResponseMode


def common_asr_options(
    default_vad_threshold: float,
    default_vad_min_silence_ms: int,
    default_vad_speech_pad_ms: int,
    default_vad_min_speech_ms: int,
) -> OptionsWrapper:
    """Inject common list of ASR-related click options to a command.

    Options:
    - audio_file: str - path to audio file (required)
    - model: str - ASR model name
    - enable_word_time_offsets: bool - enable word time offsets
    - enable_punctuator: bool - enable automatic punctuation
    - enable_denormalization: bool - enable number denormalization
    - enable_speaker_labeling: bool - enable speaker labeling by ID
    - enable_genderage: bool - enable genderage processing
    - enable_antispoofing: bool - enable spoofing detection
    - va_response_mode: VAResponseMode - VAD response mode
    - vad_algo: VADAlgo - VA algorithm choice
    - vad_mode: VADMode - VAD mode
    - vad_threshold: float - VAD threshold param
    - vad_min_silence_ms: int - VAD min_silence_ms param
    - vad_speech_pad_ms: int - VAD speech_pad_ms param
    - vad_min_speech_ms: int - VAD min_speech_ms param
    - dep_smoothed_window_threshold: float - DEP smoothed_window_threshold param
    - dep_smoothed_window_ms: int - DEP smoothed_window_ms param
    - antispoofing_attack_type: ASAttackType
    - antispoofing_far: float
    - antispoofing_frr: float
    - antispoofing_max_duration_for_analysis: int | None
    - speakers_max: int | None - max amount of speakers to label
    - speakers_num: int | None - concrete amount of speakers to label
    - wfst_dictionary_name: str - dictionary name for wFST
    - wfst_dictionary_weight: float - weight of wFST dictionary
    - enhanced_vad_beginning_window_ms: int - Enhanced VAD beginning window size in milliseconds
    - enhanced_vad_beginning_threshold: float - Enhanced VAD beginning threshold
    - enhanced_vad_ending_window_ms: int - Enhanced VAD ending window size in milliseconds
    - enhanced_vad_ending_threshold: float - Enhanced VAD ending threshold
    - target_speech_vad_beginning_window_ms: int - Target speech VAD beginning window size in milliseconds
    - target_speech_vad_beginning_threshold: float - Target speech VAD beginning threshold
    - target_speech_vad_ending_window_ms: int - Target speech VAD ending window size in milliseconds
    - target_speech_vad_ending_threshold: float - Target speech VAD ending threshold
    """
    options: list = [
        click.option(
            "--audio-file",
            required=True,
            type=click.Path(exists=True, dir_okay=False),
            help="path for audio file with recorded voice (required)",
            metavar="<.wav path>",
        ),
        click.option(
            "--model",
            default="e2e-v3",
            help="ASR model name (list can be requested with get_models_info)",
            show_default=True,
        ),
        click.option(
            "--enable-word-time-offsets",
            is_flag=True,
            default=False,
            help="enable per-word time mapping in responses",
        ),
        click.option(
            "--enable-punctuator",
            is_flag=True,
            default=False,
            help="enable automatic punctuation",
        ),
        click.option(
            "--enable-denormalization",
            is_flag=True,
            default=False,
            help="enable number denormalization (convert text numbers to actual numbers)",
        ),
        click.option(
            "--enable-speaker-labeling",
            is_flag=True,
            default=False,
            help="enable speaker labeling by ID",
        ),
        click.option(
            "--enable-genderage",
            is_flag=True,
            default=False,
            help="enable gender, age and emotion prediction",
        ),
        click.option(
            "--enable-antispoofing",
            is_flag=True,
            default=False,
            help="enable detection of spoofing attacks",
        ),
        click.option(
            "--va-response-mode",
            type=click.Choice(cast(Sequence[str], VAResponseMode)),
            default=VAResponseMode.disable,
            help="set response mode for voice activity marks",
            show_default=True,
        ),
        click.option(
            "--use-va-algo",
            "vad_algo",
            type=click.Choice(cast(Sequence[str], VADAlgo)),
            default=VADAlgo.vad,
            help="set voice activity detection algorithm",
            show_default=True,
        ),
        *_vad_options(
            default_vad_threshold,
            default_vad_min_silence_ms,
            default_vad_speech_pad_ms,
            default_vad_min_speech_ms,
        ),
        *_dep_options(),
        *_antispoofing_options(),
        *_speaker_labeling_options(),
        *_wfst_dictionary_options(),
        click.option(
            "--enhanced-vad-beginning-window-ms",
            type=int,
            default=200,
            help="Enhanced VAD beginning window size in milliseconds",
        ),
        click.option(
            "--enhanced-vad-beginning-threshold",
            type=float,
            default=0.5,
            help="Enhanced VAD beginning threshold",
        ),
        click.option(
            "--enhanced-vad-ending-window-ms",
            type=int,
            default=200,
            help="Enhanced VAD ending window size in milliseconds",
        ),
        click.option(
            "--enhanced-vad-ending-threshold",
            type=float,
            default=0.5,
            help="Enhanced VAD ending threshold",
        ),
        click.option(
            "--target-speech-vad-beginning-window-ms",
            type=int,
            default=200,
            help="Target speech VAD beginning window size in milliseconds",
        ),
        click.option(
            "--target-speech-vad-beginning-threshold",
            type=float,
            default=0.5,
            help="Target speech VAD beginning threshold",
        ),
        click.option(
            "--target-speech-vad-ending-window-ms",
            type=int,
            default=200,
            help="Target speech VAD ending window size in milliseconds",
        ),
        click.option(
            "--target-speech-vad-ending-threshold",
            type=float,
            default=0.5,
            help="Target speech VAD ending threshold",
        ),
    ]

    return options_wrapper(options)


def _vad_options(
    default_vad_threshold: float,
    default_vad_min_silence_ms: int,
    default_vad_speech_pad_ms: int,
    default_vad_min_speech_ms: int,
) -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--vad-mode",
            "vad_mode",
            type=click.Choice(cast(Sequence[str], VADMode)),
            default=VADMode.default,
            help="set voice activity detection mode",
            show_default=True,
        ),
        click.option(
            "--vad-threshold",
            "vad_threshold",
            type=float,
            default=default_vad_threshold,
            help="override VAD threshold parameter",
            show_default=True,
        ),
        click.option(
            "--vad-min-silence-ms",
            "vad_min_silence_ms",
            type=int,
            default=default_vad_min_silence_ms,
            help="override VAD min_silence_ms parameter",
            show_default=True,
        ),
        click.option(
            "--vad-speech-pad-ms",
            "vad_speech_pad_ms",
            type=int,
            default=default_vad_speech_pad_ms,
            help="override VAD speech_pad_ms parameter",
            show_default=True,
        ),
        click.option(
            "--vad-min-speech-ms",
            "vad_min_speech_ms",
            type=int,
            default=default_vad_min_speech_ms,
            help="override VAD min_speech_ms parameter",
            show_default=True,
        ),
    ]

    return options


def _dep_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--dep-smoothed-window-threshold",
            "dep_smoothed_window_threshold",
            type=float,
            default=DEFAULT_DEP_SMOOTHED_WINDOW_THRESHOLD,
            help="override DEP smoothed_window_threshold parameter",
            show_default=True,
        ),
        click.option(
            "--dep-smoothed-window-ms",
            "dep_smoothed_window_ms",
            type=int,
            default=DEFAULT_DEP_SMOOTHED_WINDOW_MS,
            help="override DEP smoothed_window_ms parameter",
            show_default=True,
        ),
    ]

    return options


def _antispoofing_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--as-attack-type",
            "antispoofing_attack_type",
            type=click.Choice(cast(Sequence[str], ASAttackType)),
            default=ASAttackType.logical,
            help="set attack type to detect with antispoofing service",
            show_default=True,
        ),
        click.option(
            "--as-far",
            "antispoofing_far",
            type=float,
            help="set max allowed False Acceptance Rate (not detected attacks) for antispoofing",
        ),
        click.option(
            "--as-frr",
            "antispoofing_frr",
            type=float,
            help="set max allowed False Rejection Rate (genuine audio detected as an attack) "
            "for antispoofing",
        ),
        click.option(
            "--as-max-duration-for-analysis",
            "antispoofing_max_duration_for_analysis",
            type=click.IntRange(min=0),
            help="set max audio chunk length in milliseconds",
        ),
    ]

    return options


def _speaker_labeling_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--speakers-max",
            type=click.IntRange(min=0),
            help="set max amount of speakers for labeling",
        ),
        click.option(
            "--speakers-num",
            type=click.IntRange(min=0),
            help="set number of speakers that must be labeled",
        ),
    ]

    return options


def _wfst_dictionary_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--dictionary-name",
            "wfst_dictionary_name",
            default="",
            help="set wFST dictionary name to amplify recognition of words in that dictionary",
        ),
        click.option(
            "--dictionary-weight",
            "wfst_dictionary_weight",
            type=click.FloatRange(-1, 1),
            default=0,
            show_default=True,
            help="set weight for specified wFST dictionary",
        ),
    ]

    return options
