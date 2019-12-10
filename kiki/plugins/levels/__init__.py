"""
Levels plugin.
"""

from .cogs import Levels


def setup(bot):
    """
    Set up plugin.
    """

    bot.add_cog(Levels(bot))
