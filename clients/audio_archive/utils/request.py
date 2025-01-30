import click
import pydantic
import requests

from clients.audio_archive.utils.models import RequestsList


def try_request(url: str) -> requests.Response:
    try:
        return requests.get(url)
    except requests.ConnectionError as e:
        click.echo(f"Connection error: {e}")
        context = click.get_current_context()
        context.exit(-1)


def fetch_trace_and_session_id(
    api_address: str,
    client_id: str,
    request_id: str,
) -> tuple[str | None, str | None]:
    url = "https://" + api_address + f"/clients/{client_id}/requests"

    resp = try_request(url)

    if resp.status_code != 200:
        click.echo("Unable to fetch session and trace ids for this request")
        return None, None

    resp_json = resp.json()

    try:
        req_list = RequestsList(**resp_json)
    except pydantic.ValidationError as e:
        click.echo(f"Unable to find session and trace ids for this request: {e.errors()}")
        return None, None

    for item in req_list.data:
        if item.request_id != request_id:
            continue

        return item.trace_id, item.session_id

    return None, None
