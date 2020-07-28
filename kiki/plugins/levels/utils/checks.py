"""
"""

from discord.ext.commands import Context


def check_admin(ctx: Context) -> bool:
    """Checks that the author of a command is an admin.
    """

    return ctx.message.author.id == 183731781994938369


def check_database(ctx: Context) -> bool:
    """Checks that the database is running.

    Discord.py command check to verify that the database is running.

    Args:
        ctx: Discord.py context object to check against.

    Returns:
        A bool indicating whether or not the database is connected. True if
        connected, false otherwise.
    """

    # Determine whether or not Redis is available.
    return bool(ctx.bot.redis)
