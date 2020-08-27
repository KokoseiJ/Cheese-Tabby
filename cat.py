# -*- coding: utf-8 -*-

import os
import sys
import logging
import importlib
import subprocess

try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    print("===< Installing Module >===")
    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    except OSError:
        subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])
    print("===========================")

    import discord
    from discord.ext import commands

from data.lib import guild, log, start_page, token, cache
from data.lib import on_message

try:
    import option
except ModuleNotFoundError:
    print("CatBOT Option File is Missing!")
    print(" - Download: https://github.com/chick0/CatBOT/blob/master/option.py")
    sys.exit(-1)

##################################################################################
log.create_logger()
logger = logging.getLogger()

# bot = commands.Bot(command_prefix=option.prefix)
bot = commands.AutoShardedBot(command_prefix=option.prefix)

token_worker = token.Token(file_name="token.json",
                           service="Discord")

bot_token = token_worker.get_token()
del token_worker


##################################################################################
def cache_filter():
    from data.lib import filter
    filter.get_filter()


def load_command():
    for module_file in os.listdir("data/command/"):
        module = importlib.import_module(f"data.command.{module_file.split('.')[0]}")

        for mod in dir(module):
            if not mod.startswith("__"):
                if "Cog" in getattr(module, mod).__class__.__name__:
                    logger.info(f"Command Detected from '{module.__name__}' name '{mod}'")
                    try:
                        bot.add_cog(getattr(module, mod)(bot))
                        logger.info("OK! - Cogs Registered")
                    except Exception as moduleLoad_error:
                        logger.critical(f"FAIL! - {moduleLoad_error.__class__.__name__}:"
                                        f" {moduleLoad_error}")


cache_filter(), load_command()


##################################################################################
@bot.event
async def on_ready():
    await start_page.set_status(bot, "idle", "watching", "Cat")
    start_page.bot_info(bot=bot)
    guild.dump_guild(bot=bot)


@bot.listen(name="on_message")
async def filter_work(message):
    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        return

    await on_message.do_filter(message=message)


@bot.event
async def on_raw_reaction_add(payload):
    await bot.fetch_channel(channel_id=payload.channel_id)
    channel = await bot.fetch_channel(channel_id=payload.channel_id)
    message = await channel.fetch_message(id=payload.message_id)

    if message.author.id == bot.user.id and payload.user_id != bot.user.id:
        x_emoji = [
            "🇽", "❌"
        ]

        if payload.emoji.name in x_emoji:
            logger.info(f"Emoji added! Removing Image...")

            try:
                await message.delete()
            except discord.errors.NotFound:
                logger.error("Failed to delete image... I think it's already deleted.")
            except (discord.errors.HTTPException, Exception):
                logger.error("Failed to delete image... But just ignore it.")


##################################################################################
# BOT Start
try:
    logger.info("CatBOT Starting...")
    bot.run(bot_token)
except discord.errors.LoginFailure:
    logger.critical("**Invalid token loaded!!**")

    token_worker = token.Token(file_name="token.json",
                               service="Discord")

    token_worker.reset_token()
    del bot_token
except Exception as botStart_error:
    logger.critical("--------<< Bot is dead >>--------")
    logger.critical(f"{botStart_error.__class__.__name__}:"
                    f" {botStart_error}")
finally:
    cache.run()
