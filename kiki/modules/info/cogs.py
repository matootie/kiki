"""Info cogs.

Essential functionality for the info module to run. This module contains the
main functionality of the module. There is no typical usage here as the
top-level info module is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

import aiohttp
from discord import Embed
from discord.ext import commands


class Info(commands.Cog):
    """Info Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the info module.
    """
    @commands.command()
    async def info(self, ctx: commands.Context):
        """Show the bot statistics sheet

        A command to show the current status of the inner-workings of the bot,
        such as database connections or the current running version. Invoked by
        members of a shared server with the bot. The response is sent back to
        the original context in the form of a Discord embed.

        Args:
            ctx: Discord.py context object.
        """

        # Build the embed.
        embed = Embed(
            title="Status Sheet",
            type="rich",
            description="Outline of what's working with Kiki, and, more \
                importantly, what isn't.")

        # Set the author of the embed.
        embed.set_author(
            name="Kiki & Riki",
            url="https://github.com/matootie/kiki",
            icon_url=
            "https://cdn.discordapp.com/icons/558027628502712330/27a8e964b8c8f68a64e158afb82fbf3e.png?size=128"
        )  # noqa

        # Set a footer for the embed.
        embed.set_footer(text="Report any issues to an admin.")

        # Add database stats.
        db_status = bool(ctx.bot.redis)
        embed.add_field(name="Database",
                        value="🟢 Running" if db_status else "🔴 Down",
                        inline=True)

        # Add website stats.
        web_status: int = None
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get("https://kikiriki.ca") as response:
                    web_status = response.status
        except:
            pass
        embed.add_field(name="Website",
                        value="🟢 Running" if web_status == 200 else "🔴 Down",
                        inline=True)

        # Add version stats.
        embed.add_field(name="Version", value=ctx.bot.version, inline=False)

        # Send the statistics sheet.
        await ctx.send(embed=embed)
