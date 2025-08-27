from typing import Any

import click
import pydantic
import requests

from audiogram_client.audio_archive.utils.request import get_requests_list
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler


def _format_list_url(
    api_address: str,
    client_id: str,
    session_id: str | None,
    trace_id: str | None,
) -> str:
    url = f"https://{api_address}/clients/{client_id}"

    if session_id:
        return f"{url}/sessions/{session_id}/requests"

    if trace_id:
        return f"{url}/traces/{trace_id}/requests"

    return f"{url}/requests"


def _print_request_list(resp_json: dict[str, Any]) -> None:
    try:
        req_list = RequestsList(**resp_json)
    except pydantic.ValidationError as e:
        click.echo("Errors happened during validation of response JSON:")
        click.echo(e.errors())
        return

    click.echo(f"Found {len(req_list.data)} request(s):\n")
    for index, item in enumerate(req_list.data):
        if index > 0:
            click.echo()  # Separator line

        click.echo(f"Request: {item.request_id}")
        click.echo(f"Created at: {item.created_at}")
        if item.trace_id:
            click.echo(f"Trace ID: {item.trace_id}")
        if item.session_id:
            click.echo(f"Session ID: {item.session_id}")


@click.command(
    "list-requests",
    help="List client requests in audio archive",
)
@common_options_in_settings()
def get_requests(
    api_address: str,
    client_id: str,
    session_id: str | None,
    trace_id: str | None,
) -> None:
    context = click.get_current_context()
    if session_id and trace_id:
        context.fail("Wrong parameters: filtering is supported either by session id or trace id")

    url = _format_list_url(api_address, client_id, session_id, trace_id)

    resp = try_request(url)

    if resp.status_code == 404:
        click.echo("Requests for those parameters were not found")
        context.exit(-1)

    try:
        resp.raise_for_status()
    except requests.HTTPError as e:
        click.echo(f"HTTP Error occured during request: {e}")
        context.exit(-1)

    _print_request_list(resp.json())
