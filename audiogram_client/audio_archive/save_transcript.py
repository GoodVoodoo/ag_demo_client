from pathlib import Path

import click
import pydantic

from audiogram_client.audio_archive.utils.request import get_transcript
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler


@click.command(
    "save-transcript",
    help="Fetch transcript of a request by its ID",
)
@common_options_in_settings()
def save_transcript(
    api_address: str,
    client_id: str,
    request_id: str,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{api_address}/clients/{client_id}/requests/{request_id}/transcript"

    resp = errors_handler(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    resp_json = resp.json()

    try:
        transcript_list = pydantic.parse_obj_as(get_transcript, resp_json)
    except pydantic.ValidationError as e:
        click.echo("Errors happened during validation of response JSON:")
        click.echo(e.errors())
        return

    trace_id, session_id = errors_handler(api_address, client_id, request_id)

    path = errors_handler(client_id, request_id, trace_id, session_id, save_dir)
    path.mkdir(parents=True, exist_ok=True)
    path = path / "transcript.txt"

    with path.open("w") as f:
        for index, transcript in enumerate(transcript_list.data, start=1):
            f.write(
                f"Transcript #{index} ({transcript.start_time}s-{transcript.end_time}s): "
                f'"{transcript.transcript}" '
                f"confidence: {transcript.confidence:.4g}\n"
            )

            for word in transcript.words:
                f.write(
                    f"  {word.start_time}s-{word.end_time}s: "
                    f'"{word.word}" '
                    f"confidence: {word.confidence:.4g}\n"
                )

    click.echo(f"Successfully saved to {path}")
