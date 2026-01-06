#
# Copyright (C) 2025 National Institute of Informatics.
#

"""Token management command-line interface."""

import click

from server.services.token import prepare_issuing_url, refresh_access_token


@click.group()
def token() -> None:
    """Manage OAuth tokens."""


@token.command()
def issue() -> None:
    """Issue access token."""
    url = prepare_issuing_url()
    click.echo(
        "Please access the following URL to authenticate. "
        f"An access token will be issued:\n{url}"
    )


@token.command()
def refresh() -> None:
    """Refresh access token."""
    refresh_access_token()
    click.echo("Access token has been refreshed.")
