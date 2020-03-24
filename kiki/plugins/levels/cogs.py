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
from orm.exceptions import NoMatch

from .models import User


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
    async def enrol(self, ctx):
        """
        Enrol in the experience system.
        """

        # Create a new user entry in the database.
        await User.objects.create(id=str(ctx.author.id), experience=0)

        # Sent feedback.
        await ctx.send("Welcome to the experience system. Start chatting!")

    @commands.command()
    async def rank(self, ctx, user: typing.Optional[DiscordUser]):
        """
        Show the users ranking stats.
        """

        # Choose the appropriate user.
        if not user:
            user = ctx.author

        # Get the user instance from the database.
        try:
            db_user = await User.objects.get(id=str(user.id))
        except NoMatch:
            await ctx.send("You are not enrolled in the experience system. \
                Type `.enrol` to begin.")
            return

        # Fetch the data.
        level = db_user.level
        total = db_user.experience

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

        # Calculate the xp to award.
        xp_to_gain = random.randint(5, 15)

        # Get the user instance from the database.
        try:
            user = await User.objects.get(id=str(message.author.id))
        except NoMatch:
            return

        # Calculate the users new experience.
        xp = user.experience + xp_to_gain

        # Apply changes.
        await user.update(experience=xp)
