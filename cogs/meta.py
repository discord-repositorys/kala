import discord
from discord.ext import commands
import random
import asyncio
import datetime
import time
import traceback
import sys
import aiohttp
import urllib.parse
import copy
import unicodedata
import inspect

class Meta:
    """Meta Commands"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Shows you information about a number of characters.
        Only up to 25 characters at a time.
        """

        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
        msg = '\n'.join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send('Output too long to display.')
        await ctx.send(msg)
        
    @commands.command(aliases=['invite'])
    async def join(self, ctx):
        """Joins a server."""
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.manage_roles = True
        perms.manage_channels = True
        perms.ban_members = True
        perms.kick_members = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.add_reactions = True
        await ctx.send(f'<{discord.utils.oauth_url(self.bot.client_id, perms)}>')
        
def setup(bot):
    bot.add_cog(Meta(bot))
