"""
Levels cogs.
"""

import random
import typing

from datetime import datetime
from discord.ext import commands
from discord import Message
from discord import User as DiscordUser
from discord import Embed


class Levels(commands.Cog):
    """
    Levels Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot

    @commands.command()
    async def rank(self, ctx, user: typing.Optional[DiscordUser]):
        """
        Show the users ranking stats.
        """

        # Choose the appropriate user.
        if not user:
            user = ctx.author

        redis = self.bot.redis
        if not redis:
            await ctx.send("Database connection is down. Use `.info` to view the current status sheet.")
            return

        total = await redis.get(f"xp:{user.id}")

        if not total:
            total = 0

        level = 0
        xp = int(total)
        while True:
            needed = 5 * (level ** 2) + 50 * level + 100
            if xp - needed >= 0:
                xp -= needed
                level += 1
            else:
                break

        # Set up the embed.
        embed = Embed(
            title="Rank",
            type="rich",
            timestamp=datetime.utcnow())
        embed.set_author(
            name=user.name,
            icon_url=user.avatar_url)
        embed.set_footer(text="Report any issues to an admin.")
        embed.add_field(
            name="Current level",
            value=level)
        embed.add_field(
            name="Total XP",
            value=total)

        # Send the embed.
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(
            self,
            message: Message):
        """
        Award the user with experience when they send messages to supported
        channels.
        """

        redis = self.bot.redis
        user = message.author.id

        if redis:
            blocked = await redis.exists(f"cd:{user}")
            if not blocked:
                xp_to_gain = random.randint(5, 15)
                await redis.incrby(
                    f"xp:{user}",
                    xp_to_gain)
                await redis.set(
                    f"cd:{user}",
                    "true",
                    expire=30)
