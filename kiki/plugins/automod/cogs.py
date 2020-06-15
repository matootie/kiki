"""Automod cogs.

Essential functionality for the automod plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level automod plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

from discord.ext.commands import Cog
from discord.utils import find


class Automod(Cog):
    """Automod Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the automod plugin.
    """

    def __init__(self, bot):
        """Initialize the Cog.
        """

        # Dictionary where keys are channel ID, values are role ID.
        # Eventually this will be moved to database.
        self.supported_channels = {
            558027628502712334: 722115152832364624,
            558085901255704577: 722115302669811785
        }

    @Cog.listener()
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

    @Cog.listener()
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
