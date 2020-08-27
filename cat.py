# -*- coding: utf-8 -*-

# Test Discord Module
try:
    import discord
    from discord.ext import commands
except ModuleNotFoundError:
    # Try to install
    import subprocess

    try:
        subprocess.run(['pip', 'install', '-r', 'requirements.txt'])
    except OSError:
        subprocess.run(['pip3', 'install', '-r', 'requirements.txt'])

    try:
        import discord
        from discord.ext import commands
    except ModuleNotFoundError:
        import sys

        print("Module installation failed...")
        print("Please check the 'requirements.txt' and install it!")

        sys.exit(-1)


# Need to Before Setting
def create_logger():
    import logging
    from data.lib import log
    log.create_logger()

    return logging.getLogger()


logger = create_logger()


def set_bot():
    try:
        import option
    except ModuleNotFoundError:
        print("CatBOT Option File is Missing!")
        print(" - Download: https://github.com/chick0/CatBOT/blob/master/option.py")
        sys.exit(-2)

    if option.use_Auto_shard is True:
        return commands.AutoShardedBot(command_prefix=option.prefix)
    else:
        return commands.Bot(command_prefix=option.prefix)


def cache_filter():
    from data.lib import filter
    filter.get_filter()


bot = set_bot()
cache_filter()


# Import Command Modules
def load_command():
    import os
    import importlib

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


load_command()


# Bot Event Method
@bot.event
async def on_command(ctx):
    if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
        logger.info(f"[{ctx.author.id}]{ctx.author} use [{ctx.message.content}] command at [PrivateChannel]")
    else:
        logger.info(f"[{ctx.author.id}]{ctx.author} use [{ctx.message.content}] command at [{ctx.guild.id}]")


@bot.event
async def on_command_error(ctx, error):
    if isinstance(error, discord.ext.commands.errors.CommandOnCooldown):
        await ctx.send(f"```\n"
                       f"{error}\n"
                       f"``` - <@{ctx.author.id}>")
        return

    if isinstance(error, discord.ext.commands.errors.CommandNotFound):
        return

    if isinstance(ctx.message.channel, discord.abc.PrivateChannel):
        logger.info(f"[{ctx.author.id}]{ctx.author} meet the '{error.__class__.__name__}' error at [PrivateChannel]")
    else:
        logger.info(f"[{ctx.author.id}]{ctx.author} meet the '{error.__class__.__name__}' error at [{ctx.guild.id}]")


@bot.event
async def on_ready():
    from data.lib import start_page
    from option import presence

    await start_page.set_status(
        bot=bot,
        status=presence.status,
        activity=presence.activity,
        name=presence.name
    )
    start_page.bot_info(
        bot=bot
    )


@bot.listen(name="on_message")
async def filter_work(message):
    from data.lib import on_message

    if message.author.bot or isinstance(message.channel, discord.abc.PrivateChannel):
        return

    await on_message.do_filter(
        message=message
    )


@bot.listen(name="on_raw_reaction_add")
async def image_delete(payload):
    from data.lib import on_raw_reaction_add

    await on_raw_reaction_add.check_delete(
        payload=payload,
        bot=bot
    )


# Load Bot Token
def bot_token(reset=False):
    from data.lib import token

    token_worker = token.Token(
        file_name="token.json",
        service="Discord"
    )

    if reset is True:
        token_worker.reset_token()
    else:
        return token_worker.get_token()


# BOT Start
try:
    logger.info("CatBOT Starting...")
    bot.run(bot_token())
except discord.errors.LoginFailure:
    logger.critical("**Invalid token loaded!!**")
    bot_token(
        reset=True
    )
except Exception as botStart_error:
    logger.critical("--------<< Bot is dead >>--------")
    logger.critical(f"{botStart_error.__class__.__name__}:"
                    f" {botStart_error}")
finally:
    from data.lib import cache

    cache.run()
