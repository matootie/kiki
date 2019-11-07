"""
Kiki cli tools.
"""

import os
import click

from kiki import Kiki


@click.group()
def cli():
    """
    Main CLI command group for Kiki bot.
    """


@cli.command()
def run():
    """
    Run the bot.
    """

    Kiki.new(token=os.environ.get("KIKI_TOKEN"))
