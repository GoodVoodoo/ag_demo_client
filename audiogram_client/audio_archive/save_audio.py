from pathlib import Path

import click

from audiogram_client.audio_archive.utils.request import get_audio
from audiogram_client.common_utils.arguments import common_options_in_settings
from audiogram_client.common_utils.config import SettingsProtocol
from audiogram_client.common_utils.errors import errors_handler


@click.command(
    "save-audio",
    help="Fetch audio recording of recognized audio",
)
@common_options_in_settings()
def save_wav_audio(
    settings: SettingsProtocol,
    save_dir: Path | None,
) -> None:
    context = click.get_current_context()

    url = f"https://{settings.api_address}/clients/{settings.client_id}/requests/{settings.request_id}/audio"

    resp = get_audio(url)

    if resp.status_code == 404:
        click.echo("Such request for specified client ID was not found")
        context.exit(-1)

    resp.raise_for_status()

    trace_id, session_id = errors_handler.fetch_trace_and_session_id(
        settings.api_address, settings.client_id, settings.request_id
    )

    path = errors_handler.save_file_dir(
        settings.client_id, settings.request_id, trace_id, session_id, save_dir
    )
    path.mkdir(parents=True, exist_ok=True)
    path = path / "audio.wav"

    with path.open("wb") as f:
        f.write(resp.content)

    click.echo(f"Successfully saved to {path}")
