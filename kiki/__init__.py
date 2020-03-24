"""
Main functions of the Kiki bot, including the Kiki bot.
"""

from discord.ext import commands
from discord.errors import LoginFailure
from discord.ext.commands.errors import CommandNotFound
from click import echo
from sqlalchemy import create_engine

from kiki.utils.db import database, metadata


class Kiki(commands.Bot):
    """
    The Kiki bot.
    """

    @staticmethod
    def new(token: str = None, **kwargs):
        """
        Run an instance of the bot.
        """

        # Initialize the bot.
        kiki = Kiki(command_prefix=".", **kwargs)

        # Load extensions.
        kiki.load_extension("kiki.plugins.info")
        kiki.load_extension("kiki.plugins.automod")
        kiki.load_extension("kiki.plugins.levels")

        # Initialize the database after all plugin
        # models have been registered.
        engine = create_engine(str(database.url))
        metadata.create_all(engine)

        # Run the bot.
        try:
            kiki.run(token)
        except LoginFailure:
            echo("Improper token.")

    async def on_ready(self):
        """
        This event is called when the bot is fully ready.
        """

        # Establish a database connection.
        try:
            await database.connect()
        except AssertionError:
            echo("Database already connected. Skipping.")
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
