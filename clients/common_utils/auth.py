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
    sso_url: str,
    realm: str,
    client_id: str,
    client_secret: str,
    iam_account: str,
    iam_workspace: str,
    verify_sso: bool,
) -> list[tuple[str, str]]:
    auth_enabled = client_id and client_secret

    if not auth_enabled:
        click.echo("SSO authorization disabled\n")
        return []

    result_metadata: list[tuple[str, str]] = []

    click.echo("Fetching SSO access token...\n")
    access_token = get_sso_access_token(
        sso_url,
        realm,
        client_id,
        client_secret,
        verify_sso,
    )
    result_metadata.append(("authorization", f"Bearer {access_token}"))

    # Add required headers for v3
    if iam_account:
        result_metadata.append(("x-ai-account", iam_account))
    else:
        result_metadata.append(("x-ai-account", "demo"))
        
    if iam_workspace:
        result_metadata.append(("x-ai-workspace", iam_workspace))
    else:
        result_metadata.append(("x-ai-workspace", "default"))

    return result_metadata
