# -*- coding: utf-8 -*-

import discord

from data.lib import core


help = "Send the cat"


async def main(message, client):
    content = await core.get()

    if isinstance(content, str):
        await message.channel.send(content=content)
    else:
        try:
            await message.channel.send(file=discord.File(content, 'some_cat.png'))
        except discord.errors.Forbidden:
            await message.channel.send("```\nHello?\n"
                                       f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                                       f"```\n <@{message.guild.owner_id}>")
            return

    return
