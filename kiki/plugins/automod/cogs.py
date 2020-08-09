"""Automod cogs.

Essential functionality for the automod plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level automod plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

from discord.ext import commands
from discord.utils import find

from kiki.plugins.automod.utils import checks


class Automod(commands.Cog):
    """Automod Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the automod plugin.
    """

    def __init__(self, bot):
        """Initialize the Cog.
        """

        self.bot = bot
        # Dictionary where keys are channel ID, values are role ID.
        # Eventually this will be moved to database.
        self.supported_channels = {
            558027628502712334: 722115152832364624,
            558085901255704577: 722115302669811785
        }
        # List of available roles for users to join/leave as they please.
        # Eventually this will be moved to database.
        # bot.get_emoji(id)
        self.supported_roles = {
            742115931542519810: {
                "name": "Counter-Strike: Global Offensive",
                "role": 673282506543464488,
            },
            742115929621790799: {
                "name": "Valorant",
                "role": 700130836527317002,
            },
            742115929906872329: {
                "name": "Overwatch",
                "role": 673282438037897284,
            },
            742115929957072988: {
                "name": "Minecraft",
                "role": 673282603440406567,
            },
            742115930187759679: {
                "name": "Jackbox",
                "role": 708866612626718820,
            },
            742115930196410558: {
                "name": "League of Legends",
                "role": 712462587857600523,
            },
            742116519919484928: {
                "name": "Smite",
                "role": 739259679707889774,
            },
            742115931714617404: {
                "name": "Fall Guys",
                "role": 740597562545012818,
            },
        }
        self.role_message_id = 1234

    @commands.command()
    @commands.check(checks.check_admin)
    async def spit(self, ctx: commands.Context):
        """List supported roles.

        Args:
            ctx: Discord.py context object.
        """

        message = "**Games**\n"
        emojis = []
        se = self.bot.util_guild.emojis
        for eid, value in self.supported_roles.items():
            emoji = find(lambda x: x.id == eid, se)
            if emoji:
                emojis.append(emoji)
                message += f"\n{emoji} {value['name']} (<@&{value['role']}>)"

        message += "\n\nReact below with a game icon to join its corresponding role!"  # noqa

        m = await ctx.send(message)
        await self.__set_role_message_id(m.id)
        for e in emojis:
            await m.add_reaction(e)

        print(self.role_message_id)

    @commands.Cog.listener()
    async def on_ready(self):
        """
        """

        self.role_message_id = await self.__get_role_message_id()
        print(self.role_message_id)

    @commands.Cog.listener()
    async def on_raw_reaction_add(self, payload):
        """
        """

        message_id = payload.message_id

        if message_id != self.role_message_id:
            return

        guild = find(lambda x: x.id == payload.guild_id, self.bot.guilds)
        emoji_id = payload.emoji.id
        user = guild.get_member(payload.user_id)
        if user.bot:
            return
        game = self.supported_roles[emoji_id]
        role = find(lambda x: x.id == game["role"], guild.roles)
        if role:
            await user.add_roles(
                role,
                reason="Joined community through reaction")

    @commands.Cog.listener()
    async def on_raw_reaction_remove(self, payload):
        """
        """

        message_id = payload.message_id

        if message_id != self.role_message_id:
            return

        guild = find(lambda x: x.id == payload.guild_id, self.bot.guilds)
        emoji_id = payload.emoji.id
        user = guild.get_member(payload.user_id)
        if user.bot:
            return
        game = self.supported_roles[emoji_id]
        role = find(lambda x: x.id == game["role"], guild.roles)
        if role:
            await user.remove_roles(
                role,
                reason="Left community through reaction")

    @commands.Cog.listener()
    async def on_voice_state_update(self, member, before, after):
        """Voice state listener.

        When a user joins a supported voice channel, give them an @'able role.
        When they leave, remove the role. This allows users to @ everyone in a
        voice channel at once.

        Args:
            member: The discord Member that has modified their voice state.
            before: The users VoiceState prior to the change.
            after: The users VoiceState after the change.
        """

        # Shorthand local variables.
        b = before.channel
        a = after.channel

        # Assuming the user was not in a channel, but is now...
        if (b is None and a is not None):
            # And the channel they are in is supported...
            if a.id in self.supported_channels.keys():
                # Add the role.
                role_id = self.supported_channels.get(a.id)
                role = find(lambda x: x.id == role_id, member.guild.roles)
                await member.add_roles(role, reason="In voice channel")

        # Assuming the user was in a channel, but is not anymore...
        if (b is not None and a is None):
            # And the channel they were in is supported...
            if b.id in self.supported_channels.keys():
                # Remove the role.
                role_id = self.supported_channels.get(b.id)
                role = find(lambda x: x.id == role_id, member.guild.roles)
                await member.remove_roles(role, reason="Left voice channel")

        # Assuming the user was in a channel,
        # but is in a different channel now...
        if (b is not None and a is not None and b != a):
            # And the channel they were in is supported...
            if b.id in self.supported_channels.keys():
                # Remove the role.
                role_id = self.supported_channels.get(b.id)
                role = find(lambda x: x.id == role_id, member.guild.roles)
                await member.remove_roles(role, reason="Left voice channel")
            # And the channel they are in is supported...
            if a.id in self.supported_channels.keys():
                # Add the role.
                role_id = self.supported_channels.get(a.id)
                role = find(lambda x: x.id == role_id, member.guild.roles)
                await member.add_roles(role, reason="In voice channel")

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """Message listener.

        When new users join the server, it grants them with a complimentary
        default role.

        Args:
            member: The user that joined the server.
        """

        # Find an appropriate default role.
        role = find(lambda x: x.name == "folk", member.guild.roles)

        # Assign the role, if it was found.
        if role:
            await member.add_roles(
                role,
                reason="Granting new user default role.")

    async def __get_role_message_id(self) -> int:
        """
        """

        redis = self.bot.redis
        id_raw = await redis.get("automod:rmid")
        return int(id_raw)

    async def __set_role_message_id(self, rmid: int):
        """
        """

        redis = self.bot.redis
        self.role_message_id = rmid
        await redis.set("automod:rmid", rmid)
