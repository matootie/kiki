"""

"""

from aioredis import Redis
from discord import User


async def check_database(ctx):
    """
    Command check to see that the database is running.
    """

    if not ctx.bot.redis:
        await ctx.send("Reason: **Database connection unavailable**\nUse `.info` to view the current status sheet.")
        return False
    return True


async def get_experience(
        redis: Redis,
        user: User) -> int:
    """
    """

    experience = 0 # TODO: Get the experience.
    return experience


async def set_experience(
        redis: Redis,
        user: User,
        experience: int = None,
        offset: int = 0) -> int:
    """
    """

    if experience:
        # TODO: Set to exact value.
        return experience

    new_experience = 0 # TODO: Apply offset.
    return new_experience
