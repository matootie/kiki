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
"""  # noqa

import aioredis
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import when_mentioned
from discord.ext.commands import command
from discord.ext.commands.errors import CommandNotFound
from discord.ext.commands.errors import CheckFailure

__version__ = None


class Kiki(Bot):
    """The Kiki bot.

    Subclass of Discord.py command-bot. Houses some custom functionality
    including a language dictionary and a connection to Redis for data storage.

    Attributes:
        redis: A connection to Redis, or None if no connection exists.
    """
    def __init__(self, **kwargs):
        """Initialize the custom bot.

        Class initializer, simply sets some default attributes and loads the
        default set of modules.

        Args:
            command_prefix: The desired command prefix for the bot.
            kwargs: Any optional attributes to set.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
        """

        # Initialize attributes.
        redis_url = kwargs.get("redis_url")
        if redis_url:
            try:
                self.redis = aioredis.from_url(redis_url,
                                               encoding="utf-8",
                                               decode_responses=True)
            except:
                self.redis = None
        else:
            self.redis = None
        self.version = __version__ or "UNOFFICIAL VERSION"

        # Run superclass initialization.
        super().__init__(command_prefix=when_mentioned,
                         help_command=None,
                         **kwargs)

        # Load all modules.
        self.load_extension("kiki.modules.admin")
        self.load_extension("kiki.modules.info")
        self.load_extension("kiki.modules.levels")

    @property
    def guild(self):
        server = self.get_guild(604373743837511691)
        return server

    @property
    def util_guild(self):
        server = self.get_guild(742115522950201355)
        return server

    async def on_ready(self):
        """Discord Bot on ready.

        This event is called when the bot is fully ready.

        References:
        - https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
        """

        # Announce version number.
        print(f"Running Kiki bot {self.version}")

        # Announce readiness.
        print("Ready.")

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
        """  # noqa

        # Pass if the command was simply not found.
        if isinstance(exception, CommandNotFound):
            return

        # Otherwise, raise the exception.
        raise exception
