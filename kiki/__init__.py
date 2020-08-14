"""The Kiki bot class.

Kiki bot is a subclass of Discord.py command-bot. This is where some
additional custom functionality is initialized, and customizations are
made before runtime.

  Typical usage example: |

    kiki = Kiki()
    kiki.run("discord-bot-token")

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
- https://aioredis.readthedocs.io/en/v1.3.0/api_reference.html#aioredis.create_redis_pool
- http://pyenchant.github.io/pyenchant/#introduction
"""

import os
import asyncio
import socket
import typing
import aioredis
from click import echo
from discord import Guild, Emoji
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import errors

from kiki import utils


class Kiki(Bot):
    """The Kiki bot.

    Subclass of Discord.py command-bot, housing some custom functionality.
    """

    def __init__(self):
        """Initialize the custom bot.

        Class initializer, simply sets some default attributes and loads the
        default set of plugins.

        Args:
          command_prefix: The desired command prefix for the bot.
          kwargs: Any optional attributes to set.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
        """

        # Load configuration file
        config = utils.load_config()
        self.config = config

        # Set global attributes
        self.version = config.get("version", "v0.0.0-demo")

        # Connect to database
        redis_config = config.get("redis")
        if redis_config:
            redis_url = redis_config.get("url")
            self.redis = None
            if redis_url:
                try:
                    loop = asyncio.get_event_loop()
                    self.redis = loop.run_until_complete(
                        aioredis.create_redis_pool(redis_url, encoding="utf-8"))
                except (socket.gaierror, OSError):
                    pass

        # Run superclass initialization
        command_prefix = config.get("prefix", ".")
        super().__init__(command_prefix=command_prefix)

        # Load all plugins
        #self.load_extension("kiki.plugins.info")
        #self.load_extension("kiki.plugins.automod")
        #self.load_extension("kiki.plugins.levels")

    async def on_ready(self):
        """Discord Bot on ready.

        This event is called when the bot is fully ready.

        References:
        - https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
        """

        # Announce version number.
        echo(f"Running Kiki bot {self.version}")

    async def on_command_error(self, context: Context, exception: Exception):
        """Discord bot on command error.

        This event is called when a command raises an error.

        Args:
          context: The Discord context object from when the error happened.
          exception: The exception that was raised.

        Raises: |
          The original exception, if it can not be dealt with silently.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.on_command_error
        """

        # When an appropriate command can not be found.
        if isinstance(exception, errors.CommandNotFound):
            await context.send("Unknown command.")
            return

        # When a prerequisite check for a command has failed.
        if isinstance(exception, errors.CheckFailure):
            await context.send("Failed to run the requested command.")
            return

        # Otherwise, raise the exception.
        raise exception
