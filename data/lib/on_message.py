# -*- coding: utf-8 -*-

import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def public(message: discord.message):
    def open_it(filename: str):
        return open(
            file=filename,
            mode="r",
            encoding="utf-8"
        )

    msg_content = message.content
    for block_item in json.load(open_it(filename="data/cache__block_words.json")):
        msg_content = msg_content.replace(block_item, "")

    for item in json.load(open_it(filename="data/cache__filters.json")):
        if item.lower() in msg_content.lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat! Used Word: {item} ")

            cat_img, cat_id, msg = await core.work()

            if cat_img is None:
                await message.channel.send(
                    content=msg
                )
            else:
                try:
                    try_send_cat = await message.channel.send(
                        file=discord.File(
                            fp=cat_img,
                            filename=f"{cat_id}.png"
                        )
                    )
                except discord.errors.Forbidden:
                    await message.channel.send(
                        "```\n"
                        "Hello?\n"
                        f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                        f"``` <@{message.guild.owner_id}>"
                    )
                    return

                if len(msg_content.replace(item.lower(), "")) != 0:
                    try:
                        await try_send_cat.add_reaction("❌")
                    except discord.errors.Forbidden:
                        logger.warning("Fail to add emoji...")

            return
