from pathlib import Path

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
from .utils.request import make_tts_request


@click.command(
    no_args_is_help=True,
    help="Offline (file) speech synthesis",
)
@errors_handler
@common_options_in_settings
@common_tts_options()
def synthesize(
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

        response: tts_pb2.SynthesizeSpeechResponse
        call: grpc.Call
        response, call = stub.Synthesize.with_call(
            request,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo("Response metadata:")
        print_metadata(call.initial_metadata())
        click.echo()

    click.echo(f"Received audio size: {len(response.audio)}")

    Path(output_file).write_bytes(response.audio)
    click.echo(f"Synthesized audio stored in {output_file}")
