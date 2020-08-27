# -*- coding: utf-8 -*-

import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def main(message):
    for item in json.load(open("data/cache__filters.json", mode="r", encoding="utf-8")):
        if item.lower() in str(message.content).replace(" ", "").lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat! Used Words: {item} ")

            content = await core.get()

            if isinstance(content, str):
                await message.channel.send(content=content)
            else:
                try:
                    cat_img = await message.channel.send(file=discord.File(content, 'some_cat.png'))
                except discord.errors.Forbidden:
                    await message.channel.send("```\nHello?\n"
                                               f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                                               f"```\n <@{message.guild.owner_id}>")
                    return

                if len(item.lower()) is not len(message.content):
                    try:
                        await cat_img.add_reaction("\U0001F1FD")
                    except discord.errors.Forbidden:
                        pass

            return