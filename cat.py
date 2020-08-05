# -*- coding: utf-8 -*-

import sys
import logging
import subprocess

try:
    import discord
except ModuleNotFoundError:
    print("===< Installing Module >===")
    try:
        subprocess.run(['pip', 'install', 'discord'])
    except OSError:
        subprocess.run(['pip3', 'install', 'discord'])
    print("===========================")

    import discord

try:
    from data.lib import api, filter, guild, log, option, start_page, token
except ModuleNotFoundError:
    print("Fail to load CatBOT library...")
    print(" - PLZ Download again")
    print(" - Download: https://github.com/chick0/CatBOT")
    sys.exit(-1)

##################################################################################
log.create_logger()
logger = logging.getLogger()

option = option.get_option()

filters = filter.get_filter()

client = discord.Client()
bot_token = token.get_token()


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.invite_me(bot=client, permission=35840)
    guild.dump_guild(bot=client, save=option['save_guild_data'])


@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        app = await client.application_info()

        if message.author.id == app.owner.id:
            await message.author.send("Closing CatBOT...")
            await client.close()
        return

    async def get_content():
        try:
            tm_out = int(option['timeout'])
        except ValueError:
            logger.critical("Warning! Timeout option is not integer")
            logger.info("Set timeout to default value [3] ")
            tm_out = 3

        cat_worker = await api.get_data(api_url=option['api_url'],
                                        tm_out=tm_out)

        if cat_worker[0] is False:
            error_img = await api.download(url=f"https://http.cat/{cat_worker[1]}.jpg",
                                           tm_out=tm_out)

            return error_img, "**WARNING! API SERVER ERROR!**"
        elif cat_worker[0] is True:
            return cat_worker[1], None

    if client.user.mentioned_in(message) and str(client.user.id) in message.content:
        app = await client.application_info()

        await message.channel.send("```"
                                   f"Connected to {len(client.guilds)} guilds\n"
                                   f"BOT Owner: {app.owner}"
                                   "```")
        return

    for item in filters:
        if item.lower() in str(message.content).lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat!")

            try:
                content = await get_content()

                if content[1] is not None:
                    await message.channel.send(file=discord.File(content[0], 'some_cat.png'), content=content[1])
                else:
                    await message.channel.send(file=discord.File(content[0], 'some_cat.png'))
            except discord.errors.Forbidden:
                await message.channel.send(f"```\n"
                                           f"{client.user} need [Embed Links] Permission!\n"
                                           f"```")

            return
    return


##################################################################################
# BOT Start
try:
    logger.info("CatBOT Starting...")
    client.run(bot_token)
except discord.errors.LoginFailure:
    logger.critical("**Invalid token loaded!!**")
    token.reset_token()
except Exception as e:
    logger.critical("=" * 30)
    logger.critical("<< Bot is dead >>")
    logger.critical(e)
    logger.critical("=" * 30)
