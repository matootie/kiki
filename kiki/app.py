"""
"""

import os
import asyncio
import aioredis
import socket
from starlette.applications import Starlette
from starlette.routing import Route
from starlette.routing import PlainTextResponse

from .utils import load_config
from .kiki import Kiki


async def lifespan(app):
    """Configure application companions

    Run an instance of Kiki bot with the application as well as an active
    connection to Redis for session.
    """

    try:
        token = os.environ["KIKI_TOKEN"]
    except KeyError:
        click.echo("You must specify the bot token under KIKI_TOKEN.")
        exit()

    config = load_config()
    redis_config = config.get("redis")
    if redis_config:
        redis_url = redis_config.get("url", "redis://localhost")
        try:
            app.redis = await aioredis.create_redis_pool(
                redis_url,
                encoding="utf-8")
        except (socket.gaierror, OSError):
            app.redis = None

    kiki = Kiki(config=config)
    app.kiki = kiki
    setattr(kiki, "app", app)

    async def runner():
        try:
            await kiki.start(token)
        finally:
            await kiki.close()

    loop = asyncio.get_event_loop()
    future = asyncio.ensure_future(runner(), loop=loop)

    yield


app = Starlette(lifespan=lifespan)
