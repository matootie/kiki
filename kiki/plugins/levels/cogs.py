"""
Levels cogs.
"""

import random
import typing
import enchant
import math

from discord.ext import commands
from discord import User as DiscordUser
from discord import Embed

from kiki.plugins.levels.utils import check_database


class Levels(commands.Cog):
    """
    Levels Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot
        self._d = enchant.Dict("en")


    @commands.command()
    @commands.check(check_database)
    async def rank(self, ctx, user: typing.Optional[DiscordUser]):
        """
        Show the users ranking stats.
        """

        # Choose the appropriate user.
        if not user:
            user = ctx.author

        redis = self.bot.redis
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
            type="rich")
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

    async def calculate_xp(self, message):
        """
        Calculate experience based on size and complexity of message. Makes use
        of Redis sets, more information can be found in references.

        References:
          https://redis.io/commands#set
        """

        redis = self.bot.redis

        content = message.content
        m = ' '.join(content.split())
        character_count = len(m.replace(" ", ""))
        points = 49 * math.pow(2.7, -(math.pow(character_count - 120, 2)/9000)) + 1
        words = set([word.lower() for word in m.split(" ") if self._d.check(word)])

        # Determine the valid words by checking whether they exist in the
        # blocked set.
        valid_words = []
        for word in words:
            is_member = await redis.sismember("blockedwords", word)
            if not is_member:
                valid_words.append(word)

        word_lengths = [len(word) for word in valid_words]
        divisor = len(word_lengths) if len(word_lengths) > 0 else 1
        avg_word_length = sum(word_lengths) / divisor
        multiplier = math.pow(avg_word_length - 4.7, 3)/120 + 1

        # Block the new words.
        await redis.spop("blockedwords", len(valid_words))
        await redis.sadd("blockedwords", *valid_words)

        return int(points * multiplier)

    @commands.Cog.listener()
    async def on_message(self, message):
        """
        Award the user with experience when they send messages to supported
        channels.
        """

        redis = self.bot.redis
        user = message.author

        if not redis:
            return
        if user.bot:
            return
        blocked = await redis.exists(f"cd:{user.id}")
        if blocked:
            return

        xp_to_gain = await self.calculate_xp(message)
        await redis.incrby(
            f"xp:{user.id}",
            xp_to_gain)
        await redis.set(
            f"cd:{user.id}",
            "true",
            expire=60)
