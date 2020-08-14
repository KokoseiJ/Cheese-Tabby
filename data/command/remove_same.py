# -*- coding: utf-8 -*-

import logging

from data.lib import cat_cache

logger = logging.getLogger()


async def main(message, client):
    app = await client.application_info()
    if app.owner.id == message.author.id:
        before = len(cat_cache.get_cache_list())
        cat_cache.purge_same()
        after = len(cat_cache.get_cache_list())

        await message.channel.send(f"{before} => {after}")
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.channel.send(":cat: ?")

    return
