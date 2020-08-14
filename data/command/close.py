# -*- coding: utf-8 -*-

import logging

help = None

logger = logging.getLogger()


async def main(message, client):
    app = await client.application_info()
    if app.owner.id == message.author.id:
        logger.info(f"Closed bot by {message.author}")

        await message.channel.send(":wave:")
        await client.close()
    else:
        logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
        await message.author.send("https://http.cat/403.jpg")

    return
