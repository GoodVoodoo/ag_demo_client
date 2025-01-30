import os
from collections.abc import Iterable
from pathlib import Path
from typing import Protocol, TypedDict

import click
from dynaconf import Dynaconf, Validator

from clients.common_utils.definitions import SETTINGS_TEMPLATE


def _bool_validators(name: str) -> list[Validator]:
    bool_is_str = Validator(name, is_type_of=str)
    bool_is_valid_str = Validator(
        name,
        is_in=["true", "false"],
        messages={
            "operations": '{name} value must be either "true" or "false", ' 'but it is "{value}".'
        },
        when=bool_is_str,
    )
    cast_to_bool = Validator(
        name,
        cast=lambda val: val == "true",  # cast to boolean
        when=bool_is_str,
    )

    return [bool_is_valid_str, cast_to_bool]


def _required_bool_validators(name: str, required_message: str) -> list[Validator]:
    return [
        Validator(
            name,
            must_exist=True,
            messages={"must_exist_true": required_message},
        ),
        *_bool_validators(name),
    ]


def _default_bool_validators(name: str, default: bool) -> list[Validator]:
    return [
        Validator(name, default=default),
        *_bool_validators(name),
    ]


# NB (k.zhovnovatiy): After adding/removing options - review Settings.merge_options below
_VALIDATORS = [
    Validator(
        "API_ADDRESS",
        must_exist=True,
        is_type_of=str,
        len_min=1,
        messages={
            "must_exist_true": (
                "gRPC API address is missing - "
                "specify it using --api-address option "
                'or "api_address" parameter in config file'
            )
        },
    ),
    *_required_bool_validators(
        "USE_SSL",
        (
            "SSL usage option is missing - specify it using --secure <true/false> option "
            'or "use_ssl" parameter in config file'
        ),
    ),
    Validator(
        "CA_CERT_PATH",
        is_type_of=str,
        default="",
        # NB (k.zhovnovatiy): "not path" allows empty default
        condition=lambda path: not path or os.path.isfile(path),
        messages={"condition": "CA_CERT_PATH must point to an existing file."},
    ),
    Validator(
        "CERT_PRIVATE_KEY_PATH",
        is_type_of=str,
        default="",
        # NB (k.zhovnovatiy): "not path" allows empty default
        condition=lambda path: not path or os.path.isfile(path),
        messages={"condition": "CERT_PRIVATE_KEY_PATH must point to an existing file."},
    ),
    Validator(
        "CERT_CHAIN_PATH",
        is_type_of=str,
        default="",
        # NB (k.zhovnovatiy): "not path" allows empty default
        condition=lambda path: not path or os.path.isfile(path),
        messages={"condition": "CERT_CHAIN_PATH must point to an existing file."},
    ),
    Validator(
        "TIMEOUT",
        cast=float,
        gt=0,
        default=60,
        messages={"operations": "Timeout must be > 0, but it is {value}"},
    ),
    Validator(
        "SSO_URL",
        "REALM",
        "CLIENT_ID",
        "CLIENT_SECRET",
        "IAM_WORKSPACE",
        "IAM_ACCOUNT",
        is_type_of=str,
        default="",
    ),
    Validator(
        "CLIENT_ID",
        len_min=1,
        when=Validator("CLIENT_SECRET", len_min=1),
        messages={
            "operations": (
                "Keycloak Client ID is missing - "
                "specify it using --client-id option "
                'or "client_id" parameter in config file'
            )
        },
    ),
    Validator(
        "CLIENT_SECRET",
        len_min=1,
        when=Validator("CLIENT_ID", len_min=1),
        messages={
            "operations": (
                "Keycloak Client Secret is missing - "
                "specify it using --client-secret option or "
                '"client_secret" parameter in config file'
            )
        },
    ),
    Validator(
        "SSO_URL",
        len_min=1,
        when=Validator("CLIENT_ID", len_min=1) | Validator("CLIENT_SECRET", len_min=1),
        messages={
            "operations": (
                "Keycloak URL is missing - "
                "specify it using --sso-url option or "
                '"sso_url" parameter in config file'
            )
        },
    ),
    Validator(
        "REALM",
        len_min=1,
        when=Validator("CLIENT_ID", len_min=1) | Validator("CLIENT_SECRET", len_min=1),
        messages={
            "operations": (
                "Keycloak Realm is missing - "
                "specify it using --realm option or "
                '"realm" parameter in config file'
            )
        },
    ),
    *_default_bool_validators("VERIFY_SSO", True),
]


class CLIOptionsDict(TypedDict):
    api_address: str | None
    use_ssl: bool | None
    ca_cert: str | None
    cert_private_key: str | None
    cert_chain: str | None
    timeout: float | None
    client_id: str | None
    client_secret: str | None
    sso_url: str | None
    realm: str | None
    verify_sso: bool | None
    iam_account: str | None
    iam_workspace: str | None


class SettingsProtocol(Protocol):
    api_address: str
    use_ssl: bool
    ca_cert_path: str
    cert_private_key_path: str
    cert_chain_path: str
    timeout: float

    sso_url: str
    realm: str
    client_id: str
    client_secret: str
    verify_sso: bool

    iam_account: str | None
    iam_workspace: str | None


class Settings(Dynaconf):
    def __init__(self, settings_files: Iterable[str]) -> None:
        super().__init__(
            settings_files=settings_files,
            core_loaders=["INI"],  # NB (k.zhovnovatiy): Remove all loaders except .ini
            loaders=[],  # NB (k.zhovnovatiy): Disable env_loader
            environments=False,
            load_dotenv=False,
            envvar_prefix=False,
        )

        # NB (k.zhovnovatiy): Add validators separately to control when they are applied
        self.validators.register(*_VALIDATORS)

    def merge_options(
        self,
        options: CLIOptionsDict,
    ) -> None:
        """Merge values from CLI arguments into config."""
        # NB (k.zhovnovatiy): keys in options and keys in config are not the same,
        # so options dict can't be used as-is
        merge_dict = {
            "api_address": options["api_address"],
            "use_ssl": options["use_ssl"],
            "ca_cert_path": options["ca_cert"],
            "cert_private_key_path": options["cert_private_key"],
            "cert_chain_path": options["cert_chain"],
            "timeout": options["timeout"],
            "client_id": options["client_id"],
            "client_secret": options["client_secret"],
            "sso_url": options["sso_url"],
            "realm": options["realm"],
            "verify_sso": options["verify_sso"],
            "iam_account": options["iam_account"],
            "iam_workspace": options["iam_workspace"],
        }

        for key, value in merge_dict.items():
            if value is None:
                continue
            self.set(key, value)


@click.command(
    no_args_is_help=True,
    short_help="Generate config file",
    help="Generate config at specified FILE_PATH (eg. ~/config.ini)",
)
@click.argument(
    "file_path",
    type=click.Path(),
)
def create_config(file_path: str) -> None:
    path_obj = Path(file_path)

    if path_obj.is_dir():
        ctx = click.get_current_context()
        ctx.fail("Provided path is a directory! Provide path for a file.")

    if path_obj.is_file():
        replace = click.prompt(
            "File at provided path already exists, replace? [y/n]",
            type=bool,
        )
        if not replace:
            return

    path_obj.parent.mkdir(parents=True, exist_ok=True)

    settings_bytes = SETTINGS_TEMPLATE.read_bytes()
    path_obj.write_bytes(settings_bytes)

    click.echo(f"Generated config in {file_path}")
