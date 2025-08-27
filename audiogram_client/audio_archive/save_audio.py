import click
from audiogram_client.audio_archive.utils.arguments import (
    common_options,
    file_options,
    request_options,
)
from audiogram_client.audio_archive.utils.request import get_and_save_data


@click.command(name="audio", help="Save audio to file")
@common_options
@request_options
@file_options
def save_wav_audio(
    host: str,
    port: int,
    request_id: str,
    audio_id: str,
    file_name: str,
    file_dir: str,
) -> None:
    get_and_save_data(host, port, request_id, audio_id, "audio", file_name, file_dir)
