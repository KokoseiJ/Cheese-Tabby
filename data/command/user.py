# -*- coding: utf-8 -*-

import io
import uuid
import json

import discord
from discord.ext import commands

from data.lib import img_cache, invite
import option


def is_public(ctx):
    return not isinstance(
        ctx.message.channel,
        discord.abc.PrivateChannel
    )


class userCommand(commands.Cog, name="for @everyone"):
    @commands.command(help="Check information about the bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(is_public)
    async def me(self, ctx):
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
    @commands.check(is_public)
    async def invite(self, ctx):
        await ctx.send(
            "```\n"
            " - Check your Private Message!\n"
            "```"
        )

        embed = discord.Embed(
            title="Invite Me!",
            color=16579836,
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
    async def filter(self, ctx):
        filters = json.load(
            open(
                "data/cache__filters.json",
                mode="r",
                encoding="utf-8"
            )
        )

        await ctx.send(
            "```\n"
            " - Check your Private Message!\n"
            "```"
        )

        try:
            await ctx.author.send(
                "```\n"
                f" - {ctx.bot.user}'s filter information!\n"
                f" - {len(filters)} words\n"
                "```"
            )

            result = ""
            for f in filters:
                result += f"- {f}\n"

            result = io.BytesIO(result.encode("utf-8"))
            await ctx.author.send(
                file=discord.File(
                    fp=result,
                    filename="filter.txt"
                )
            )
        except discord.errors.Forbidden:
            pass

    @commands.command(help="Check cache information")
    @commands.cooldown(1, 10, commands.BucketType.user)
    @commands.check(is_public)
    async def cache(self, ctx):
        await ctx.send(
            "```\n"
            f" - Cached Image: {len(img_cache.get_cache_list())}\n"
            f" - Cache Limit: {option.cache_limit}\n"
            f" - Cache Size: {round(img_cache.get_cache_size() / (1024 * 1024), 2)} MB\n"
            "```"
        )

    @commands.command(help="Send random image from cache")
    @commands.cooldown(1, 5, commands.BucketType.user)
    @commands.check(is_public)
    async def send(self, ctx):
        content = await img_cache.get_cat_random()

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
                    filename=f"{str(uuid.uuid4())}.png"
                )
            )
