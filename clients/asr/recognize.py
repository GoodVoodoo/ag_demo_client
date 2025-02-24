from collections.abc import Iterable

import click
import grpc

from clients.common_utils.arguments import common_options_in_settings
from clients.common_utils.audio import AudioFile
from clients.common_utils.auth import get_auth_metadata
from clients.common_utils.config import SettingsProtocol
from clients.common_utils.errors import errors_handler
from clients.common_utils.grpc import open_grpc_channel, print_metadata, ssl_creds_from_settings
from clients.genproto import stt_pb2, stt_pb2_grpc

from .utils.arguments import common_asr_options
from .utils.definitions import (
    CHUNK_LEN_MS,
    DEFAULT_VAD_S_MIN_SILENCE_MS,
    DEFAULT_VAD_S_MIN_SPEECH_MS,
    DEFAULT_VAD_S_SPEECH_PAD_MS,
    DEFAULT_VAD_S_THRESHOLD,
)
from .utils.option_types import ASAttackType, VADAlgo, VADMode, VAResponseMode
from .utils.request import (
    make_antispoofing_config,
    make_context_dictionary_config,
    make_recognition_config,
    make_speaker_labeling_config,
    make_va_config,
    stream_request_iterator,
)
from .utils.response import print_recognize_response


@click.command(
    help="Online (stream) speech recognition",
)
@errors_handler
@common_options_in_settings
@common_asr_options(
    DEFAULT_VAD_S_THRESHOLD,
    DEFAULT_VAD_S_MIN_SILENCE_MS,
    DEFAULT_VAD_S_SPEECH_PAD_MS,
    DEFAULT_VAD_S_MIN_SPEECH_MS,
)
@click.option(
    "--single-utterance",
    is_flag=True,
    default=False,
    help="make recognition only for first continuous speech segment",
)
@click.option(
    "--interim-results",
    is_flag=True,
    default=False,
    help="show partly recognized results (when phrase recognition is not complete)",
)
@click.option(
    "--rt",
    "realtime",
    is_flag=True,
    default=False,
    help="enable emulation of real-time audio streaming",
)
@click.option(
    "--chunk-len",
    "chunk_len_ms",
    type=click.IntRange(500, 2000),
    default=CHUNK_LEN_MS,
    help="set audio chunk length in milliseconds (from 500 to 2000)",
)
def recognize(
    settings: SettingsProtocol,
    audio_file: str,
    model: str,
    enable_word_time_offsets: bool,
    enable_punctuator: bool,
    enable_denormalization: bool,
    enable_speaker_labeling: bool,
    enable_genderage: bool,
    enable_antispoofing: bool,
    va_response_mode: VAResponseMode,
    vad_algo: VADAlgo,
    vad_mode: VADMode,
    vad_threshold: float,
    vad_speech_pad_ms: int,
    vad_min_silence_ms: int,
    vad_min_speech_ms: int,
    dep_smoothed_window_threshold: float,
    dep_smoothed_window_ms: int,
    antispoofing_attack_type: ASAttackType | None,
    antispoofing_far: int | None,
    antispoofing_frr: int | None,
    antispoofing_max_duration_for_analysis: int | None,
    speakers_max: int | None,
    speakers_num: int | None,
    wfst_dictionary_name: str,
    wfst_dictionary_weight: float,
    single_utterance: bool,
    interim_results: bool,
    realtime: bool,
    chunk_len_ms: int,
    enhanced_vad_beginning_window_ms: int,
    enhanced_vad_beginning_threshold: float,
    enhanced_vad_ending_window_ms: int,
    enhanced_vad_ending_threshold: float,
    target_speech_vad_beginning_window_ms: int,
    target_speech_vad_beginning_threshold: float,
    target_speech_vad_ending_window_ms: int,
    target_speech_vad_ending_threshold: float,
) -> None:
    auth_metadata = get_auth_metadata(
        settings.sso_url,
        settings.realm,
        settings.client_id,
        settings.client_secret,
        settings.iam_account,
        settings.iam_workspace,
        settings.verify_sso,
    )
    
    # Add required headers for v3
    auth_metadata.append(("x-ai-account", "demo"))
    auth_metadata.append(("x-ai-workspace", "default"))

    audio = AudioFile(audio_file)

    click.echo(
        f"Request parameters:\n"
        f"Audio sample rate: {audio.sample_rate}\n"
        f"Audio channels: {audio.channel_count}\n"
        f"VAD algorithm: {vad_algo.name.upper()}\n"
        f"Genderage enabled: {enable_genderage}\n"
        f"Punctuator enabled: {enable_punctuator}\n"
        f"Denormalization enabled: {enable_denormalization}\n"
        f"Speaker labeling enabled: {enable_speaker_labeling}\n"
        f"Word time offsets enabled: {enable_word_time_offsets}\n"
        f"Antispoofing enabled: {enable_antispoofing}\n"
        f"Single utterance enabled: {single_utterance}\n"
        f"Interim results enabled: {interim_results}\n"
    )

    va_config = make_va_config(
        vad_algo,
        vad_mode,
        vad_threshold,
        vad_min_silence_ms,
        vad_speech_pad_ms,
        vad_min_speech_ms,
        dep_smoothed_window_threshold,
        dep_smoothed_window_ms,
        enhanced_vad_beginning_window_ms,
        enhanced_vad_beginning_threshold,
        enhanced_vad_ending_window_ms,
        enhanced_vad_ending_threshold,
        target_speech_vad_beginning_window_ms,
        target_speech_vad_beginning_threshold,
        target_speech_vad_ending_window_ms,
        target_speech_vad_ending_threshold,
    )
    as_config = make_antispoofing_config(
        enable_antispoofing,
        antispoofing_attack_type,
        antispoofing_far,
        antispoofing_frr,
        antispoofing_max_duration_for_analysis,
    )
    sl_config = make_speaker_labeling_config(
        enable_speaker_labeling,
        speakers_max,
        speakers_num,
    )
    wfst_config = make_context_dictionary_config(
        wfst_dictionary_name,
        wfst_dictionary_weight,
    )
    recognition_config = make_recognition_config(
        model,
        va_config,
        va_response_mode,
        audio.sample_rate,
        audio.channel_count,
        enable_genderage,
        enable_word_time_offsets,
        enable_punctuator,
        enable_denormalization,
        as_config,
        sl_config,
        wfst_config,
    )
    stream_recognition_config = stt_pb2.StreamRecognitionConfig(
        config=recognition_config,
        single_utterance=single_utterance,
        interim_results=interim_results,
    )
    request_iterator = stream_request_iterator(
        stream_recognition_config,
        audio.chunks(chunk_len_ms),
        chunk_len_ms if realtime else 0,
    )

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = stt_pb2_grpc.STTStub(channel)

        response_iterator: Iterable[stt_pb2.StreamRecognitionConfig] | grpc.Call
        response_iterator = stub.Recognize(
            request_iterator,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo("Response metadata:")
        print_metadata(response_iterator.initial_metadata())

        for response_idx, response in enumerate(response_iterator, 1):
            click.echo(f"\nResponse #{response_idx}:")
            print_recognize_response(response)
