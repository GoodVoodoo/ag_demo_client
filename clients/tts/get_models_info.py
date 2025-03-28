import click
import grpc
from google.protobuf.empty_pb2 import Empty
from tabulate import tabulate

from clients.common_utils.arguments import common_options_in_settings
from clients.common_utils.auth import get_auth_metadata
from clients.common_utils.config import SettingsProtocol
from clients.common_utils.errors import errors_handler
from clients.common_utils.grpc import open_grpc_channel, print_metadata, ssl_creds_from_settings
from clients.genproto import tts_pb2, tts_pb2_grpc


@click.command(
    help="Get a list of available speech synthesis models and their parameters",
)
@errors_handler
@common_options_in_settings
def get_models_info(settings: SettingsProtocol) -> None:
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
        stub = tts_pb2_grpc.TTSStub(channel)

        response: tts_pb2.ModelsInfo
        call: grpc.Call
        response, call = stub.GetModelsInfo.with_call(
            Empty(),
            metadata=auth_metadata,
            timeout=settings.timeout,
        )

        click.echo("Response metadata:")
        print_metadata(call.initial_metadata())
        click.echo()

        model_table = [
            {
                "Name": model.name,
                "Sample Rate (Hz)": model.sample_rate_hertz,
                "Type": model.type,
                "Language": model.language_code,
            }
            for model in response.models
        ]
        model_table = sorted(
            model_table,
            key=lambda x: (x["Name"], x["Sample Rate (Hz)"], x["Type"]),
        )

        click.echo("Available models:")
        click.echo(tabulate(model_table, headers="keys", maxheadercolwidths=11))
