"""The Kiki bot class.

Kiki bot is a subclass of Discord.py command-bot. This is where some
additional custom functionality is initialized, and customizations are
made before runtime.

    Typical usage example:

    kiki = Kiki()
    kiki.run("discord-bot-token")

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
- https://aioredis.readthedocs.io/en/v1.3.0/api_reference.html#aioredis.create_redis_pool
- http://pyenchant.github.io/pyenchant/#introduction
"""

from socket import gaierror
from aioredis import create_redis_pool
from enchant import Dict
from click import echo
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands.errors import CheckFailure


class Kiki(Bot):
    """The Kiki bot.

    Subclass of Discord.py command-bot. Houses some custom functionality
    including a language dictionary and a connection to Redis for data storage.

    Attributes:
        redis: A connection to Redis, or None if no connection exists.
        dictionary: An enchant language dictionary set to English.
        version: The current running version of the bot.
    """

    def __init__(self, command_prefix: str = ".", **kwargs):
        """Initialize the custom bot.

        Class initializer, simply sets some default attributes and loads the
        default set of plugins.

        Args:
            command_prefix: The desired command prefix for the bot.
            kwargs: Any optional attributes to set.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
        """

        # Initialize attributes.
        self._redis_url = kwargs.get("redis_url")
        self.redis = None
        self.dictionary = Dict("en")
        self.version = kwargs.get("version")

        # Run superclass initialization.
        super().__init__(command_prefix=command_prefix, **kwargs)

        # Load all plugins.
        self.load_extension("kiki.plugins.info")
        self.load_extension("kiki.plugins.automod")
        self.load_extension("kiki.plugins.levels")

    async def on_ready(self):
        """Discord Bot on ready.

        This event is called when the bot is fully ready.

        References:
        - https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
        """

        # Announce version number.
        echo(f"Running Kiki bot {self.version}")

        # Set a cleaner name for the URL.
        url = self._redis_url

        # Attempt to connect to Redis.
        if url:
            try:
                self.redis = await create_redis_pool(url, encoding="utf-8")
                echo(f"Successfully connected to Redis: {url}")
            except gaierror:
                echo(f"Unable to connect to Redis: {url}")
                self.redis = None

        # Announce readiness.
        echo("Ready.")

    async def on_command_error(self, context: Context, exception: Exception):
        """Discord bot on command error.

        This event is called when a command raises an error.

        Args:
            context: The Discord context object from when the error happened.
            exception: The exception that was raised.

        Raises:
            The original exception, if it can not be dealt with silently.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.on_command_error
        """

        # If the problem is that the command cannot be found, let the user know.
        if isinstance(exception, CommandNotFound):
            await context.send("Unknown command.")
            return

        # If a command prerequisite check has failed, let the user know.
        if isinstance(exception, CheckFailure):
            await context.send("Prerequisite checks for this command have failed. See `.info` for more insight.")
            return

        # Otherwise, raise the exception.
        raise exception
