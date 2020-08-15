# -*- coding: utf-8 -*-

import json

import option
from data.lib import cat_cache

from option import prefix

help = "Check {{bot}}'s Information"


async def main(message, client):
    app = await client.application_info()
    filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))

    await message.channel.send("``\n`"
                               f"Connected to {len(client.guilds)} guilds\n"
                               f"BOT Owner: {app.owner}\n\n"
                               f"Filter words: {len(filters)}\n  -> use '{prefix}filter' command to check it!"
                               "```")
    if message.author.id == app.owner.id:
        await message.channel.send("```\n"
                                   f"Cached Cat: {len(cat_cache.get_cache_list())}\n"
                                   f"Cache Limit: {option.cache_limit}\n"
                                   f"Cache Size: {round(cat_cache.get_cache_size() / (1024 * 1024), 2)} MB\n"
                                   "```")
