# -*- coding: utf-8 -*-

import logging

logger = logging.getLogger()


async def main(message, client):
    app = await client.application_info()

    if message.author.id == app.owner.id:
        await message.author.send("Closing CatBOT...")
        await client.close()
    else:
        await message.author.send("https://http.cat/403.jpg")
    return