import click

def common_voice_cloning_options(f):
    f = click.option(
        '--audio-file',
        required=True,
        help='Path to audio file for voice cloning',
        type=click.Path(exists=True),
    )(f)
    return f

def task_id_option(f):
    f = click.option(
        '--task-id',
        required=True,
        help='The ID of the voice cloning task',
    )(f)
    return f

def voice_id_option(f):
    f = click.option(
        '--voice-id',
        required=True,
        help='The ID of the voice to delete',
    )(f)
    return f
