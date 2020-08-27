# -*- coding: utf-8 -*-

import logging

import discord
from discord.ext import commands

from data.lib import img_cache, filter

logger = logging.getLogger()


def is_public(ctx):
    return not isinstance(ctx.message.channel, discord.abc.PrivateChannel)


class ownerCommand(commands.Cog, name="for Bot OWNER"):
    @commands.command(help="Shutdown the bot")
    @commands.check(is_public)
    async def close(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            await ctx.send(":wave:")
            await ctx.bot.close()
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Reload the Filter Words")
    @commands.check(is_public)
    async def reload(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            await ctx.send(
                "```\n"
                f" - {ctx.bot.user}'s filter information!\n"
                f" - {len(filter.get_filter())} words\n"
                "```"
            )
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete the same cached image")
    @commands.check(is_public)
    async def purge(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            before = len(img_cache.get_cache_list())
            await img_cache.purge_same()
            after = len(img_cache.get_cache_list())

            await ctx.send(
                "```\n"
                f" - {before - after} Deleted!"
                "```"
            )
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete all cached images")
    @commands.check(is_public)
    async def purge_all(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            logger.info("Removing cached image from cache directory...")

            cc = len(img_cache.get_cache_list())
            logger.info(f"'{cc}' detected")

            if cc == 0:
                logger.info("cache directory is already empty")
                await ctx.send(
                    "```\n"
                    " - Already empty!"
                    "```"
                )
            else:
                img_cache.purge_cache()
                await ctx.send(
                    "```\n"
                    f" - {cc} Deleted!"
                    "```"
                )
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")
