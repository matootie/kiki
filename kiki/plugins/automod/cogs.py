"""Automod cogs.

Essential functionality for the automod plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level automod plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

import typing
from discord.ext import commands
from discord.utils import find
from discord import Role


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
        self.supported_roles = [
            673282506543464488,
            700130836527317002,
            703783696460939335,
            673282438037897284,
            673282603440406567,
            708866612626718820,
            712462587857600523,
            717925373647519774,
            722123884811386971,
            721215716564533279,
            722140497812127777,
            722140535133044787,
            722148256385335346,
            722148258516041779,
            722148300660277248,
            725800015901098207,
            725800019394822275,
            725800021051572256,
            725800024058888192,
            725800917068415166,
            725852723354009663,
            725853438755471440,
            725853029710168115,
            725853264066904085,
            725853325085507625,
            725853358665236531,
            739259679707889774
        ]

    @commands.command()
    async def list(self, ctx: commands.Context):
        """List supported roles.

        Args:
            ctx: Discord.py context object.
        """

        message = "Here's a list of supported roles:\n\n"

        for role_id in self.supported_roles:
            role = find(lambda x: x.id == role_id, ctx.guild.roles)
            if role:
                message += f"\"{role.name}\"\n"

        message += "\nYou can add roles using the `.join` command, "\
            "specifying each role by mention or by full name (in quotes)."

        await ctx.send(message)

    @commands.command()
    async def join(
            self,
            ctx: commands.Context,
            roles: commands.Greedy[typing.Union[Role, str]]):
        """Join supported roles.

        Args:
            ctx: Discord.py context object.
            roles: Collection of roles by mention or by name.
        """

        r = []
        for role in roles:
            if type(role) == str:
                role = find(lambda x: x.name == role, ctx.guild.roles)
            if role and role.id in self.supported_roles:
                r.append(role)
        if r:
            await ctx.author.add_roles(*r, reason="Subscribed to roles")

    @commands.command()
    async def leave(
            self,
            ctx: commands.Context,
            roles: commands.Greedy[typing.Union[Role, str]]):
        """Leave supported roles.

        Args:
            ctx: Discord.py context object.
            roles: Collection of roles by mention or by name.
        """

        r = []
        for role in roles:
            if type(role) == str:
                role = find(lambda x: x.name == role, ctx.guild.roles)
            if role.id in self.supported_roles:
                r.append(role)
        if r:
            await ctx.author.remove_roles(*r, reason="Unsubscribed from roles")

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
