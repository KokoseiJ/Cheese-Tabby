# -*- coding: utf-8 -*-

import logging

import discord

import data.lib.log as log
import data.lib.token as token

import data.lib.api as api
import data.lib.filter as cat_filter

import data.lib.guild as guild
import data.lib.option as option_loader
import data.lib.start_page as start_page


##################################################################################
log.create_logger()
logger = logging.getLogger()

option = option_loader.get_option()
filters = cat_filter.get_filter()

client = discord.Client()
bot_token = token.get_token()


##################################################################################
@client.event
async def on_ready():
    await start_page.set_status(client, "idle", "watching", "Cat")
    start_page.invite_me(bot=client, permission=52288)
    guild.dump_guild(bot=client, save=option['save_guild_data'])


@client.event
async def on_message(message):
    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        return

    if "hellothisisverification" in message.content:
        app = await client.application_info()
        await message.channel.send("```"
                                   f"Owner: {app.owner}"
                                   "```")
        return

    for item in filters:
        if item.lower() in str(message.content).lower():
            logger.info(f"[{message.author.id}]{message.author} Called the Cat!")

            cat_url = await api.get_data(api_url=option['api_url'],
                                         json_key=option['json_key'])

            embed = discord.Embed(title=f"{item}!", color=option['color'])
            embed.set_image(url=cat_url)
            await message.channel.send(embed=embed)


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
