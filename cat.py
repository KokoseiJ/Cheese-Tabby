# -*- coding: utf-8 -*-

import os
import sys
import logging
import importlib
import subprocess

try:
    import discord
except ModuleNotFoundError:
    print("===< Installing Module >===")
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    except OSError:
        subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])
    print("===========================")

    import discord

from data.lib import guild, log, start_page, token, cache
from data.static_command import filter_work

try:
    import option
except ModuleNotFoundError:
    print("CatBOT Option File is Missing!")
    print(" - Download: https://github.com/chick0/CatBOT/blob/master/option.py")
    sys.exit(-1)

##################################################################################
log.create_logger()
logger = logging.getLogger()

client = discord.Client()

token_worker = token.Token(file_name="token.json",
                           service="Discord")
bot_token = token_worker.get_token()
del token_worker


def cache_filter():
    from data.lib import filter
    filter.get_filter()


cache_filter()


##################################################################################
modules = dict()

logger.info("Loading Command Module...")
command_files = os.listdir("data/command/")
for module_file in command_files:
    if not module_file.startswith("__"):
        try:
            module = importlib.import_module(f"data.command.{module_file.split('.')[0]}")

            if module.__getattribute__("main"):
                modules[module_file.split('.')[0]] = module
                logger.info(f"Loaded Command '{module_file.split('.')[0]}' from {module_file}")
        except (AttributeError, Exception):
            logger.critical(f"Fail to load Command from '{module_file}'")

logger.info("Command Module Loaded!")
logger.info("<< Command Module Information >>")
logger.info(f" - {len(modules.keys())} commands")
logger.info(f" - Commands: {list(modules.keys())}")
del command_files


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.bot_info(bot=client)
    guild.dump_guild(bot=client)


@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        return

    if message.content.startswith(option.prefix):
        commands = list(modules.keys())
        for command in commands:
            if message.content.startswith(option.prefix + command):
                logger.info(f"[{message.author.id}]{message.author} use command '{command}'")
                await modules[command].main(message, client)
                return

    await filter_work.main(message)
    return


@client.event
async def on_raw_reaction_add(payload):
    await client.fetch_channel(channel_id=payload.channel_id)
    channel = await client.fetch_channel(channel_id=payload.channel_id)
    message = await channel.fetch_message(id=payload.message_id)
    if message.author.id == client.user.id and payload.user_id != client.user.id:
        x_emoji = [":regional_indicator_x:", "\U0001F1FD"]
        if payload.emoji.name in x_emoji:
            await message.delete()


##################################################################################
# BOT Start
try:
    logger.info("CatBOT Starting...")
    client.run(bot_token)
except discord.errors.LoginFailure:
    logger.critical("**Invalid token loaded!!**")

    token_worker = token.Token(file_name="token.json",
                               service="Discord")
    bot_token = token_worker.reset_token()
    del bot_token
except Exception as e:
    logger.critical("=" * 30)
    logger.critical("<< Bot is dead >>")
    logger.critical(e)
    logger.critical("=" * 30)

cache.run()
