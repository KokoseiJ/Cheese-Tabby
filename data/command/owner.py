# -*- coding: utf-8 -*-

import logging

from discord.ext import commands

from data.lib import img_cache, filter_load

logger = logging.getLogger()


class Owner(commands.Cog, name="for Bot OWNER"):
    @commands.command(help="Shutdown the bot")
    @commands.is_owner()
    async def close(self, ctx: commands.context):
        if await ctx.bot.is_owner(user=ctx.author):
            await ctx.send(":wave:")
            await ctx.bot.close()
        else:
            logger.warning(f"[{ctx.author.id}]{ctx.author} try to use owner command")
            await ctx.send("?")

    @commands.command(help="Delete the same cached image")
    @commands.is_owner()
    async def purge(self, ctx: commands.context):
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
            await ctx.send("?")

    @commands.command(help="Delete all cached images")
    @commands.is_owner()
    async def clean(self, ctx: commands.context):
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
            await ctx.send("?")
