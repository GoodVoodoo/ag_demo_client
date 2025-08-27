import click


def audio_file_option(required: bool = True) -> click.option:
    """Add `--audio-file` option to a command."""
    return click.option(
        "--audio-file",
        "audio_file",
        required=required,
        type=click.Path(exists=True, dir_okay=False, resolve_path=True),
        help="path to an audio file",
        metavar="<path>",
    )


def output_file_option(default_filename: str = "output.wav") -> click.option:
    """Add `--save-to` option to a command."""
    return click.option(
        "--save-to",
        "output_file",
        type=click.Path(file_okay=True, dir_okay=False, writable=True, resolve_path=True),
        default=default_filename,
        help="path to an output file",
        metavar="<path>",
        show_default=True,
    )


def text_option(required: bool = True) -> click.option:
    """Add `--text` option to a command."""
    return click.option(
        "--text",
        required=required,
        help="text for synthesis",
        metavar="<string>",
    )
