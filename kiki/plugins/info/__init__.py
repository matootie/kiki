"""
Info plugin.
"""

from .cogs import Info


def setup(bot):
    """
    Set up plugin.
    """

    bot.add_cog(Info(bot))
