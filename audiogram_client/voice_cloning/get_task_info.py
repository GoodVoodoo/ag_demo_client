import click
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import voice_cloning_pb2, voice_cloning_pb2_grpc
from .utils.arguments import task_id_option


@click.command(help="Get information about a voice cloning task")
@errors_handler
@common_options_in_settings
@task_id_option
def get_task_info(
    settings: SettingsProtocol,
    task_id: str,
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

    request = voice_cloning_pb2.TaskId(val=task_id)

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = voice_cloning_pb2_grpc.VoiceCloningStub(channel)
        response: voice_cloning_pb2.TaskInfo
        response, call = stub.GetTaskInfo.with_call(
            request,
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        status_map = {
            voice_cloning_pb2.TaskInfo.Status.UNDEFINED: "Undefined",
            voice_cloning_pb2.TaskInfo.Status.CREATING: "Creating",
            voice_cloning_pb2.TaskInfo.Status.READY: "Ready",
            voice_cloning_pb2.TaskInfo.Status.ERROR: "Error",
        }

        click.echo(f"Task ID: {task_id}")
        click.echo(f"Status: {status_map.get(response.status, 'Unknown')}")
        if response.voice_id:
            click.echo(f"Voice ID: {response.voice_id}")

