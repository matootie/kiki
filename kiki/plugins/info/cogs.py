"""Info cogs.

Essential functionality for the info plugin to run. This module contains the
main functionality of the plugin. There is no typical usage here as the
top-level info plugin is the only module that requires access to this code.

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
"""

from discord import Embed
from discord.ext import commands


class Info(commands.Cog):
    """Info Cog.

    Discord.py extensions Cog, defining all commands and listeners related to
    the info plugin.
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
            name="Kikiriki Studios Canada",
            url="https://github.com/matootie/kiki",
            icon_url="https://cdn.discordapp.com/attachments/604373743837511693/653741067904221231/icon_circle_variant_1000x1000.png")  # noqa

        # Set a footer for the embed.
        embed.set_footer(text="Report any issues to an admin.")

        # Add database stats.
        db_status = bool(ctx.bot.redis)
        embed.add_field(
            name="Database connection",
            value="🟢 Running" if db_status else "🔴 Down",
            inline=False)

        # Add version stats.
        embed.add_field(
            name="Version",
            value=ctx.bot.version,
            inline=False)

        # Send the statistics sheet.
        await ctx.send(embed=embed)
