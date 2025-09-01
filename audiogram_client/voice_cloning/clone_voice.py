import click
import grpc
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.audio import AudioFile
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import stt_pb2, voice_cloning_pb2, voice_cloning_pb2_grpc
from .utils.arguments import common_voice_cloning_options


@click.command(help="Clone a voice from an audio file")
@errors_handler
@common_options_in_settings
@common_voice_cloning_options
def clone_voice(
    settings: SettingsProtocol,
    audio_file: str,
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

    audio = AudioFile(audio_file)

    click.echo(
        f"Request parameters:\n"
        f"Audio sample rate: {audio.sample_rate}\n"
        f"Audio channels: {audio.channel_count}\n"
    )

    audio_format = voice_cloning_pb2.AudioFormat(
        encoding=stt_pb2.LINEAR_PCM,
        sample_rate_hertz=audio.sample_rate,
        audio_channel_count=audio.channel_count,
    )

    request = voice_cloning_pb2.CloneVoiceRequest(
        audio_format=audio_format,
        signal=audio.blob,
    )

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = voice_cloning_pb2_grpc.VoiceCloningStub(channel)
        response: voice_cloning_pb2.TaskId
        response, call = stub.CloneVoice.with_call(
            request,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo(f"Voice cloning task created with ID: {response.val}")

