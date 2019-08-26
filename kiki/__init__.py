"""
Main functions of the Kiki bot, including the Kiki bot.
"""

from discord.ext import commands
from discord.errors import LoginFailure
from click import echo


class Kiki(commands.AutoShardedBot):
    """
    The Kiki bot, subclass of AutoShardedClient.
    """

    @staticmethod
    def new(token: str = None, prefix: str = None, **kwargs):
        """
        Run an instance of the bot.
        """

        if not prefix:
            prefix = "."
        kiki = Kiki(command_prefix=prefix, **kwargs)
        kiki.add_cog(Basics(kiki))
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
