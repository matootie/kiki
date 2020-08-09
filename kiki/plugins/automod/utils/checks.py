"""
"""

from discord.ext.commands import Context


def check_admin(ctx: Context) -> bool:
    """Checks that the author of a command is an admin.
    """

    return ctx.message.author.id == 183731781994938369
