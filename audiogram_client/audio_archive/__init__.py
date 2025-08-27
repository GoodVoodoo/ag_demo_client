import click

from audiogram_client.asr.file_recognize import file_recognize
from audiogram_client.asr.recognize import recognize


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
