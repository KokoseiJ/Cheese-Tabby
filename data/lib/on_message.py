# -*- coding: utf-8 -*-

import uuid
import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def do_filter(message: discord.message):
    black_item_list = [
        "1", "2", "3",
        "4", "5", "6",
        "7", "8", "9",
        "*", "0", "#",
        " ", ".", ",",
        "!", "?", "-",
        "_", "=", "\n",
    ]

    msg_content = message.content
    for black_item in black_item_list:
        msg_content = msg_content.replace(black_item, "")

    for item in json.load(open("data/cache__filters.json", mode="r", encoding="utf-8")):
        if item.lower() in msg_content.lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat! Used Word: {item} ")

            ct = await core.get()
            used_cache, content = ct[0], ct[1]
            del ct

            if isinstance(content, str):
                await message.channel.send(
                    content=content
                )
            else:
                try:
                    cat_img = await message.channel.send(
                        file=discord.File(
                            fp=content,
                            filename=f"{str(uuid.uuid4())}.png"
                        )
                    )
                except discord.errors.Forbidden:
                    await message.channel.send(
                        "```\nHello?\n"
                        f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                        f"```\n <@{message.guild.owner_id}>"
                    )
                    return

                if len(msg_content.replace(item.lower(), "")) != 0:
                    try:
                        if used_cache is True:
                            await cat_img.add_reaction("❌")
                        else:
                            await cat_img.add_reaction("🇽")
                    except discord.errors.Forbidden:
                        logger.warning("Fail to add emoji...")

            return
