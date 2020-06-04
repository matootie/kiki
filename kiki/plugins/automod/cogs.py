"""Automod cogs.

Essential functionality for the automod plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level automod plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

from discord.ext.commands import Cog
from discord.utils import find


class WelcomeRole(Cog):
    """Welcome role Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the "welcome role" aspect of the automod plugin.
    """

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
