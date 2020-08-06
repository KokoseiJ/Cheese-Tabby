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

from data.lib import guild, log, start_page, token
from data.lib import api, filter, cat_cache

try:
    import option
except ModuleNotFoundError:
    print("CatBOT Option File is Missing!")
    print(" - Download: https://github.com/chick0/CatBOT/blob/master/option.py")
    sys.exit(-1)

##################################################################################
log.create_logger()
logger = logging.getLogger()

filters = filter.get_filter()
cat_cache.check_dir()

client = discord.Client()

token_worker = token.Token(file_name="token.json",
                           service="Discord")
bot_token = token_worker.get_token()
del token_worker


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.invite_me(bot=client, permission=35840)
    guild.dump_guild(bot=client)


@client.event
async def on_message(message):
    if message.author.bot is True:
        return

    if isinstance(message.channel, discord.abc.PrivateChannel):
        app = await client.application_info()

        if message.author.id == app.owner.id:
            await message.author.send("Closing CatBOT...")
            await client.close()
        else:
            await message.author.send("https://http.cat/403.jpg")
        return

    async def get_content():
        try:
            tm_out = int(option.timeout)
        except ValueError:
            logger.critical("Warning! Timeout option is not integer")
            logger.info("Set timeout to default value [3] ")
            tm_out = 3

        cat_worker = await api.get_data(api_url=option.api_url,
                                        tm_out=tm_out)

        if cat_worker[0] is False:
            logging.info("Try to use Cat Cache...")
            if len(cat_cache.get_cache_list()) == 0:
                logging.warning("'cat_cache' is EMPTY!")
                logging.warning("Send Error Message!")
                return f"**WARNING! API SERVER ERROR!**\n - {cat_worker[1]}"
            else:
                return await cat_cache.get_cat_random()
        elif cat_worker[0] is True:
            if option.cache_limit > len(cat_cache.get_cache_list()):
                logger.info("Adding Cat to 'cat_cache'...")
                await cat_cache.save_cat(cat_worker[1])
            else:
                logger.info("Cache is full!")
                if option.replace_on_limit is True:
                    logger.info("Replace option is enabled!")
                    logger.info("Adding Cat to 'cat_cache'...")
                    await cat_cache.replace_cat(cat_worker[1])
                pass

            return cat_worker[1]

    if message.content[0] == option.prefix:
        if message.content.startswith(option.prefix + "help"):
            with open("help_msg.txt", mode='r') as worker:
                help_msg = worker.read()

            help_msg = help_msg.replace("{{prefix}}", option.prefix)
            await message.channel.send("```\n" + help_msg + "\n```")

        if message.content.startswith(option.prefix + "purge_cache"):
            app = await client.application_info()
            if app.owner.id == message.author.id:
                logger.info("Removing cat image from 'cat_cache'...")

                cc = len(cat_cache.get_cache_list())
                logger.info(f"'{cc}' detected")
                if cc == 0:
                    logger.info("'cat_cache' is already empty")
                else:
                    cat_cache.purge_cache()
            else:
                logger.info(f"[{message.author.id}]{message.author} try to use admin command!")
                await message.channel.send(":cat:")
            return

    if client.user.mentioned_in(message) and str(client.user.id) in message.content:
        app = await client.application_info()

        await message.channel.send("```"
                                   f"Connected to {len(client.guilds)} guilds\n"
                                   f"BOT Owner: {app.owner}\n\n"
                                   f"Cached Cat: {len(cat_cache.get_cache_list())}\n"
                                   f"Cache Limit: {option.cache_limit}\n\n"
                                   f"Filter words: {len(filters)}\n"
                                   "```")
        return

    for item in filters:
        if item.lower() in str(message.content).lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat using '{item}'")
            logger.info(f"Original Text: {message.content}")

            try:
                content = await get_content()

                if isinstance(content, str):
                    await message.channel.send(content=content)
                else:
                    await message.channel.send(file=discord.File(content, 'some_cat.png'))
            except discord.errors.Forbidden:
                await message.channel.send("```\nHello?\n"
                                           f"{client.user} need [Attach Files] Permission!!\n"
                                           f"```\n <@{message.guild.owner_id}>")

            return
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
