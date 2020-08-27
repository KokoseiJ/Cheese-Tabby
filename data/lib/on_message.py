# -*- coding: utf-8 -*-

import uuid
import json
import logging

import discord

from data.lib import core

logger = logging.getLogger()


async def do_filter(message: discord.message):
    msg_content = message.content
    for black_item in [" ", ".", ",", "!", "?", "-", "_", "\n"]:
        msg_content = msg_content.replace(black_item, "")

    for item in json.load(open("data/cache__filters.json", mode="r", encoding="utf-8")):
        if item.lower() in msg_content.lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat! Used Word: {item} ")

            content = await core.get()

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

                if len(item.lower()) is not len(msg_content):
                    try:
                        await cat_img.add_reaction("🇽")
                    except discord.errors.Forbidden:
                        logger.warning("Fail to add emoji...")

            return
