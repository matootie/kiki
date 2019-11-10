"""
Ping plugin.
"""

from discord.ext import commands


@commands.command()
async def ping(ctx):
    """
    Ping.
    """

    await ctx.send('pong')


def setup(bot):
    """
    Set up plugin.
    """

    bot.add_command(ping)
