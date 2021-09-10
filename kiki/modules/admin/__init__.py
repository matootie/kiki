from .cogs import Admin


def setup(bot):
    bot.add_cog(Admin())
