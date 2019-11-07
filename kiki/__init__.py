"""
Main functions of the Kiki bot, including the Kiki bot.
"""

import os

from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import NoEntryPointError, ExtensionNotFound
from click import echo


BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
INSTALLED_PLUGINS = [
    'ping', ]


class Kiki(commands.AutoShardedBot):
    """
    The Kiki bot, subclass of AutoShardedClient.
    """

    #pylint: disable=attribute-defined-outside-init
    @staticmethod
    def new(token: str = None, **kwargs):
        """
        Run an instance of the bot.
        """

        kiki = Kiki(command_prefix=".", **kwargs)
        kiki.add_cog(Basics(kiki))

        for plugin in INSTALLED_PLUGINS:
            try:
                kiki.load_extension(f"plugins.{plugin}")
            except (NoEntryPointError, ExtensionNotFound):
                echo(f"Load crashed due to plugin: '{plugin}'")
                return

        try:
            kiki.run(token)
        except LoginFailure:
            echo("Improper token.")


class Basics(commands.Cog):
    """
    Basics cog, containing commands to manage plugins.
    """

    def __init__(self, bot):
        """
        Initialize the basics cog.
        """

        self.bot = bot

    #pylint: disable=unused-argument
    @commands.command(name="reload")
    async def reload(self, ctx, *extensions):
        """
        Reload a given extension, or all.
        """

        if extensions:
            for extension in extensions:
                self.bot.reload_extension(extension)
        else:
            for extension, _ in self.bot.extensions:
                self.bot.reload_extension(extension)
