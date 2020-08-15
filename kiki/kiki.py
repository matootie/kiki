"""The Kiki bot class

Kiki bot is a subclass of Discord.py command-bot. This is where some
additional custom functionality is initialized, and customizations are
made before runtime.

  Typical usage example: |

    kiki = Kiki()
    kiki.run("discord-bot-token")

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
- https://aioredis.readthedocs.io/en/v1.3.0/api_reference.html#aioredis.create_redis_pool
"""

import asyncio
import socket
import aioredis
import functools
from click import echo
from discord.ext.commands import Bot
from discord.ext.commands import Context
from discord.ext.commands import errors


class Kiki(Bot):
    """The Kiki bot

    Subclass of Discord.py command-bot, housing some custom functionality.
    """

    def __init__(self, config: dict = {}):
        """Initialize the custom bot

        Class initializer, simply sets some default attributes and loads the
        default set of plugins.

        Args:
          command_prefix: The desired command prefix for the bot.
          kwargs: Any optional attributes to set.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#bot
        """

        # Set global attributes
        self.config = config
        self.version = config.get("version", "v0.0.0-demo")

        # Run superclass initialization
        command_prefix = config.get("prefix", ".")
        super().__init__(command_prefix=command_prefix)

        # Load all plugins

    async def on_ready(self):
        """Discord Bot on ready

        This event is called when the bot is fully ready.

        References:
        - https://discordpy.readthedocs.io/en/latest/api.html#discord.on_ready
        """

        # Announce version number.
        echo(f"Running Kiki bot {self.version}")
        echo(f"Connected application {self.app}")

        # Write to readiness file.
        # This lets Kubernetes know the deployment has successfully started.
        with open("/tmp/healthy", "w") as file:
            file.write("Healthy")

    async def on_command_error(self, context: Context, exception: Exception):
        """Discord bot on command error

        This event is called when a command raises an error.

        Args:
          context: The Discord context object from when the error happened.
          exception: The exception that was raised.

        Raises: |
          The original exception, if it can not be dealt with silently.

        References:
        - https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#discord.ext.commands.Bot.on_command_error
        """  # noqa

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
