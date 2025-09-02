from pathlib import Path
import wave

import click
import grpc

from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, print_metadata, ssl_creds_from_settings
from audiogram_client.common_utils.types import TTSVoiceStyle
from audiogram_client.genproto import tts_pb2, tts_pb2_grpc

from .utils.arguments import common_tts_options
from .utils.definitions import AUDIO_SAVE_CHANNELS, AUDIO_SAVE_SAMPLE_WIDTH
from .utils.request import make_tts_request


@click.command(
    no_args_is_help=True,
    help="Online (stream) speech synthesis",
)
@errors_handler
@common_options_in_settings
@common_tts_options()
def stream_synthesize(
    settings: SettingsProtocol,
    text: str,
    output_file: str,
    is_ssml: bool,
    sample_rate: int,
    voice_name: str,
    model_type: str | None,
    model_sample_rate: int | None,
    voice_style: TTSVoiceStyle,
    language_code: str | None,
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

    click.echo(
        f"Request parameters:\n"
        f"Interpret text as SSML: {is_ssml}\n"
        f"Requested audio sample rate: {sample_rate}\n"
        f"Voice name: {voice_name}\n"
        f"Voice style: {voice_style}\n"
        f"Model type: {model_type or 'auto'}\n"
        f"Model sample rate: {model_sample_rate or 'auto'}\n"
        f"Language code: {language_code or 'ru (default)'}\n"
    )

    request = make_tts_request(
        text,
        is_ssml,
        voice_name,
        sample_rate,
        model_type,
        model_sample_rate,
        voice_style,
        language_code,
    )

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = tts_pb2_grpc.TTSStub(channel)

        response_iterator: Iterable[tts_pb2.StreamingSynthesizeSpeechResponse] | grpc.Call
        response_iterator = stub.StreamingSynthesize(
            request,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo("Response metadata:")
        print_metadata(response_iterator.initial_metadata())
        click.echo()

        total_audio_length = 0
        with wave.open(output_file, "wb") as wav_file:
            wav_file.setnchannels(AUDIO_SAVE_CHANNELS)
            wav_file.setsampwidth(AUDIO_SAVE_SAMPLE_WIDTH)
            wav_file.setframerate(sample_rate)

            for i_response in response_iterator:
                wav_file.writeframesraw(i_response.audio)

                chunk_length = len(i_response.audio)
                total_audio_length += chunk_length
                click.echo(f"Received audio chunk size: {chunk_length}")

        click.echo(f"Total received audio size: {total_audio_length}")
        click.echo(f"Synthesized audio stored in {output_file}")
