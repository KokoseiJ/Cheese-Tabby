# -*- coding: utf-8 -*-

import discord

from data.lib import invite


async def main(message, client):
    await message.channel.send("```\nCheck your Private Message\n```")

    embed = discord.Embed(title="Invite Me!", color=16579836,
                          description="Please Click me!",
                          url=invite.get_link(client))
    try:
        await message.author.send(embed=embed)
    except discord.errors.Forbidden:
        pass

    return
