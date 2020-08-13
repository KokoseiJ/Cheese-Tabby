# -*- coding: utf-8 -*-

import json
import logging

import option
from data.lib import cat_cache


logger = logging.getLogger()


async def main(message, client):
    app = await client.application_info()
    filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))

    await message.channel.send("```"
                               f"Connected to {len(client.guilds)} guilds\n"
                               f"BOT Owner: {app.owner}\n\n"
                               f"Filter words: {len(filters)}\n"
                               "```")
    if message.author.id == app.owner.id:
        await message.channel.send("```"
                                   f"Cached Cat: {len(cat_cache.get_cache_list())}\n"
                                   f"Cache Limit: {option.cache_limit}\n"
                                   f"Cache Size: {cat_cache.get_cache_size()} B\n"
                                   "```")