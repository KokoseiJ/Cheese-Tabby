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
    except Exception as e:
        print(f"Unexpected Error {e.__class__.__name__}!")
        print("Try to user install...")

        try:
            subprocess.run(['pip', 'install', '-r', 'requirements.txt', '--user'])
        except OSError:
            subprocess.run(['pip3', 'install', '-r', 'requirements.txt', '--user'])
    print("===========================")

    import discord

from data.lib import guild, log, start_page, token, cache
from data.static_command import filter_work, mention

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

command_files = os.listdir("data/command/")
for module_file in command_files:
    module = importlib.import_module(f"data.command.{module_file.split('.')[0]}")
    modules[module_file.split('.')[0]] = module

del command_files


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.bot_info(bot=client)
    guild.dump_guild(bot=client)


@client.event
async def on_message(message):
    if message.author.bot:
        return

    if message.content.startswith(option.prefix):
        commands = list(modules.keys())
        for command in commands:
            if message.content.startswith(option.prefix + command):
                await modules[command].main(message, client)

    if client.user.mentioned_in(message) and str(client.user.id) in message.content:
        await mention.main(message, client)
        return

    await filter_work.main(message)
    return


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
