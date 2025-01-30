import contextlib
from collections.abc import Iterator
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Self

import click
import grpc

from clients.common_utils.config import SettingsProtocol


@dataclass
class SSLCreds:
    """SSL certificates used for authentication in gRPC.

    Values:
    - private_key and certificate_chain used for client identification.
    - root_certificates aka CA used to verify server's certificate.
    """

    root_certificates: bytes | None = None
    private_key: bytes | None = None
    certificate_chain: bytes | None = None

    @classmethod
    def load(
        cls,
        root_certificates_path: str | None,
        private_key_path: str | None,
        certificate_chain_path: str | None,
    ) -> Self:
        """Load SSL certificates to be used in gRPC authentication.

        (!) All certificates should be passed in PEM format. Pay attention that
        private keys could contain data in PEM format even if
        key file ends with .key suffix.
        """
        rv = cls()

        if root_certificates_path:
            rv.root_certificates = Path(root_certificates_path).read_bytes()

        if private_key_path:
            rv.private_key = Path(private_key_path).read_bytes()

        if certificate_chain_path:
            rv.certificate_chain = Path(certificate_chain_path).read_bytes()

        return rv


def ssl_creds_from_settings(settings: SettingsProtocol) -> SSLCreds | None:
    if not settings.use_ssl:
        return None

    return SSLCreds.load(
        settings.ca_cert_path,
        settings.cert_private_key_path,
        settings.cert_chain_path,
    )


@contextlib.contextmanager
def open_grpc_channel(address: str, ssl_creds: SSLCreds | None) -> Iterator[grpc.Channel]:
    """Open either secure or insecure connection to gRPC API."""
    if ssl_creds:
        creds = grpc.ssl_channel_credentials(
            root_certificates=ssl_creds.root_certificates,
            private_key=ssl_creds.private_key,
            certificate_chain=ssl_creds.certificate_chain,
        )

        channel_ctx = grpc.secure_channel(address, creds)
    else:
        channel_ctx = grpc.insecure_channel(address)

    with channel_ctx as channel:
        yield channel


def print_metadata(metadata: Iterable[tuple[str, str | bytes]]) -> None:
    for key, value in metadata:
        click.echo(f"{key}: {value!r}")
