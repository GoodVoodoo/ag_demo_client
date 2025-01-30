from typing import cast

import click
from keycloak import KeycloakOpenID


def get_sso_access_token(
    sso_server_url: str,
    realm_name: str,
    client_id: str,
    client_secret: str,
    verify: bool = True,
) -> str:
    sso_connection = KeycloakOpenID(
        sso_server_url,
        realm_name,
        client_id,
        client_secret,
        verify=verify,
    )
    token_info = sso_connection.token(grant_type="client_credentials")
    return cast(str, token_info["access_token"])


def get_auth_metadata(
    sso_server_url: str,
    realm_name: str,
    client_id: str,
    client_secret: str,
    iam_account: str | None,
    iam_workspace: str | None,
    verify: bool = True,
) -> tuple[tuple[str, str], ...]:
    auth_enabled = client_id and client_secret

    if not auth_enabled:
        click.echo("SSO authorization disabled\n")
        return ()

    result_metadata: list[tuple[str, str]] = []

    click.echo("Fetching SSO access token...\n")
    access_token = get_sso_access_token(
        sso_server_url,
        realm_name,
        client_id,
        client_secret,
        verify,
    )
    result_metadata.append(("authorization", f"Bearer {access_token}"))

    if iam_account:
        result_metadata.append(("x-ai-account", iam_account))

    if iam_workspace:
        result_metadata.append(("x-ai-workspace", iam_workspace))

    return tuple(result_metadata)
