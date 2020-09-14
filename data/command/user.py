# -*- coding: utf-8 -*-

import discord
from discord.ext import commands


def is_public(ctx: commands.context):
    return not isinstance(
        ctx.message.channel,
        discord.abc.PrivateChannel
    )


class User(commands.Cog, name="for @everyone"):
    @commands.command(help="Check information about the bot")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def status(self, ctx: commands.context):
        await ctx.send(
            "```\n"
            f" - Connected to ( {len(ctx.bot.guilds)} ) guilds!\n"
            "```"
        )

    @commands.command(help="Send Bot Invite link to you")
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def invite(self, ctx: commands.context):
        from data.lib import invite

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
                "```"
            )
