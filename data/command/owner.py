# -*- coding: utf-8 -*-

import logging

import discord
from discord.ext import commands

from data.lib import cat_cache, filter
import option

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

    @commands.command(help="Check cache information")
    @commands.check(is_public)
    async def cache(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            await ctx.send("```\n"
                           f"Cached Cat: {len(cat_cache.get_cache_list())}\n"
                           f"Cache Limit: {option.cache_limit}\n"
                           f"Cache Size: {round(cat_cache.get_cache_size() / (1024 * 1024), 2)} MB\n"
                           "```")
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete the same pictures")
    @commands.check(is_public)
    async def purge(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            before = len(cat_cache.get_cache_list())
            cat_cache.purge_same()
            after = len(cat_cache.get_cache_list())

            await ctx.send(f"{before} => {after}")
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")

    @commands.command(help="Delete all pictures")
    @commands.check(is_public)
    async def purge_all(self, ctx):
        if await ctx.bot.is_owner(user=ctx.author):
            logger.info("Removing cat image from 'cat_cache'...")

            cc = len(cat_cache.get_cache_list())
            logger.info(f"'{cc}' detected")
            await ctx.send(f"```\n{cc} => 0\n```")

            if cc == 0:
                logger.info("'cat_cache' is already empty")
            else:
                cat_cache.purge_cache()
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")
