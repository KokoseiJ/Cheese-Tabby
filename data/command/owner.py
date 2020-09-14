# -*- coding: utf-8 -*-

import logging

from discord.ext import commands

from data.lib import img_cache

logger = logging.getLogger()


class Owner(commands.Cog, name="for Bot OWNER"):
    @commands.command(help="Shutdown the bot")
    @commands.is_owner()
    async def close(self, ctx: commands.context):
        await ctx.send(":wave: :cat:")
        await ctx.bot.close()

    @commands.command(help="Delete all images in the cache folder")
    @commands.is_owner()
    async def clear_cache(self, ctx: commands.context):
        logger.info("Removing cached image from cache directory...")

        if len(img_cache.get_cache_list()) == 0:
            logger.info("cache directory is already empty")
            await ctx.send(
                "```\n"
                " - Already empty!"
                "```"
            )
            logger.warning("Already empty!")
        else:
            img_cache.purge_cache()
            await ctx.send(
                "```\n"
                " - Deleted!"
                "```"
            )
