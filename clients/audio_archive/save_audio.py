from pathlib import Path

import click

from clients.audio_archive.utils.arguments import download_options
from clients.audio_archive.utils.request import fetch_trace_and_session_id, try_request
from clients.audio_archive.utils.response import save_file_dir


@click.command(
    "audio",
    help="Fetch audio recording of recognized audio",
)
@download_options()
def save_wav_audio(
    api_address: str,
    client_id: str,
    request_id: str,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{api_address}/clients/{client_id}/requests/{request_id}/audio"

    resp = try_request(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    trace_id, session_id = fetch_trace_and_session_id(api_address, client_id, request_id)

    path = save_file_dir(client_id, request_id, trace_id, session_id, save_dir)
    path.mkdir(parents=True, exist_ok=True)
    path = path / "audio.wav"

    with path.open("wb") as f:
        f.write(resp.content)

    click.echo(f"Successfully saved to {path}")
