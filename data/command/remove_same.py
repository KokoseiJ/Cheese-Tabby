# -*- coding: utf-8 -*-

import logging

from data.lib import admin, cat_cache

help = None

logger = logging.getLogger()


async def main(message, client):
    if await admin.check(message, client):
        before = len(cat_cache.get_cache_list())
        cat_cache.purge_same()
        after = len(cat_cache.get_cache_list())

        await message.channel.send(f"{before} => {after}")
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.channel.send(":cat: ?")

    return
