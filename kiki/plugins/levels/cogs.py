"""
Levels cogs.
"""

import random
import typing

from datetime import datetime, timedelta
from discord.ext import commands
from discord import Message
from discord import User
from discord import Member
from discord import TextChannel
from discord import Embed

from kiki.utils import is_admin
from kiki.utils.db import get_db


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
    @is_admin()
    async def blacklist(
            self,
            ctx,
            channels: commands.Greedy[TextChannel]):
        """
        Blacklist a specific channel.
        """

        db = get_db()
        if not db:
            self.bot.log(
                "Failed to establish connection to database. Levels plugin malfunctioning.")
            await ctx.send("Unable to process request at this time. Please notify an admin.")
            return

        values = [c.id for c in channels]
        db.lpush("levels:blacklist:channels", *values)

        await ctx.send(f"Successfully added {len(values)} channels to blacklist.")

    @property
    def blacklisted_channels(self):
        """
        Retrieve a list of blacklisted channel IDs.
        """

        db = get_db()
        if not db:
            return []

        channel_ids = db.lrange("levels:blacklist:channels", 0, -1)
        if not channel_ids:
            return []

        return [int(x) for x in channel_ids]

    def get_level(self, xp: int) -> int:
        """
        Calculate the users current level.
        """

        level = 0
        while True:
            needed = 5 * (level ** 2) + 50 * level + 100
            if xp - needed >= 0:
                xp -= needed
                level += 1
            else:
                break

        needed = 5 * (level ** 2) + 50 * level + 100
        to_next = needed - xp

        return level, to_next

    @commands.command()
    async def rank(self, ctx, user: typing.Optional[User]):
        """

        """

        if not user:
            user = ctx.author

        db = get_db()
        if not db:
            await ctx.send("Unable to proccess your request at this time.")
            self.bot.log(
                "Failed to establish connection to database. Levels plugin malfunctioning.")
            return

        xp = int(db.hget(f"levels:user:{user.id}", "xp"))
        level, to_next = self.get_level(xp)
        users = [(x, db.hget(x, "xp"))
                 for x in db.scan_iter(match="levels:user:*")]

        def key(item):
            return item[1]
        rankings = [int(x[0][12:])
                    for x in sorted(users, key=key, reverse=True)]

        rank = rankings.index(user.id) + 1

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
            name="Rank",
            value=f"#{rank}")

        embed.add_field(
            name="Current level",
            value=level)

        embed.add_field(
            name="XP to level up",
            value=to_next)

        embed.add_field(
            name="Total XP",
            value=xp)

        # Send the embed.
        await ctx.send(embed=embed)

    @commands.Cog.listener()
    async def on_message(
            self,
            message: Message):
        """
        Award the user with experience when they send messages to supported channels.
        """

        if not message.content.startswith(self.bot.command_prefix):
            if message.channel.id not in self.blacklisted_channels:
                db = get_db()
                if not db:
                    return

                xp = random.randint(5, 15)
                db.hincrby(f"levels:user:{message.author.id}", "xp", amount=xp)
