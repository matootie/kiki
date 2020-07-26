"""Levels cogs.

Essential functionality for the levels plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level levels plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

import typing

from discord import User, Embed, Message, Member, VoiceState
from discord.ext import commands
from discord.utils import find

from kiki.plugins.levels import utils


class Levels(commands.Cog):
    """Levels Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the levels plugin.

    Attributes:
        bot: A reference to the main bot, only used within listeners.
    """

    def __init__(self, bot):
        """
        """

        self.bot = bot
        self.voice = utils.Voice(bot)

    @commands.command()
    @commands.check(utils.check_database)
    async def rank(self, ctx: commands.Context, user: typing.Optional[User]):
        """Show the users ranking stats.

        A command to show the level and total experience of a given
        user. Invoked by members of a shared server with the bot. The response
        is sent back to the original context in the form of a Discord embed.

        Args:
            ctx: Discord.py context object.
            user: Optional third-party to check rankings for.
        """

        # Choose the appropriate user.
        if not user:
            user = ctx.author

        response = await utils.get_experience(ctx.bot.redis, user)
        level, total = utils.check_level(response)

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

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: Member,
            before: VoiceState,
            after: VoiceState):
        """
        """

        voice = self.voice

        # If they were previously eligible or they are eligible.
        if voice.eligible_member(member) or voice.eligible(after):
            bc = before.channel
            ac = after.channel
            # Refresh the state for the channel they were in, if there is one.
            if bc:
                await voice.refresh(bc)
            # Refresh the state for the channel they are in, if there is one,
            # only if the channel is not the same.
            if ac and ac != bc:
                await voice.refresh(ac)

    @commands.Cog.listener()
    async def on_member_update(
            self,
            before: Member,
            after: Member):
        """
        """

        voice = self.voice
        ba = before.activity
        aa = after.activity

        # If their activity has changed.
        if ba != aa:
            bv = before.voice
            av = after.voice

            # If they were previously eligible or they are eligible.
            if voice.eligible(bv) or voice.eligible(av):
                bc = bv.channel
                ac = av.channel

                # Refresh the state for the channel they were in,
                # if there is one.
                if bc:
                    await voice.refresh(bc)
                # Refresh the state for the channel they are in,
                # if there is one.
                if ac:
                    await voice.refresh(ac)

    @commands.Cog.listener()
    async def on_message(self, message: Message):
        """Message listener.

        Listen for messages and award message authors with experience when they
        send messages to supported channels.

        Args:
            message: The message that was sent.
        """

        # Preemptive checks.
        if not utils.check_database(self):
            return
        if message.author.bot:
            return
        if (await utils.is_blocked(self.bot.redis, message.author)):
            return

        # Award experience.
        xp = await utils.calculate_worth(
            self.bot.redis,
            self.bot.dictionary,
            message)
        new_xp = await utils.set_experience(
            self.bot.redis,
            message.author,
            offset=xp)

        old_xp = new_xp - xp
        old_level, _ = utils.check_level(old_xp)
        new_level, _ = utils.check_level(new_xp)

        if old_level >= new_level:
            return

        # User has ranked up.
        await message.channel.send(
            f"{message.author.mention}, you are now level {new_level}.")

        old_digits = len(str(old_level))
        new_digits = len(str(new_level))

        if new_digits > 4 or old_digits >= new_digits:
            return

        role_structure = {
            1: find(lambda x: x.id == 717586013534421002, message.guild.roles),
            2: find(lambda x: x.id == 717586130689589309, message.guild.roles),
            3: find(lambda x: x.id == 717586290740297739, message.guild.roles),
            4: find(lambda x: x.id == 717586479236251732, message.guild.roles),
        }

        outranked = []
        for digits, role in role_structure.items():
            if digits == new_digits:
                await message.author.add_roles(
                    role,
                    reason="User has gained a new status")
                break
            outranked.append(role)

        await message.author.remove_roles(
            *outranked,
            reason="User has outranked this status")
