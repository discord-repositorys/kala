
import discord 
from discord.ext import commands
import asyncio
import os
import json
import traceback
import sys
import textwrap
import io
from contextlib import redirect_stdout
import random
import inspect
from motor.motor_asyncio import AsyncIOMotorClient
import re


bravo_db = AsyncIOMotorClient(os.environ['DB'])

async def getprefix(bot, message):
    if isinstance(message.channel, discord.DMChannel): return "k."
    l = await bravo_db.bravo.prefix.find_one({"id": str(message.guild.id)})
    pre = None
    lol = None
    if l:
        pre = l.get('prefix') or "k."
    else:
        match = re.match(f"<@!?{bot.user.id}> ", message.content)   
        if match:
            lol = match.group()
        else:
            lol = None
    return lol or pre or "k."

async def save_prefix(prefix, guildID, ctx):
    await bravo_db.bravo.prefix.update_one({"id": str(ctx.guild.id)}, {"$set": {"prefix": prefix}}, upsert=True)

#prefixes=['k.', 'K.']
bot = commands.Bot(command_prefix=getprefix, owner_id=426060491681431562)
bot.commands_run = 0



@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')

@bot.event
async def on_command(ctx):
    bot.commands_run += 1
    log = bot.get_channel(451103131409842176)
    em = discord.Embed(color=discord.Color(value=0x00ff00), title="Command Run!")
    em.set_author(name=str(ctx.author), icon_url=ctx.author.avatar_url)
    em.add_field(name="User ID", value=ctx.author.id)
    em.add_field(name="Server", value=ctx.guild.name)
    em.add_field(name="Server ID", value=ctx.guild.id)
    em.add_field(name="User Status",value=ctx.author.status)
    em.add_field(name="Channel", value=ctx.channel.name)
    em.add_field(name="Command Content", value=f"```{ctx.message.content}```")
    em.set_thumbnail(url=ctx.guild.icon_url)
    await log.send(embed=em)

@bot.event
async def on_guild_join(guild):
    channel = bot.get_channel(441408391676559361)
    embed = discord.Embed(title='New Server!', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.green())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)

@bot.event
async def on_guild_remove(guild):
    channel = bot.get_channel(441408391676559361)
    embed = discord.Embed(title='Removed from Server', description=f'Server Name: {guild.name} | Server Num {len(bot.guilds)}', color=discord.Color.red())
    embed.set_thumbnail(url=guild.icon_url)
    embed.set_footer(text=f"Server ID: {guild.id}")
    embed.set_author(name=f"Owner: {guild.owner} | ID: {guild.owner.id}", icon_url=guild.owner.avatar_url)
    await channel.send(embed=embed)

bot.load_extension("cogs.mod")
bot.load_extension("cogs.info")
bot.load_extension("cogs.ErrorHandler")
bot.load_extension("cogs.pubg")
bot.load_extension("cogs.idiotic")
bot.load_extension("cogs.math")
bot.load_extension("cogs.utility")
bot.load_extension("cogs.owner")
bot.load_extension("cogs.fun")
bot.load_extension("cogs.nsfw")
bot.load_extension("cogs.meta")

@bot.command()
@commands.has_permissions(manage_messages=True)
async def prefix(ctx, prefix=None):
    """Change Prefix of the server"""
    guildID = str(ctx.guild.id)
    if not prefix:
        return await ctx.send('Please provide a prefix for this command to work')
    try:
        await save_prefix(prefix, guildID, ctx)
        await ctx.send(f'Prefix `{prefix}` successfully saved (re-run this command to replace it)')
    except Exception as e:
        await ctx.send(f'Something went wrong\nError Log: `str({e})`')

@bot.command(name='presence')
@commands.is_owner()
async def _set(ctx, Type=None, *, thing=None):
    """What AM I doing?!?!?!"""
    if Type is None:
        await ctx.send('Do it right, plz! Usage: *presence [game/stream] [msg]')
    else:
      if Type.lower() == 'stream':
        await bot.change_presence(activity=discord.Game(name=thing,type=1, url='https://www.twitch.tv/scarecrowboat'), status='online')
        await ctx.send(f'Presence set to {thing}.')
      elif Type.lower() == 'game':
        await bot.change_presence(activity=discord.Game(name=thing))
        await ctx.send(f'Presece set to {thing}.')
      elif Type.lower() == 'clear':
        await bot.change_presence(activity=None)
        await ctx.send('Presence set to `nil`.')
      else:
        await ctx.send('Want me to do something? YOU do it right first. Usage: *presence [game/stream] [msg]')


@bot.command()
async def ping(ctx):
    """Ping the bot"""
    await ctx.send("Pong! https://www.tenor.co/zP3r.gif ")


bot.run(os.environ['TOKEN'])
