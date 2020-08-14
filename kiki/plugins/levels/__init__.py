"""Levels plugin.

Top level of the levels plugin. This is what Kiki bot will import, and thus it
has its necessary setup step.

    Typical usage example:

    kiki.load_extension('kiki.plugins.levels')

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/extensions.html
"""

from plugins.levels.cogs import Text, Voice, Levels


def setup(bot):
    """Set up plugin.

    Simple setup of the levels plugin.
    """

    bot.add_cog(Text(bot))
    bot.add_cog(Voice(bot))
    bot.add_cog(Levels())
