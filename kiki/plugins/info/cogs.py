"""
Info cogs.
"""

from datetime import datetime
from discord.ext import commands
from discord import Embed


class Info(commands.Cog):
    """
    Info Cog.
    """

    def __init__(self, bot):
        """
        Initialize the Cog.
        """

        self.bot = bot

    @commands.command()
    async def info(self, ctx):
        """
        Info.
        """

        # Set up the embed.
        embed = Embed(
            title="Status Sheet",
            type="rich",
            description="Outline of what's working at Kikiriki, and, more \
                importantly, what isn't.",
            url="https://kikiriki.ca/status",
            timestamp=datetime.utcnow())

        embed.set_author(
            name="Kikiriki Studios Canada",
            url="https://kikiriki.ca/",
            icon_url="https://cdn.discordapp.com/attachments/604373743837511693/653741067904221231/icon_circle_variant_1000x1000.png")  # noqa

        embed.set_footer(text="Report any issues to an admin.")

        # Check database and add info to embed.
        db_status = bool(self.bot.redis)

        embed.add_field(
            name="Database connection",
            value="🟢 Running" if db_status else "🔴 Down",
            inline=False)

        # Send the embed.
        await ctx.send(embed=embed)
