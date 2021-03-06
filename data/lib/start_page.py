# -*- coding: utf-8 -*-

import logging

import discord

from data.lib import invite

logger = logging.getLogger()


def get_status(option: str):
    if option == "idle":
        return discord.Status.idle
    elif option == "dnd":
        return discord.Status.dnd
    elif option == "online":
        return discord.Status.online
    elif option == "offline":
        return discord.Status.offline
    else:
        return discord.Status.online


def get_type(option: str):
    if option == "playing":
        return discord.ActivityType.playing
    elif option == "streaming":
        return discord.ActivityType.streaming
    elif option == "listening":
        return discord.ActivityType.listening
    elif option == "watching":
        return discord.ActivityType.watching
    else:
        return discord.ActivityType.unknown


async def set_status(bot, status: str, activity: str, name: str):
    await bot.change_presence(
        status=get_status(status),
        activity=discord.Activity(
            type=get_type(activity),
            name=name
        )
    )


def bot_info(bot):
    logger.info("-" * 50)
    logger.info(f" - BOT Login -> {bot.user}")
    logger.info(f" - Connected to ( {len(bot.guilds)} ) guilds!")
    logger.info("-" * 50)
    logger.info(f" - Invite bot: {invite.get_link(bot)}")
    logger.info("-" * 50)
