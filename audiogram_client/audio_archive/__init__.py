import click

from audiogram_client.audio_archive.save_audio import save_wav_audio
from audiogram_client.audio_archive.save_transcript import save_transcript
from audiogram_client.audio_archive.save_vad_marks import save_vad_marks
from audiogram_client.audio_archive.get_requests import get_requests


@click.group()
def main() -> None:
    pass


@click.group("download")
def download() -> None:
    pass


download.add_command(save_transcript)
download.add_command(save_vad_marks)
download.add_command(save_wav_audio)


main.add_command(get_requests)
main.add_command(download)
