"""
Main functions of the Kiki bot, including the Kiki bot.
"""

from socket import gaierror
from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import CommandNotFound
from aioredis import create_redis_pool
from click import echo


class Kiki(commands.Bot):
    """
    The Kiki bot.
    """

    def __init__(self, command_prefix: str = ".", **kwargs):
        """
        Initialize the custom bot.
        """

        self.redis_host = kwargs.get("redis_host")
        self.redis = None

        super().__init__(command_prefix=command_prefix, **kwargs)

        self.load_extension("kiki.plugins.info")
        self.load_extension("kiki.plugins.automod")
        self.load_extension("kiki.plugins.levels")

    async def on_ready(self):
        """
        This event is called when the bot is fully ready.
        """

        if self.redis_host:
            try:
                self.redis = await create_redis_pool(
                    self.redis_host,
                    encoding="utf-8")
            except gaierror:
                self.redis = None
        echo("Ready.")

    async def on_command_error(self, context, exception):
        """
        This event is called when a user enters a command incorrectly.
        """

        # If the problem is that the command cannot be found,
        # let the user know.
        if isinstance(exception, CommandNotFound):
            await context.send("Unknown command.")
            return
        # Raise the exception.
        raise exception
