"""
Automod plugin.
"""

from .cogs import WelcomeRole


def setup(bot):
    """
    Set up plugin.
    """

    bot.add_cog(WelcomeRole(bot))
