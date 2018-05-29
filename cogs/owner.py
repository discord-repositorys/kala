from discord import HTTPException
from discord.ext import commands
import random
import asyncio
import datetime
import time
import traceback
import sys
import aiohttp
import discord


class Owner:
    """Owner-only commands"""
    def __init__(self, bot):
        self.bot = bot
        self.sessions = set()

    @commands.command(aliases=['r', 'reload'], hidden=True)
    @commands.is_owner()
    async def cog_reload(self, ctx, *, cog: str):
        """Command which Reloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'{self.bot.get_emoji(450879049699688458)}Error! {type(e).__name__} - {e}')
        else:
            await ctx.send(f'{self.bot.get_emoji(450876075161944075)} Success!')

    @commands.command(name='load', hidden=True)
    @commands.is_owner()
    async def cog_load(self, ctx, *, cog: str):
        """Command which Loads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.load_extension(cog)
        except Exception as e:
            await ctx.send(f'{self.bot.get_emoji(450881764978589696)} Error! {type(e).__name__} - {e}')
        else:
            await ctx.send(f'{self.bot.get_emoji(450881658271301632)} Success!')

    @commands.command(name='unload', hidden=True)
    @commands.is_owner()
    async def cog_unload(self, ctx, *, cog: str):
        """Command which Unloads a Module.
        Remember to use dot path. e.g: cogs.owner"""

        try:
            self.bot.unload_extension(cog)
        except Exception as e:
            await ctx.send(f'{self.bot.get_emoji(450883357304291330)} Error! {type(e).__name__} - {e}')
        else:
            await ctx.send(f'{self.bot.get_emoji(450883247077982219)} Success!')

    @commands.command(aliases=["getservers", "getguild", "getserver"], hidden=True)
    @commands.guild_only()
    @commands.is_owner()
    async def getguilds(self, ctx):
        if (ctx.channel.permissions_for(ctx.me).embed_links):
            embed = discord.Embed(color=ctx.message.author.color)
            for i in range(0, len(self.bot.guilds)):
                embed.add_field(name=self.bot.guilds[i].name, value=self.bot.guilds[i].id, inline=True)
            await ctx.send(embed=embed)

    @commands.command(name="name", hidden=True)
    @commands.is_owner()
    async def name_change(self, ctx, *, name: str):
        try:
            await self.bot.edit(username=name)
            await ctx.send("```Bot name has been changed to: {}```".format(name))
        except HTTPException as e:
            await ctx.send(e)

    


    

def setup(bot):
    bot.add_cog(Owner(bot))