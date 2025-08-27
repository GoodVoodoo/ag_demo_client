import sys

from audiogram_client.audio_archive.get_requests import get_requests
from audiogram_client.audio_archive.save_audio import save_wav_audio
from audiogram_client.audio_archive.save_transcript import save_transcript
from audiogram_client.audio_archive.save_vad_marks import save_vad_marks

import click


@click.group(name='archive', help='Audio archive commands')
def audio_archive():
    pass

@click.group("download", help='Download data from archive')
def download():
    pass


download.add_command(save_transcript)
download.add_command(save_vad_marks)
download.add_command(save_wav_audio)

audio_archive.add_command(get_requests)
audio_archive.add_command(download)
