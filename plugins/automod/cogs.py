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

    @commands.command()
    async def tempadmin(self, arg, ctx):
        """
        Grant temporary admin to matootie.
        """

        if message.channel.guild.id == 558027628502712330:
            if ctx.message.author.id == 183731781994938369:
                if arg == "on":
                    role = find(lambda x: x.name == "tempadmin", guild.roles[::-1])
                    if role:
                        await ctx.message.author.add_roles(role)
                elif arg == "off":
                    role = find(lambda x: x.name == "tempadmin", guild.roles[::-1])
                    if role:
                        await ctx.message.author.remove_roles(role)
                elif arg == "init":
                    role = find(lambda x: x.name == "tempadmin", guild.roles[::-1])
                    if not role:
                        await ctx.message.channel.guild.create_role(
                            name="tempadmin",
                            permissions = Permissions(permissions=8))
                else:
                    await ctx.send("Invalid argument. Must be 'on' of 'off'")
            else:
                await ctx.send("You aren't authorized to perform this action")


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
