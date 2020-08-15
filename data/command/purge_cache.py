# -*- coding: utf-8 -*-

import logging

from data.lib import admin, cat_cache

help = None

logger = logging.getLogger()


async def main(message, client):
    if await admin.check(message, client):
        logger.info("Removing cat image from 'cat_cache'...")

        cc = len(cat_cache.get_cache_list())
        logger.info(f"'{cc}' detected")
        await message.channel.send(f"```\n{cc} => 0\n```")

        if cc == 0:
            logger.info("'cat_cache' is already empty")
        else:
            cat_cache.purge_cache()
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.channel.send(":cat: ?")

    return
