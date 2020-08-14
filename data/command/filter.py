# -*- coding: utf-8 -*-

import io
import json

import discord

help = "Check {{bot}}'s cat filter"


async def main(message, client):
    filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))
    await message.channel.send("```\nCheck your Private Message\n```")

    try:
        await message.author.send(f"{client.user}'s filter information!\n - {len(filters)} words")

        result = ""
        for f in filters:
            result += f"- {f}\n"

        result = io.BytesIO(result.encode("utf-8"))
        await message.author.send(file=discord.File(result, "filter.txt"))
    except discord.errors.Forbidden:
        pass

    return
