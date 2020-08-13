# -*- coding: utf-8 -*-

import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def main(message):
    for item in json.load(open("data/cache__filters.json", mode="r", encoding="utf-8")):
        if item.lower() in str(message.content).lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat using '{item}'")
            logger.info(f"Original Text: {message.content}")

            try:
                content = await core.get()

                if isinstance(content, str):
                    await message.channel.send(content=content)
                else:
                    await message.channel.send(file=discord.File(content, 'some_cat.png'))
            except discord.errors.Forbidden:
                await message.channel.send("```\nHello?\n"
                                           f"This bot need [Attach Files] Permission!!\n"
                                           f"```\n <@{message.guild.owner_id}>")
