from discord.ext import commands
from discord.utils import find


class WelcomeRole(commands.Cog):
    """
    Welcome role Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Grant default role on join.
        """

        guild = member.guild
        role = find(lambda x: x.name == "folk", guild.roles)
        if role:
            await member.add_roles(
                role,
                reason="Granting new user default role.")
