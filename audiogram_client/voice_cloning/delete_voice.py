import click
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import voice_cloning_pb2, voice_cloning_pb2_grpc
from .utils.arguments import voice_id_option


@click.command(help="Delete a cloned voice")
@errors_handler
@common_options_in_settings
@voice_id_option
def delete_voice(
    settings: SettingsProtocol,
    voice_id: str,
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

    request = voice_cloning_pb2.DeleteVoiceRequest(voice_id=voice_id)

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = voice_cloning_pb2_grpc.VoiceCloningStub(channel)
        stub.DeleteVoice(
            request,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo(f"Voice with ID '{voice_id}' deleted successfully.")

