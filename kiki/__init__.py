"""
Main functions of the Kiki bot, including the Kiki bot.
"""

import os

from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import NoEntryPointError, ExtensionNotFound
from click import echo


class Kiki(commands.AutoShardedBot):
    """
    The Kiki bot, subclass of AutoShardedClient.
    """

    @staticmethod
    def new(token: str = None, **kwargs):
        """
        Run an instance of the bot.
        """

        # Initialize the bot.
        kiki = Kiki(command_prefix=".", **kwargs)

        # Load extensions.
        kiki.load_extension('kiki.plugins.ping')
        kiki.load_extension('kiki.plugins.automod')

        # Run the bot.
        try:
            kiki.run(token)
        except LoginFailure:
            echo("Improper token.")
