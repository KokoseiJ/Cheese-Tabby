# -*- coding: utf-8 -*-

import io
import json

import discord
from discord.ext import commands

from data.lib import core, invite


def is_public(ctx):
    return not isinstance(ctx.message.channel, discord.abc.PrivateChannel)


class userCommand(commands.Cog, name="for @everyone"):
    @commands.command(help="Check information about the bot")
    @commands.check(is_public)
    async def me(self, ctx):
        filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))

        await ctx.send("```\n"
                       f"Connected to {len(ctx.bot.guilds)} guilds\n"
                       f"Filter words: {len(filters)}\n"
                       "```")

    @commands.command(help="Send the cat")
    @commands.check(is_public)
    async def cat(self, ctx):
        content = await core.get()

        if isinstance(content, str):
            await ctx.send(content=content)
        else:
            try:
                await ctx.send(file=discord.File(content, 'some_cat.png'))
            except discord.errors.Forbidden:
                await ctx.send("```\nHello?\n"
                               f"This bot need [Attach Files] and [Add Reactions] Permission!!\n"
                               f"```\n <@{ctx.guild.owner_id}>")

    @commands.command(help="Send Bot Invite link to you")
    @commands.check(is_public)
    async def invite(self, ctx):
        await ctx.send("```\nCheck your Private Message!\n```")

        embed = discord.Embed(title="Invite Me!", color=16579836,
                              description="Please Click me!",
                              url=invite.get_link(ctx.bot))
        try:
            await ctx.author.send(embed=embed)
        except discord.errors.Forbidden:
            await ctx.send("plz allow dm")

    @commands.command(help="Check filter words")
    @commands.check(is_public)
    async def filter(self, ctx):
        filters = json.load(open("data/cache__filters.json", mode="r", encoding="utf-8"))
        await ctx.send("```\nCheck your Private Message!\n```")

        try:
            await ctx.author.send(f"{ctx.bot.user}'s filter information!\n - {len(filters)} words")

            result = ""
            for f in filters:
                result += f"- {f}\n"

            result = io.BytesIO(result.encode("utf-8"))
            await ctx.author.send(file=discord.File(result, "filter.txt"))
        except discord.errors.Forbidden:
            pass
