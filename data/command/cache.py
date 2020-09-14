# -*- coding: utf-8 -*-

import logging

import discord
from discord.ext import commands

from data.lib import img_cache

logger = logging.getLogger()


class Cache(commands.Cog, name="Cache control"):
    @commands.command(help="Check status")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cache(self, ctx: commands.context):
        from data.lib import img_cache
        from option import cache_limit

        await ctx.send(
            "```\n"
            f" - Cached Image: {len(img_cache.get_cache_list())}\n"
            f" - Cache Limit: {cache_limit}\n"
            f" - Cache Size: {round(img_cache.get_cache_size() / (1000 * 1000), 2)} MB\n"
            "```"
        )

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

    @commands.command(help="Send random image or select it")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def send(self, ctx: commands.context, cache_id: str = None):
        from data.lib import img_cache

        if cache_id is None:
            content, cat_id = await img_cache.get_img_random(
                return_with_cache_id=True
            )

            if content is False:
                await ctx.send(
                    "```\n"
                    " - Cache is EMPTY!\n"
                    "```"
                )
            else:
                await ctx.send(
                    file=discord.File(
                        fp=content,
                        filename=f"{cat_id}.png"
                    )
                )
        else:
            content = await img_cache.get_image_by_id(
                cache_id=cache_id
            )

            if content is False:
                await ctx.send(
                    "```\n"
                    " - Cache Not Found!\n"
                    "```"
                )
            else:
                await ctx.send(
                    file=discord.File(
                        fp=content,
                        filename=f"{cache_id}.png"
                    )
                )
