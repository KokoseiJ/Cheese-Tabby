# -*- coding: utf-8 -*-

import logging

from data.lib import admin

help = None

logger = logging.getLogger()


async def main(message, client):
    if await admin.check(message, client):
        logger.info(f"Closed bot by {message.author}")

        await message.channel.send(":wave:")
        await client.close()
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.author.send("https://http.cat/403.jpg")

    return
