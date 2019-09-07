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

    #pylint: disable=attribute-defined-outside-init
    @staticmethod
    def new(
            token: str = None,
            prefix: str = None,
            plugin_directory: str = None,
            **kwargs):
        """
        Run an instance of the bot.
        """

        if not prefix:
            prefix = "."
        kiki = Kiki(
            command_prefix=prefix,
            **kwargs)
        kiki.add_cog(Basics(kiki))
        kiki.plugin_directory = plugin_directory

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

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Load extensions on startup.
        """

        for plugin in os.listdir(self.bot.plugin_directory):
            try:
                self.bot.load_extension(plugin)
            except (NoEntryPointError, ExtensionNotFound):
                echo(f"\"{plugin}\" is not a valid plugin.")

    @commands.command(name="install")
    async def install(self, ctx, *extensions):
        """
        Install any given extensions.
        """

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
