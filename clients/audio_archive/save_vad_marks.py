from pathlib import Path

import click
import pydantic

from clients.audio_archive.utils.arguments import download_options
from clients.audio_archive.utils.models import VAMarkList
from clients.audio_archive.utils.request import fetch_trace_and_session_id, try_request
from clients.audio_archive.utils.response import save_file_dir


@click.command(
    "vad-marks",
    help="Fetch VAD marks of a request by its ID",
)
@download_options()
def save_vad_marks(
    api_address: str,
    client_id: str,
    request_id: str,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{api_address}/clients/{client_id}/requests/{request_id}/voice_activity_marks"

    resp = try_request(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    resp_json = resp.json()

    try:
        marks_list = VAMarkList(**resp_json)
    except pydantic.ValidationError as e:
        click.echo("Errors happened during validation of response JSON:")
        click.echo(e.errors())
        return

    trace_id, session_id = fetch_trace_and_session_id(api_address, client_id, request_id)

    path = save_file_dir(client_id, request_id, trace_id, session_id, save_dir)
    path.mkdir(parents=True, exist_ok=True)
    path = path / "vad_marks.txt"

    with path.open("w") as f:
        for index, mark in enumerate(marks_list.data, start=1):
            f.write(f"Mark #{index} Type: {mark.mark_type} Offset: {mark.offset_ms}ms\n")

    click.echo(f"Successfully saved to {path}")
