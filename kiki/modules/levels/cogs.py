"""Levels cogs.

Essential functionality for the levels module to run. This module contains the
main functionality of the module. There is no typical usage here as the
top-level info module is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

import pytz
from datetime import datetime
from aioredis import Redis
from discord.ext import commands
from discord.message import Message


class Levels(commands.Cog):
    """Levels Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the levels module.
    """

    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """
        """

        redis: Redis = self.bot.redis
        author = message.author

        # Ignore if no Redis connection.
        if not bool(redis):
            return

        # Ignore bots.
        if author.bot:
            return

        # Ignore messages not sent in lounge.
        if message.channel.id != 793970769842536458:
            return

        # Get the time in UTC.
        now_utc = pytz.utc.localize(datetime.now())
        # Convert UTC time to Toronto time.
        now_local = now_utc.astimezone(pytz.timezone("America/Toronto"))
        # Stringify the date.
        today = now_local.date().isoformat()

        await redis.zincrby(f"messages:{today}", 1, author.id)
        await redis.zincrby("messages:all", 1, author.id)
        await redis.zincrby(f"messages:{author.id}", 1, today)
