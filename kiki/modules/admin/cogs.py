from discord.ext import commands

_MODULES = [
    "kiki.modules.info",
    "kiki.modules.levels",
]

class Admin(commands.Cog):
    @commands.command()
    async def reload(self, ctx: commands.Context):

        if ctx.author.id != 183731781994938369:
            return

        successful = []
        failed = []

        for module in _MODULES:
            try:
                ctx.bot.reload_extension(module)
                successful.append(module)
            except Exception as e:
                print(e)
                failed.append(module)

        message = "Done."
        if successful:
            message += "\n\n"
            message += f"Successfully reloaded {len(successful)} modules."
            message += "\n- "
            message += "\n- ".join(successful)

        if failed:
            message += "\n\n"
            message += f"{len(failed)} modules failed to reload."
            message += "\n- "
            message += "\n- ".join(failed)

        await ctx.send(message)
