# -*- coding: utf-8 -*-

import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def add_emoji(message: discord.message):
    try:
        await message.add_reaction("❌")
    except discord.errors.Forbidden:
        logger.warning("Fail to add emoji...")


async def public(message: discord.message):
    def open_it(filename: str):
        return open(
            file=filename,
            mode="r",
            encoding="utf-8"
        )

    msg_content = message.content
    for block_item in json.load(open_it(filename="data/cache__remove_words.json")):
        msg_content = msg_content.replace(block_item, "")

    for item in json.load(open_it(filename="data/cache__filters.json")):
        if item.lower() in msg_content.lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat! Used Word: {item} ")

            image, cache_id, msg = await core.work()

            if image is None:
                await message.channel.send(
                    content=msg
                )
            else:
                try:
                    await message.channel.send(
                        file=discord.File(
                            fp=image,
                            filename=f"{cache_id}.png"
                        )
                    )
                except discord.errors.Forbidden:
                    await message.channel.send(
                        "```\n"
                        "Hello?\n"
                        f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                        f"``` <@{message.guild.owner_id}>"
                    )

                if msg == "from api":
                    await core.save_cache(
                        image=image
                    )

            return
