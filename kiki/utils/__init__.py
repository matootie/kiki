from discord.ext import commands


def is_admin():
    async def predicate(ctx):
        return ctx.author.id == 183731781994938369
    return commands.check(predicate)
