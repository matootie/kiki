"""
Main functions of the Kiki bot, including the Kiki bot.
"""

import os

from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import NoEntryPointError, ExtensionNotFound
from discord.ext.commands.errors import ExtensionNotFound
from discord.ext.commands.errors import CommandNotFound
from discord.utils import find
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
        kiki.load_extension('kiki.plugins.info')
        kiki.load_extension('kiki.plugins.automod')
        kiki.load_extension('kiki.plugins.levels')

        # Run the bot.
        try:
            kiki.run(token)
        except LoginFailure:
            echo("Improper token.")

    async def on_command_error(self, context, exception):
        if isinstance(exception, CommandNotFound):
            await context.send("Unknown command.")
            return
        raise exception

    def log(self, message):
        """
        Log messages for admins to see.
        """

        print(message)
