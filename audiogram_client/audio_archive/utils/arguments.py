import re
from collections.abc import Iterable
from pathlib import Path
from typing import Any, Callable, TypeAlias

import click

OptionCallable: TypeAlias = Callable[..., Any]
OptionsWrapper: TypeAlias = Callable[[OptionCallable], OptionCallable]


def options_wrapper(options: list[OptionsWrapper]) -> OptionsWrapper:
    def wrapper(func: OptionCallable) -> OptionCallable:
        for option in reversed(options):
            func = option(func)

        return func

    return wrapper


def _validate_api_address(_, __, value: str) -> str:
    if not re.match(r"^([\w\-\_]+\.)+([a-z]+)$", value):
        raise click.BadParameter("must be a valid hostname")

    return value


def _validate_url_param(_, __, value: str | None) -> str | None:
    if value is None:
        return value

    if not value:
        raise click.BadParameter("must not be empty")

    if not re.match(r"^[\w\-\_]+$", value):
        raise click.BadParameter(
            "must contain nothing except letters, digits, dashes or underscores"
        )

    return value


def _common_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--api-address",
            type=click.UNPROCESSED,
            callback=_validate_api_address,
            required=True,
            help="Audio archive API host",
            metavar="<URL>",
        ),
        click.option(
            "--client-id",
            type=click.UNPROCESSED,
            callback=_validate_url_param,
            required=True,
            help="Audio archive client ID",
            metavar="<str>",
        ),
    ]

    return options


def list_requests_options() -> OptionsWrapper:
    """Inject list of click options to a list command.

    Options:
        - api_address: str - host[:port] to connect to audio archive
        - client_id: str - Client ID
        - session_id: str | None - Session ID to filter requests
        - trace_id: str | None - Trace ID to filter requests
    """
    options: list[OptionsWrapper] = [
        *_common_options(),
        click.option(
            "--session-id",
            type=click.UNPROCESSED,
            callback=_validate_url_param,
            help="Filter by certain session ID. (Mutually exclusive with --trace-id)",
            metavar="<str>",
        ),
        click.option(
            "--trace-id",
            type=click.UNPROCESSED,
            callback=_validate_url_param,
            help="Filter by certain trace ID. (Mutually exclusive with --session-id)",
            metavar="<str>",
        ),
    ]

    return options_wrapper(options)


def download_options() -> OptionsWrapper:
    """Inject list of click options to a download command.

    Options:
        - api_address: str - host[:port] to connect to audio archive
        - client_id: str - Client ID
        - request_id: str - Request ID to download
        - save_dir: Path | None - root save dir
    """
    options: list[OptionsWrapper] = [
        *_common_options(),
        click.option(
            "--request-id",
            required=True,
            type=click.UNPROCESSED,
            callback=_validate_url_param,
            help="Request ID to fetch data",
            metavar="<str>",
        ),
        click.option(
            "--save-dir",
            type=click.Path(file_okay=False, exists=False, path_type=Path),
            help="Save directory for fetched files",
            metavar="<path>",
        ),
    ]

    return options_wrapper(options)


def common_options(func):
    func = click.option("--host", default="localhost", help="Host of the audio archive server")(func)
    func = click.option("--port", default=8080, help="Port of the audio archive server")(func)
    return func

def request_options(func):
    func = click.option("--request-id", required=True, help="Request ID")(func)
    func = click.option("--audio-id", required=True, help="Audio ID")(func)
    return func

def file_options(func):
    func = click.option("--file-name", default=None, help="File name to save")(func)
    func = click.option("--file-dir", default=".", help="Directory to save file")(func)
    return func
