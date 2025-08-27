import click
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.auth import get_auth_metadata
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler
from audiogram_client.common_utils.grpc import open_grpc_channel, ssl_creds_from_settings
from audiogram_client.genproto import stt_pb2, stt_pb2_grpc
from google.protobuf import empty_pb2


@click.command(help="Get ASR models info")
@errors_handler
@common_options_in_settings
def get_models_info(
    settings: SettingsProtocol,
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

    click.echo(f"Connecting to gRPC server - {settings.api_address}\n")

    with open_grpc_channel(
        settings.api_address,
        ssl_creds_from_settings(settings),
    ) as channel:
        stub = stt_pb2_grpc.STTStub(channel)
        response: stt_pb2.ModelsInfo
        response, call = stub.GetModelsInfo.with_call(
            empty_pb2.Empty(),
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        for model in response.models:
            click.echo(f"Model: {model.name}")
            click.echo(f"  Sample rate: {model.sample_rate_hertz}")
            click.echo(f"  Language code: {model.language_code}")
            click.echo(f"  Dictionaries: {', '.join(model.dictionary_name)}")
