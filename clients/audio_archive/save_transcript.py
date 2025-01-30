from pathlib import Path

import click
import pydantic

from clients.audio_archive.utils.arguments import download_options
from clients.audio_archive.utils.models import TranscriptList
from clients.audio_archive.utils.request import fetch_trace_and_session_id, try_request
from clients.audio_archive.utils.response import save_file_dir


@click.command(
    "transcript",
    help="Fetch transcript of a request by its ID",
)
@download_options()
def save_transcript(
    api_address: str,
    client_id: str,
    request_id: str,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{api_address}/clients/{client_id}/requests/{request_id}/transcript"

    resp = try_request(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    resp_json = resp.json()

    try:
        transcript_list = TranscriptList(**resp_json)
    except pydantic.ValidationError as e:
        click.echo("Errors happened during validation of response JSON:")
        click.echo(e.errors())
        return

    trace_id, session_id = fetch_trace_and_session_id(api_address, client_id, request_id)

    path = save_file_dir(client_id, request_id, trace_id, session_id, save_dir)
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
