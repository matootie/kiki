"""Info plugin.

Top level of the info plugin. This is what Kiki bot will import, and thus it
has its necessary setup step.

    Typical usage example:

    kiki.load_extension('kiki.plugins.info')

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
"""

from .cogs import Info


def setup(bot):
    """Set up plugin.

    Simple setup of the info plugin.
    """

    bot.add_cog(Info())
