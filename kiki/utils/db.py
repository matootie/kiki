"""
Database utilities.
"""

import os

from redis import Redis
from redis.exceptions import ConnectionError


def get_db(
        host=os.environ.get("REDIS_HOST", "localhost"),
        port=os.environ.get("REDIS_PORT", "6379"),
        db=os.environ.get("REDIS_DB", "0"),
        password=os.environ.get("REDIS_PASS", None),
        decode_responses=True):
    """
    Get a connection to the database.
    """

    redis = Redis(
        host=host,
        port=port,
        db=db,
        password=password,
        decode_responses=decode_responses)

    try:
        redis.info(section="stats")
    except (ConnectionError):
        return None

    return redis
