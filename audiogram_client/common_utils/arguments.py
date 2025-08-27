import functools
from collections.abc import Iterable
from pathlib import Path
from typing import Callable, cast, ParamSpec, TypeAlias, TypeVar

import click

from audiogram_client.common_utils.config import CLIOptionsDict, Settings

P = ParamSpec("P")
T = TypeVar("T")

OptionCallable: TypeAlias = Callable[P, T]
OptionsWrapper: TypeAlias = Callable[[OptionCallable], OptionCallable]

# NB (k.zhovnovatiy): Common options which should be merged in Settings object
_common_settings_options = [
    "api_address",
    "use_ssl",
    "ca_cert",
    "cert_private_key",
    "cert_chain",
    "timeout",
    "client_id",
    "client_secret",
    "sso_url",
    "realm",
    "verify_sso",
    "iam_account",
    "iam_workspace",
]


def options_wrapper(options: list) -> OptionsWrapper:
    def wrapper(func: OptionCallable) -> OptionCallable:
        for option in reversed(options):
            func = option(func)

        return func

    return wrapper


def _keycloak_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--sso-url",
            help="Keycloak server URL",
            metavar="<url>",
        ),
        click.option(
            "--realm",
            help="Keycloak realm ID",
            metavar="<realm id>",
        ),
        click.option(
            "--client-id",
            "client_id",
            help="Keycloak client ID",
            metavar="<client_id>",
        ),
        click.option(
            "--client-secret",
            "client_secret",
            help="Keycloak client secret",
            metavar="<client_secret>",
        ),
        click.option(
            "--verify-sso",
            type=bool,
            default=None,
            help="enable CA certificate validation for Keycloak connection",
        ),
    ]

    return options


def _iam_options() -> Iterable[OptionCallable]:
    options = [
        click.option(
            "--iam-account",
            "iam_account",
            help="IAM account to verify access",
            metavar="<account_name>",
        ),
        click.option(
            "--iam-workspace",
            "iam_workspace",
            help="IAM workspace (omit for default workspace)",
            metavar="<workspace_name>",
        ),
    ]

    return options


def common_options() -> OptionsWrapper:
    """Inject common list of click options to a command.

    Options:
        - config_path: str | None - Path to the .ini config file
        - api_address: str - API address:port
        - use_ssl: bool | None - use ssl or not
        - ca_cert: str - path to certificate file
        - timeout: float - timeout in seconds
        - client_id: str - Keycloak client ID
        - client_secret: str - Keycloak client secret
        - sso_url: str - Keycloak server URL
        - realm: str - Keycloak realm ID
        - verify_sso: bool | None - enable/disable certificate verification for keycloak
    """
    # NB (k.zhovnovatiy): When modifying options below - verify that those options' keys
    # exist in _common_settings_options and CLIOptionsDict
    options: list = [
        click.option(
            "--config",
            "config_path",
            type=click.Path(exists=True, dir_okay=False),
            help="path to the .ini config file",
            metavar="<path>",
        ),
        click.option(
            "--api-address",
            help="network address and port (optional) of gRPC API service",
            metavar="<host:port>",
        ),
        click.option(
            "--secure",
            "use_ssl",
            type=bool,
            default=None,
            help="enable/disable SSL for gRPC connection",
        ),
        click.option(
            "--ca-cert",
            type=click.Path(exists=True, dir_okay=False),
            help="path to a file holding the PEM-encoded root certificates for gRPC connection",
            metavar="<file path>",
        ),
        click.option(
            "--cert-private-key",
            type=click.Path(exists=True, dir_okay=False),
            help="path to a file holding the PEM-encoded private key for gRPC connection",
            metavar="<file path>",
        ),
        click.option(
            "--cert-chain",
            type=click.Path(exists=True, dir_okay=False),
            help="path to a file holding PEM-encoded certificate chain for gRPC connection",
            metavar="<file path>",
        ),
        click.option(
            "--timeout",
            type=float,
            help="time in seconds to wait for gRPC response",
            metavar="<float>",
        ),
        *_keycloak_options(),
        *_iam_options(),
    ]

    return options_wrapper(options)


def common_options_in_settings(func: Callable[P, T]) -> Callable[P, T]:
    """Read and inject settings to a command. Override settings from CLI options.

    Read Settings and apply overrides from CLI options, defined in
    common_options(). Inject only settings object to a command.
    """

    @functools.wraps(func)
    def wrapper(*args: P.args, **options) -> T:
        config_path_str = cast(str | None, options.pop("config_path"))
        config_path = Path(config_path_str or "")  # Prevent failing on None value

        # If no config path specified, look for config.ini in current directory
        if not config_path_str:
            default_config = Path("config.ini")
            if default_config.is_file():
                config_path_str = str(default_config)
                config_path = default_config
                click.echo(f'Loading .ini configuration from "{config_path.name}"\n')

        if config_path_str and config_path.is_file():
            if not config_path_str.startswith("config.ini"):
                click.echo(f'Loading .ini configuration from "{config_path.name}"\n')
            settings = Settings([config_path_str])
        else:
            settings = Settings([])

        settings.merge_options(cast(CLIOptionsDict, options))
        settings.validators.validate()

        for key in _common_settings_options:
            options.pop(key)

        return func(*args, settings=settings, **options)

    common_option_wrapper = common_options()
    wrapped_func = common_option_wrapper(wrapper)

    return wrapped_func
