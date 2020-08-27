# -*- coding: utf-8 -*-

import logging

import discord
from discord.ext import commands

from data.lib import img_cache, filter

logger = logging.getLogger()


def is_public(ctx):
    return not isinstance(ctx.message.channel, discord.abc.PrivateChannel)


class ownerCommand(commands.Cog, name="owner ONLY"):
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
            filter.get_filter()
            await ctx.send("Filter reloaded!")
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete the same pictures")
    @commands.check(is_public)
    async def purge(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            before = len(img_cache.get_cache_list())
            img_cache.purge_same()
            after = len(img_cache.get_cache_list())

            await ctx.send(f"{before} => {after}")
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete all pictures")
    @commands.check(is_public)
    async def purge_all(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            logger.info("Removing cat image from 'cat_cache'...")

            cc = len(img_cache.get_cache_list())
            logger.info(f"'{cc}' detected")
            await ctx.send("```\n"
                           f"{cc} => 0\n"
                           "```")

            if cc == 0:
                logger.info("'cat_cache' is already empty")
            else:
                img_cache.purge_cache()
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")
