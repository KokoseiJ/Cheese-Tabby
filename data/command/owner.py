# -*- coding: utf-8 -*-

import sys

from discord.ext import commands


class Owner(commands.Cog, name="for Bot OWNER"):
    @commands.command(help="(Recommend) Shutdown the bot")
    @commands.is_owner()
    async def close(self, ctx: commands.context):
        await ctx.send(":wave: :cat:")
        await ctx.bot.close()

    @commands.command(help="Shutdown the bot")
    @commands.is_owner()
    async def exit(self, ctx: commands.context):
        await ctx.send(":wave: :cat:")
        sys.exit(0)
