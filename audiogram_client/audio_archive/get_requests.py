import click
import requests
from audiogram_client.audio_archive.utils.arguments import common_options
from audiogram_client.audio_archive.utils.models import GetRequestsResponse
from audiogram_client.audio_archive.utils.response import process_response
from tabulate import tabulate


@click.command(name="requests", help="Get requests list")
@common_options
def get_requests(host: str, port: int) -> None:
    url = f"http://{host}:{port}/requests"
    response = requests.get(url)
    data = process_response(response, GetRequestsResponse)

    if not data.requests:
        click.echo("No requests found")
        return

    table = [
        [
            request.request_id,
            request.audio_id,
            request.status,
            request.timestamp,
        ]
        for request in data.requests
    ]
    click.echo(tabulate(table, headers=["Request ID", "Audio ID", "Status", "Timestamp"]))
