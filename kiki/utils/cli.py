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
def run():
    """
    Run the bot.
    """

    try:
        token = os.environ["KIKI_TOKEN"]
    except KeyError:
        click.error_message("You must specify the bot token under KIKI_TOKEN.")

    redis_url = os.environ.get("REDIS_URL")

    kiki = Kiki(redis_url=redis_url)
    kiki.run(token)
