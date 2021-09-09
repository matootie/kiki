"""Levels cogs.

Essential functionality for the levels plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level levels plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

import typing
import math

from datetime import datetime
from discord import User, Embed, Message, Member, VoiceState, VoiceChannel
from discord.ext import commands
from discord.utils import find
from kiki.plugins.levels import utils
from kiki.plugins.levels.utils.checks import check_database, check_admin


class Voice(commands.Cog):
    """
    """

    def __init__(self, bot):
        """
        """

        self.bot = bot
        self.state = {}

    @commands.command()
    @commands.check(check_database)
    @commands.check(check_admin)
    async def allranks(
            self,
            ctx: commands.Context):
        """
        """

        guild = ctx.guild
        redis = self.bot.redis

        string = ""
        cursor = b"0"
        while cursor:
            cursor, keys = await redis.scan(cursor, match='xp:*')
            for key in keys:
                member = guild.get_member(int(key[3:]))
                level = await utils.get_level(redis, member)
                string += f"{member.name} :: {level}\n"

        await ctx.send(string)

    @commands.Cog.listener()
    async def on_voice_state_update(
            self,
            member: Member,
            before: VoiceState,
            after: VoiceState):
        """Refresh state when things change.
        """

        be, bc = self.__eligible(member=member)
        ae, ac = self.__eligible(state=after)
        if be or ae:
            if bc:
                await self.__refresh_state(bc)
            if ac and ac != bc:
                await self.__refresh_state(ac)

    @commands.Cog.listener()
    async def on_member_update(
            self,
            before: Member,
            after: Member):
        """
        """

        ba = before.activity
        aa = after.activity

        if ba != aa:
            be, bc = self.__eligible(member=before)
            ae, ac = self.__eligible(state=after.voice)
            if be or ae:
                if bc:
                    await self.__refresh_state(bc)
                if ac and ac != bc:
                    await self.__refresh_state(ac)

    def __user_multiplier(
            self,
            count: int) -> float:
        """
        """

        if count < 2:
            return 1
        return (1 / 6) * (count - 2) + 1

    def __game_multiplier(
            self,
            count: int) -> float:
        """
        """

        if count < 2:
            return 1
        return (1 / 4) * (count - 2) + 1.5

    def __experience_rate(
            self) -> float:
        """
        """

        return 2

    async def __apply_state(
            self,
            channel: VoiceChannel):
        """Apply state experience to database.
        """

        # Preemptive checks.
        state = self.state.get(channel.id)
        if not state:
            return

        # Calculate the time diff.
        now = datetime.now()
        then = state["timestamp"]
        delta = now - then
        time = delta.total_seconds()

        # Count members for multipliers
        members = []
        for game, memberss in state["activities"].items():
            multiplier = self.__game_multiplier(len(memberss)) if game else 1
            for member in memberss:
                members.append((member, multiplier))

        user_multiplier = self.__user_multiplier(len(members))

        # Apply experience.
        rate = self.__experience_rate()
        redis = self.bot.redis
        guild = self.bot.guild
        for member, game_multiplier in members:
            xp = rate * time * user_multiplier * game_multiplier
            new_xp = await utils.apply(
                redis,
                id=member,
                offset=int(xp),
                cooldown=0)

            # Determine if the user has ranked up.
            new, all = await utils.ranked_up(
                redis,
                guild.roles,
                new_xp - xp,
                new_xp)
            if new:
                m = guild.get_member(member)
                # Clean the slate and award new role.
                await m.remove_roles(*all)
                await m.add_roles(new)

    async def __update_state(
            self,
            channel: VoiceChannel):
        """Update changes in a channel state.
        """

        # Completely reset the state.
        state = {
            "timestamp": datetime.now(),
            "activities": {
                None: [],
            },
        }
        self.state[channel.id] = state

        # Rebuild the state member by member.
        for member in channel.members:
            e, _ = self.__eligible(state=member.voice)
            if e:
                game = member.activity
                if game:
                    valid = await self.__valid(game.name)
                    game = game.name if valid else None
                state["activities"].setdefault(game, [])
                state["activities"][game].append(member.id)

        # Apply the new, rebuilt state.
        self.state[channel.id] = state

    async def __refresh_state(
            self,
            channel: VoiceChannel):
        """Refresh the state for a channel.

        Apply changes, then reload the state.
        """

        await self.__apply_state(channel)
        await self.__update_state(channel)

    def __unobstructed(
            self,
            state: VoiceState) -> bool:
        """Determine if a user is obstructed.
        """

        mute = state.mute or state.self_mute
        deaf = state.deaf or state.self_deaf
        obstructed = mute or deaf

        return not obstructed

    def __peers_channel(
            self,
            channel: VoiceChannel) -> int:
        """Determine the number of unobstructed members in a channel.
        """

        p = 0
        if channel:
            for member in channel.members:
                if self.__unobstructed(member.voice):
                    p += 1
        return p

    def __peers_state(
            self,
            channel: VoiceChannel) -> int:
        """Determine the number of members in the state
        """

        members = 0
        state = self.state
        if not channel or not state.get(channel.id):
            return 0
        for member in state[channel.id]["activities"].values():
            members += 1
        return members

    def __eligible(
            self,
            state: VoiceState = None,
            member: Member = None) -> bool:
        """Determine if a user is eligible.
        """

        # Preemptive check
        if not state and not member:
            raise AssertionError

        if state:
            is_unobstructed = self.__unobstructed(state)
            channel = state.channel
            previous_peers = self.__peers_state(channel)
            current_peers = self.__peers_channel(channel)
            enough_peers = previous_peers > 1 or current_peers > 1

            return is_unobstructed and enough_peers, channel

        if member:
            for channel_id, state in self.state.items():
                for member_list in state["activities"].values():
                    if member.id in member_list:
                        c = find(
                            lambda x: x.id == channel_id,
                            self.bot.guild.voice_channels)
                        return True, c
            return False, None

    async def __valid(
            self,
            game: str) -> bool:
        """Check that a game is valid.
        """

        games = await self.bot.redis.smembers("meta:games")
        return game in games


class Text(commands.Cog):
    """
    """

    def __init__(self, bot):
        """
        """

        self.bot = bot

    @commands.Cog.listener()
    async def on_message(
            self,
            message: Message):
        """Message listener.

        Listen for messages and award message authors with experience when they
        send messages to supported channels.

        Args:
            message: The message that was sent.
        """

        redis = self.bot.redis
        author = message.author

        # Run some preemptive checks.
        if not check_database(self):
            return
        if author.bot:
            return
        if message.content.startswith("."):
            return
        if (await self.__is_blocked(author)):
            return

        # Award experience.
        xp = await self.__calculate_worth(message)
        new_xp = await utils.apply(
            redis,
            user=author,
            offset=xp)

        # Determine if the user has ranked up.
        new, all = await utils.ranked_up(
            redis,
            message.guild.roles,
            new_xp - xp,
            new_xp)
        if new:
            # Clean the slate and award new role.
            await author.remove_roles(*all)
            await author.add_roles(new)

    async def __calculate_worth(
            self,
            message: Message) -> int:
        """Determines value of a message.

        Calculates the experience value of a given message. This is determined
        by both the character count and the complexity of the message. A
        message is given a score based on the number of characters, excluding
        spaces. Less characters will score lower, but too many characters will
        also score low. The message will also be given a multiplier based on
        the average word length of real words that have not been used
        previously. The resulting score is the character count score multiplied
        by the word-length multiplier.

        Args:
            redis: An available connection to Redis.
            dictionary: The dictionary to use for real-word validation.
            message: The message to calculate a score for.

        Returns:
            An integer representing the score for that given message.
        """

        redis = self.bot.redis

        # Parse out extra spaces.
        content = message.content
        message = ' '.join(content.split())

        # Collect a character count score, omitting spaces.
        character_count = len(message.replace(" ", ""))
        points = 49 * \
            math.pow(2.7, -(math.pow(character_count - 120, 2)/9000)) + 1

        # Collect a set of words.
        words = set(
            [word.lower()
             for word in message.split(" ")])
        # Determine the valid words by checking whether they exist in the
        # blocked set.
        valid_words = []
        for word in words:
            is_member = await redis.sismember("blockedwords", word)
            if not is_member:
                valid_words.append(word)

        # Calulate average word length multiplier, carefully preventing
        # division by zero.
        word_lengths = [len(word) for word in valid_words]
        divisor = len(word_lengths) if len(word_lengths) > 0 else 1
        avg_word_length = sum(word_lengths) / divisor
        multiplier = math.pow(avg_word_length - 4.7, 3)/120 + 1

        # Block the new words.
        if valid_words:
            await redis.spop("blockedwords", len(valid_words))
            await redis.sadd("blockedwords", *valid_words)

        # Return the calculated score.
        return int(points * multiplier)

    async def __is_blocked(
            self,
            user: User) -> bool:
        """Check if a user is blocked.

        Determines whether or not a user is blocked from gaining experience.

        Args:
            user: The user to check.

        Returns:
            A bool for whether or not the user is currently blocked. True if
            blocked, false otherwise.
        """

        # Determine if the cooldown key exists for that user.
        result = await self.bot.redis.exists(f"cd:{user.id}")

        # Return the result.
        return result


class Levels(commands.Cog):
    """Levels Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the levels plugin.
    """

    @commands.command()
    @commands.check(check_database)
    async def rank(
            self,
            ctx: commands.Context,
            user: typing.Optional[User]):
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

        redis = ctx.bot.redis

        # Get the level.
        level = await utils.get_level(redis, user)
        role = await utils.get_ranking_role(redis, user, ctx.guild.roles)

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
            name="Ranking",
            value=role.name)

        # Send the embed.
        await ctx.send(embed=embed)
