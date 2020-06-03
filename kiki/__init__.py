"""
Main functions of the Kiki bot, including the Kiki bot.
"""

from socket import gaierror
from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands.errors import CheckFailure
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

        self._redis_url = kwargs.get("redis_url")
        self.redis = None
        
        self.version = kwargs.get("version")

        super().__init__(command_prefix=command_prefix, **kwargs)

        self.load_extension("kiki.plugins.info")
        self.load_extension("kiki.plugins.automod")
        self.load_extension("kiki.plugins.levels")

    async def on_ready(self):
        """
        This event is called when the bot is fully ready.
        """

        url = self._redis_url

        if url:
            try:
                self.redis = await create_redis_pool(url, encoding="utf-8")
            except gaierror:
                echo(f"Unable to connect to Redis: {url}")
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

        if isinstance(exception, CheckFailure):
            await context.send("Prerequisite checks for this command have failed.")
            return

        # Raise the exception.
        raise exception
