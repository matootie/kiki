"""Kiki CLI tools.

Initialization of the Click command line tool, as well as some basic level
commands. There is no typical usage here as the runner script is the only that
requires access to this code.

References:
- https://click.palletsprojects.com/en/7.x/
"""

import os
import click

from kiki import Kiki


@click.group()
def cli():
    """Main CLI command group for Kiki bot.

    Simple grouping for all available command-line commands.
    """

    pass


@cli.command()
@click.option("-V", "--version", "version")
def run(version: str = "v0.1.0-alpha"):
    """Run the bot.

    Requires a Discord bot token to be specified in environment as KIKI_TOKEN.
    """

    # Attempt to load the token from environment.
    try:
        token = os.environ["KIKI_TOKEN"]
    except KeyError:
        click.error_message("You must specify the bot token under KIKI_TOKEN.")

    # Load the optional Redis URL from environment.
    redis_url = os.environ.get("REDIS_URL")

    # Create and run Kiki.
    kiki = Kiki(redis_url=redis_url, version=version)
    kiki.run(token)
