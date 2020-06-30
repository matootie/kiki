"""Levels plugin utilities.

Essential utilities for the levels plugin. This module contains any
additional tools and checks that the plugin requires.

    Typical usage example:

    @commands.check(check_database)
    async def my_command(self, ctx)

    total_xp = await get_experience(ctx.bot.redis, ctx.message.author)
    level = check_level(total_xp)

    value = await calculate_worth(ctx.bot.redis,
                                  ctx.bot.dictionary,
                                  ctx.message)
    if not (await is_blocked(ctx.bot.redis, ctx.message.author)):
        await set_experience(ctx.bot.redis, ctx.message.author, offset=value)

References:
- https://discordpy.readthedocs.io/en/latest/ext/commands/cogs.html
- https://discordpy.readthedocs.io/en/latest/ext/commands/api.html#checks
- http://pyenchant.github.io/pyenchant/#introduction
- https://redis.io/commands/get
- https://redis.io/commands/set
- https://redis.io/commands/exists
- https://redis.io/commands/sismember
- https://redis.io/commands/spop
- https://redis.io/commands/sadd
- https://aioredis.readthedocs.io/en/v1.3.0/mixins.html#generic-commands
"""

import math

from aioredis import Redis
from enchant import Dict
from discord import User, Message, VoiceState
from discord.ext.commands import Context


def check_database(ctx: Context) -> bool:
    """Checks that the database is running.

    Discord.py command check to verify that the database is running.

    Args:
        ctx: Discord.py context object to check against.

    Returns:
        A bool indicating whether or not the database is connected. True if
        connected, false otherwise.
    """

    # Determine whether or not Redis is available.
    return bool(ctx.bot.redis)


def check_level(total_experience: int = 0) -> int:
    """Calculates the level of a user.

    Runs a formula to determine the level of the user, based on their total
    experience.

    Args:
        total_experience: The total amount of experience the user has.

    Returns:
        A tuple containing the users current level, as well as their total
        experience. For example:

        (1, 127)
    """

    # If nothing was provided, simply return empty values.
    if not total_experience:
        return 0, 0

    # Continue with the level algorithm.
    level = 0
    xp = total_experience
    while True:
        needed = 5 * (level ** 2) + 50 * level + 100
        if xp - needed >= 0:
            xp -= needed
            level += 1
        else:
            break

    # Return the available values.
    return level, total_experience


def check_can_talk(voice_state: VoiceState) -> bool:
    return not voice_state.deaf \
        and not voice_state.mute \
        and not voice_state.self_mute \
        and not voice_state.self_deaf


async def is_blocked(redis: Redis, user: User) -> bool:
    """Check if a user is blocked.

    Determines whether or not a user is blocked from gaining experience.

    Args:
        redis: An available connection to Redis.
        user: The user to check.

    Returns:
        A bool for whether or not the user is currently blocked. True if
        blocked, false otherwise.
    """

    # Determine if the cooldown key exists for that user.
    result = await redis.exists(f"cd:{user.id}")

    # Return the result.
    return result


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

    # Return the result, ensuring it will be an integer.
    return int(experience)


async def calculate_worth(
        redis: Redis,
        dictionary: Dict,
        message: Message) -> int:
    """Determines value of a message.

    Calculates the experience value of a given message. This is determined by
    both the character count and the complexity of the message. A message is
    given a score based on the number of characters, excluding spaces. Less
    characters will score lower, but too many characters will also score low.
    The message will also be given a multiplier based on the average word
    length of real words that have not been used previously. The resulting
    score is the character count score multiplied by the word-length multiplier.

    Args:
        redis: An available connection to Redis.
        dictionary: The dictionary to use for real-word validation.
        message: The message to calculate a score for.

    Returns:
        An integer representing the score for that given message.
    """

    # Parse out extra spaces.
    content = message.content
    message = ' '.join(content.split())

    # Collect a character count score, omitting spaces.
    character_count = len(message.replace(" ", ""))
    points = 49 * math.pow(2.7, -(math.pow(character_count - 120, 2)/9000)) + 1

    # Collect a set of words.
    words = set(
        [word.lower() for word in message.split(" ") if dictionary.check(word)])
    # Determine the valid words by checking whether they exist in the
    # blocked set.
    valid_words = []
    for word in words:
        is_member = await redis.sismember("blockedwords", word)
        if not is_member:
            valid_words.append(word)

    # Calulate average word length multiplier, carefully preventing division by
    # zero.
    word_lengths = [len(word) for word in valid_words]
    divisor = len(word_lengths) if len(word_lengths) > 0 else 1
    avg_word_length = sum(word_lengths) / divisor
    multiplier = math.pow(avg_word_length - 4.7, 3)/120 + 1

    # Block the new words.
    if valid_words:
        await redis.spop("blockedwords", len(valid_words))
        await redis.sadd("blockedwords", *valid_words)

    # Return the calculated score.
    return int(points * multiplier)


async def set_experience(
        redis: Redis,
        user: User,
        experience: int = None,
        offset: int = 0,
        cooldown: int = 60) -> int:
    """Sets a users experience.

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
    xp_query = f"xp:{user.id}"
    cooldown_query = f"cd:{user.id}"

    # If a flat value was provided, set to that and return.
    if experience:
        await redis.set(xp_query, experience)
        await redis.set(cooldown_query, str(True), expire=cooldown)
        return experience

    # Otherwise, add the provided offset value and return.
    new_experience = await redis.incrby(xp_query, offset)
    await redis.set(cooldown_query, str(True), expire=cooldown)
    return new_experience
