"""
Kiki CLI tools.
"""

import os
import click

from kiki import Kiki


@click.group()
def cli():
    """
    Main CLI command group for Kiki bot.
    """

    pass


@cli.command()
@click.option("-V", "--version", "version")
def run(version: str = "v0.1.0-alpha"):
    """
    Run the bot.
    """

    try:
        token = os.environ["KIKI_TOKEN"]
    except KeyError:
        click.error_message("You must specify the bot token under KIKI_TOKEN.")

    redis_url = os.environ.get("REDIS_URL")

    kiki = Kiki(redis_url=redis_url, version=version)
    kiki.run(token)
