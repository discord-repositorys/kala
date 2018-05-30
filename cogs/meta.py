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
        
    client_id = 450419305671032832
        
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
        
    @commands.command()
    async def discrim(self, ctx, *, discriminator:str):
        """Gets a username#discriminator list of all users that the bot can see with the specified discriminator"""
        members = []
        for member in list(self.bot.get_all_members()):
            if member.discriminator == discriminator and str(member) not in members:
                members.append(str(member))
        if len(members) == 0:
            members = Language.get("information.no_discrims_found", ctx).format(discriminator)
        else:
            members = "```{}```".format(", ".join(members))
        await ctx.send(members)
        
    @commands.command()
    async def emoteinfo(self, ctx, *, emote:discord.Emoji):
        """Gets information on a custom emote (Only works for servers the bot is on)"""
        fields = {Language.get("information.name", ctx):emote.name, Language.get("information.id", ctx):emote.id, Language.get("information.server_origin", ctx):emote.guild.name, Language.get("information.created_on", ctx):format_time(emote.created_at), Language.get("information.colons_required", ctx):emote.require_colons, Language.get("information.managed_by_twitch", ctx):emote.managed}
        embed = make_list_embed(fields)
        embed.title = ":{}:".format(emote.name)
        embed.color = 0xFF0000
        embed.set_thumbnail(url=emote.url)
        await ctx.send(embed=embed)
        
def setup(bot):
    bot.add_cog(Meta(bot))
