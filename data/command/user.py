# -*- coding: utf-8 -*-

import json

import discord
from discord.ext import commands

from data.lib import filter_load, img_cache, invite
import option


def is_public(ctx: commands.context):
    return not isinstance(
        ctx.message.channel,
        discord.abc.PrivateChannel
    )


class Everyone(commands.Cog, name="for @everyone"):
    @commands.command(help="Check information about the bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def me(self, ctx: commands.context):
        filters = json.load(
            open(
                "data/cache__filters.json",
                mode="r",
                encoding="utf-8"
            )
        )

        await ctx.send(
            "```\n"
            f" - Connected to {len(ctx.bot.guilds)} guilds\n"
            f" - Filter words: {len(filters)}\n"
            "```"
        )

    @commands.command(help="Send Bot Invite link to you")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: commands.context):
        if is_public(ctx=ctx):
            await ctx.send(
                "```\n"
                " - Check your Private Message!\n"
                "```"
            )

        embed = discord.Embed(
            title="Invite Me!",
            color=0xFF933A,
            description="Please Click me!",
            url=invite.get_link(ctx.bot)
        )

        try:
            await ctx.author.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send(
                "```\n"
                " - Fail to send Private Message..."
                "```",
                embed=embed
            )

    @commands.command(help="Check filter words")
    @commands.cooldown(1, 50, commands.BucketType.user)
    @commands.check(is_public)
    async def filter(self, ctx: commands.context):
        if await ctx.bot.is_owner(user=ctx.author):
            filter_load.get()

        filters = json.load(
            open(
                "data/cache__filters.json",
                mode="r",
                encoding="utf-8"
            )
        )

        await ctx.send(
            "```\n"
            f" - {ctx.bot.user}'s filter information!\n"
            f" - {len(filters)} words\n"
            "```"
        )

    @commands.command(help="Check cache information")
    @commands.cooldown(1, 10, commands.BucketType.user)
    async def cache(self, ctx: commands.context):
        await ctx.send(
            "```\n"
            f" - Cached Image: {len(img_cache.get_cache_list())}\n"
            f" - Cache Limit: {option.cache_limit}\n"
            f" - Cache Size: {round(img_cache.get_cache_size() / (1000 * 1000), 2)} MB\n"
            "```"
        )

    @commands.command(help="Send random image from cache")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(is_public)
    async def send(self, ctx: commands.context, cache_id: str = None):
        if cache_id is None:
            content, cat_id = await img_cache.get_cat_random(
                return_with_cat_id=True
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
            content = await img_cache.get_cat_by_id(
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
