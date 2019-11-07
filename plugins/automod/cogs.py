from discord.ext import commands
from discord.utils import find


DEFAULT_ROLE_ID = "558083037896769536"


class WelcomeRole(commands.Cog):
    """
    Welcome role Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot
        self.welcome_role = find(
            lambda x: x.id == DEFAULT_ROLE_ID,
            bot.primary_server)

    @commands.Cog.listener()
    async def on_member_join(self, member):
        """
        Grant default role on join.
        """

        await member.add_roles(
            self.welcome_role,
            reason="Granting new user default role.")
