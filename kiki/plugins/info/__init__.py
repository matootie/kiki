"""
Info plugin.
"""

import requests
from requests.exceptions import ConnectionError
from datetime import datetime
from discord.ext import commands
from discord import Embed
from mcstatus import MinecraftServer
from socket import gaierror

from kiki.utils.db import get_db


@commands.command()
async def info(ctx):
    """
    Info.
    """

    # Set up the embed.
    embed = Embed(
        title="Status Sheet",
        type="rich",
        description="Outline of what's working at Kikiriki, and, more importantly, what isn't.",
        url="https://kikiriki.ca/status",
        timestamp=datetime.utcnow())

    embed.set_author(
        name="Kikiriki Studios Canada",
        url="https://kikiriki.ca/",
        icon_url="https://cdn.discordapp.com/attachments/604373743837511693/653741067904221231/icon_circle_variant_1000x1000.png")

    embed.set_footer(text="Report any issues to an admin.")

    # Check database and add info to embed.
    db_status = bool(get_db())

    embed.add_field(
        name="Database connection",
        value="🟢 Running" if db_status else "🔴 Down",
        inline=False)

    # Check Minecraft server status and add info to embed.
    mc_status = False
    mc_players = 0
    mc_version = "N/A"

    try:
        mc_server = MinecraftServer.lookup("mc.kikiriki.ca")
        ping = mc_server.ping()
        mc_status = bool(ping)
        mc_players = mc_server.query().players.online
        mc_version = mc_server.query().software.version
    except gaierror:
        pass

    embed.add_field(
        name="Minecraft server status",
        value="🟢 Running" if mc_status else "🔴 Down",)

    embed.add_field(
        name="Minecraft server players online",
        value=mc_players)

    embed.add_field(
        name="Minecraft server version",
        value=mc_version)

    # Check website status.
    web_status = False

    try:
        web_response = requests.get("https://kikiriki.ca")
        web_status = web_response.status_code == 200
    except ConnectionError:
        pass

    embed.add_field(
        name="Website status",
        value="🟢 Running" if web_status else "🔴 Down",
        inline=False)

    # Send the embed.
    await ctx.send(embed=embed)


def setup(bot):
    """
    Set up plugin.
    """

    bot.add_command(info)
