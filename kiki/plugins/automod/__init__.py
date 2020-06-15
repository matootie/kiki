"""Automod plugin.

Top level of the automod plugin. This is what Kiki bot will import, and thus it
has its necessary setup step.

    Typical usage example:

    kiki.load_extension('kiki.plugins.automod')

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
"""

from .cogs import Automod


def setup(bot):
    """Set up plugin.

    Simple setup of the automod plugin.
    """

    bot.add_cog(Automod(bot))
