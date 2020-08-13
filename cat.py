# -*- coding: utf-8 -*-

import sys
import logging
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
from data.lib import filter, invite

from data.static_command import direct, filter_work, mention

from data.command import help, invite, purge_cache

try:
    import option
except ModuleNotFoundError:
    print("CatBOT Option File is Missing!")
    print(" - Download: https://github.com/chick0/CatBOT/blob/master/option.py")
    sys.exit(-1)

##################################################################################
log.create_logger()
logger = logging.getLogger()

filter.get_filter()

client = discord.Client()

token_worker = token.Token(file_name="token.json",
                           service="Discord")
bot_token = token_worker.get_token()
del token_worker


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

    if isinstance(message.channel, discord.abc.PrivateChannel):
        await direct.main(message, client)
        return

    if message.content.startswith(option.prefix):
        if message.content.startswith(option.prefix + "help"):
            await help.main(message, client)

        if message.content.startswith(option.prefix + "invite"):
            await invite.main(message, client)

        if message.content.startswith(option.prefix + "purge_cache"):
            await purge_cache.main(message, client)

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
