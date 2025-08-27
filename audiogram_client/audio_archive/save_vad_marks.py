from pathlib import Path

import click
import pydantic

from audiogram_client.audio_archive.utils.request import get_vad_marks
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler


@click.command(
    "save-vad-marks",
    help="Fetch VAD marks of a request by its ID",
)
@common_options_in_settings()
def save_vad_marks(
    settings: SettingsProtocol,
    request_id: str,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{settings.api_address}/clients/{settings.client_id}/requests/{request_id}/voice_activity_marks"

    resp = errors_handler.try_request(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    resp_json = resp.json()

    try:
        marks_list = get_vad_marks(**resp_json)
    except pydantic.ValidationError as e:
        click.echo("Errors happened during validation of response JSON:")
        click.echo(e.errors())
        return

    trace_id, session_id = errors_handler.fetch_trace_and_session_id(settings.api_address, settings.client_id, request_id)

    path = errors_handler.save_file_dir(settings.client_id, request_id, trace_id, session_id, save_dir)
    path.mkdir(parents=True, exist_ok=True)
    path = path / "vad_marks.txt"

    with path.open("w") as f:
        for index, mark in enumerate(marks_list.data, start=1):
            f.write(f"Mark #{index} Type: {mark.mark_type} Offset: {mark.offset_ms}ms\n")

    click.echo(f"Successfully saved to {path}")
