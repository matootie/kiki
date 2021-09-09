"""Info module.

Top level of the info module. This is what Kiki bot will import, and thus it
has its necessary setup step.

    Typical usage example:

    kiki.load_extension('kiki.modules.info')

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
"""

from .cogs import Info


def setup(bot):
    """Set up module.

    Simple setup of the info module.
    """

    bot.add_cog(Info())
