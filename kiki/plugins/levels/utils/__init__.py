"""
"""

from aioredis import Redis
from discord import User, Role
from discord.utils import find


async def get_experience(
        redis: Redis,
        user: User) -> int:
    """Get experience for a user.

    Fetches the users current experience amount from the database.

    Args:
        redis: An available connection to Redis.
        user: The user to fetch experience for.

    Returns:
        An integer value corresponding to the users current experience amount.
    """

    # Get the users experience from their xp key.
    experience = await redis.get(f"xp:{user.id}")

    return int(experience)


def __calculate_level(
        experience: int) -> int:
    """Calculate a level value based off of an experience value.
    """

    level = 0
    xp = experience
    while True:
        needed = 5 * (level ** 2) + 50 * level + 100
        xp -= needed
        if xp < 0:
            break
        level += 1

    return level


async def get_level(
        redis: Redis,
        user: User) -> int:
    """Get level for a user.

    Fetches the users current experience amount from the database, then it
    converts it to a level value.

    Args:
        redis: An available connection to Redis.
        user: The user to fetch level for.

    Returns:
        An integer value corresponding to the users current level.
    """

    experience = await get_experience(redis, user)

    if not experience:
        return 0

    return __calculate_level(experience)


async def __get_ranking_table(
        redis: Redis) -> dict:
    """Get the ranking table from database.
    """

    table_raw = await redis.hgetall("meta:rankings")
    table = {int(key): int(value) for key, value in table_raw.items()}
    if not table:
        raise KeyError
    return table


async def __get_ranking(
        redis: Redis,
        user: User) -> int:
    """Get ranking for a user.

    Fetches the users current level, then it converts
    it to a ranking index based on an internal ranking
    scale.
    """

    # Get the users level.
    level = await get_level(redis, user)

    # Get the ranking table.
    ranking = await __get_ranking_table(redis)

    top = 0
    ranking = list(ranking.keys())
    # For every level milestone in the ranking scale...
    for milestone in ranking:
        # If the users level has not surpassed the milestone...
        if level >= milestone:
            top = milestone
            continue
        break
    return top


async def get_ranking_role(
        redis: Redis,
        user: User,
        roles: list) -> Role:
    """Get the associated role for users ranking.

    Fetches the role from the ranking table.
    """

    rank = await __get_ranking(redis, user)
    ranking = await __get_ranking_table(redis)

    return find(lambda x: x.id == ranking[rank], roles)


async def __get_role(
        redis: Redis,
        roles: list,
        role_id: int = None):
    """Get a discord role for a role_id, or from the ranking table.
    """

    if role_id:
        return find(lambda x: x.id == role_id, roles)

    ranking = await __get_ranking_table(redis)

    rs = []
    for role_id in ranking.values():
        rs.append(find(lambda x: x.id == role_id, roles))

    return rs


async def ranked_up(
        redis: Redis,
        roles: list,
        before: int,
        after: int) -> (Role, list):
    """Determines if a user has ranked up.

    If they have, return the appropriate role ID to award.

    Args:
        before: Their previous experience.
        after: Their current experience.
    """

    # Get ranking table
    ranking = await __get_ranking_table(redis)

    # Convert experience to levels.
    before = __calculate_level(before)
    after = __calculate_level(after)

    # Determine of a rankup occurred.
    for milestone, role_id in ranking.items():
        # If their previous level did not pass a milestone...
        # But their current level did...
        if before < milestone and after >= milestone:
            # Return the role ID to award.
            awarded = await __get_role(redis, roles, role_id)
            all = await __get_role(redis, roles)
            return awarded, all
    # No rankup occurred.
    return None, None


async def apply(
        redis: Redis,
        user: User = None,
        id: int = None,
        experience: int = None,
        offset: int = 0,
        cooldown: int = 60) -> int:
    """Apply experience to a user.

    Writes a users experience to the database based on either a flat value or
    an offset. If a flat value is provided, the users xp will be overwritten
    with the given value. If an offset is provided, then the offset will be
    added to the users current experience level. Negative numbers are allowed.
    If both a flat value and an offset are provided, the flat value will trump
    the offset.

    Args:
        redis: An available connection to Redis.
        user: The user to set experience for.
        experience: A flat value of experience to set.
        offset: An amount of experience to add. Negative numbers will subtract.
        cooldown: Time in seconds representing how long the user will be
            prevented from gaining additional experience.

    Returns:
        An integer value representing the users new total experience amount.
    """

    # Determine the necessary queries for xp and cooldown.
    if not user:
        if not id:
            raise AssertionError
        uid = id
    else:
        uid = user.id
    xp_query = f"xp:{uid}"

    # If a flat value was provided, set to that and return.
    if experience:
        await redis.set(xp_query, experience)
        if cooldown:
            cooldown_query = f"cd:{user.id}"
            await redis.set(cooldown_query, str(True), expire=cooldown)
        return experience

    # Otherwise, add the provided offset value and return.
    new_experience = await redis.incrby(xp_query, offset)
    if cooldown:
        cooldown_query = f"cd:{user.id}"
        await redis.set(cooldown_query, str(True), expire=cooldown)
    return new_experience
