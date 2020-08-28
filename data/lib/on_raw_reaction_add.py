# -*- coding: utf-8 -*-

import logging

import discord

logger = logging.getLogger()


async def check_delete(payload, bot):
    await bot.fetch_channel(
        channel_id=payload.channel_id
    )

    channel = await bot.fetch_channel(
        channel_id=payload.channel_id
    )

    message = await channel.fetch_message(
        id=payload.message_id
    )

    if message.author.id == bot.user.id and payload.user_id != bot.user.id:
        x_emoji = [
            "🇽", "❌"
        ]

        if payload.emoji.name in x_emoji:
            logger.info(f"Emoji added! Removing Message...")

            try:
                await message.delete()
            except discord.errors.NotFound:
                logger.error("Failed to delete image... I think it's already deleted.")
            except (discord.errors.HTTPException, Exception):
                logger.error("Failed to delete image... But just ignore it.")
