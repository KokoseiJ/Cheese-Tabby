# -*- coding: utf-8 -*-

import logging

from data.lib import admin, filter

help = None

logger = logging.getLogger()


async def main(message, client):
    if await admin.check(message, client):
        filter.get_filter()
        await message.channel.send("Filter reloaded!")
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.author.send("https://http.cat/403.jpg")

    return
