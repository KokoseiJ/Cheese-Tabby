# -*- coding: utf-8 -*-

import json

import discord

help = "Check {{bot}}'s cat filter"


async def main(message, client):
    filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))
    await message.channel.send("```\nCheck your Private Message\n```")

    try:
        await message.author.send(f"{client.user}'s filter information!\n - {len(filters)} words")
        for f in filters:
            await message.author.send(f"- {f}")
    except discord.errors.Forbidden:
        pass

    return
