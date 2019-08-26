"""
Kiki cli tools.
"""

import click

from kiki import Kiki


@click.group()
def cli():
    """
    Main CLI command group for Kiki bot.
    """


@cli.command()
@click.option("-t", "--token", required=True, help="Discord bot secret token.")
@click.option("-p", "--prefix", help="Command prefix for the bot.")
def run(token, prefix):
    """
    Run the bot.
    """

    Kiki.new(token=token, prefix=prefix)
