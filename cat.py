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
    print("Fail to load Cat library...")
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

cache = dict()


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.invite_me(bot=client, permission=52288)
    guild.dump_guild(bot=client, save=option['save_guild_data'])


@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        try:
            app = cache['app']
        except KeyError:
            app = await client.application_info()

        if message.author.id == app.owner.id:
            await message.author.send("Closing CatBOT...")
            await client.close()
        return

    if message.content.startswith("hellothisisverification"):
        try:
            app = cache['app']
        except KeyError:
            app = await client.application_info()

        await message.channel.send("```"
                                   f"BOT Owner: {app.owner}"
                                   "```")
        return

    async def get_embed(title: str):
        try:
            tm_out = int(option['timeout'])
        except ValueError:
            logger.critical("Warning! Timeout option is not integer")
            logger.info("Set timeout to default value [3] ")
            tm_out = 3

        cat_url = await api.get_data(api_url=option['api_url'],
                                     json_key=option['json_key'],
                                     tm_out=tm_out)

        if cat_url is None:
            title = f"**WARNING! API SERVER ERROR!**"
            cat_url = "https://http.cat/503"

        embed = discord.Embed(title=f"{title}!",
                              color=option['color'])

        embed.set_image(url=cat_url)
        return embed

    if client.user.mentioned_in(message) and str(client.user.id) in message.content:
        try:
            await message.channel.send(embed=await get_embed(title="It's Me!"))
        except discord.errors.Forbidden:
            await message.channel.send(f"```\n"
                                       f"{client.user} need [Embed Links] Permission!\n"
                                       f"```")
        return

    for item in filters:
        if item.lower() in str(message.content).lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat!")

            try:
                await message.channel.send(embed=await get_embed(title=item))
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
