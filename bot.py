
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
import aiohttp


bravo_db = AsyncIOMotorClient(os.environ['DB'])
cr_db = AsyncIOMotorClient(os.environ['cr_db'])

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
bot._last_result = None
bot.commands_run = 0
bot.session = aiohttp.ClientSession()

def cleanup_code(content):
    '''Automatically removes code blocks from the code.'''
    # remove ```py\n```
    if content.startswith('```') and content.endswith('```'):
        return '\n'.join(content.split('\n')[1:-1])

    return content.strip('` \n')

if 'TOKEN' in os.environ:
    heroku = True
    TOKEN = os.environ['TOKEN']

def dev_check(id):
    with open('devs.json') as f:
        devs = json.load(f)
        if id in devs:
            return True
        return False

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(bot.user.id)
    print('------')
    while True:
        await bot.change_presence(activity=discord.Game(type=discord.ActivityType.listening, name='with you in your sleep'))
        await asyncio.sleep(2)
        await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.watching, name="you sleep"))
        await asyncio.sleep(2)
        
        
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
bot.load_extension("cogs.latency")
bot.load_extension("cogs.cr")


@bot.command(name='eval')
async def _eval(ctx, *, body):
    """Evaluates python code"""
    if not dev_check(ctx.author.id):
        return await ctx.send("You cannot use this because you are not a developer.")
    env = {
        'ctx': ctx,
        'channel': ctx.channel,
        'author': ctx.author,
        'guild': ctx.guild,
        'message': ctx.message,
        '_': bot._last_result,
        'source': inspect.getsource
    }

    env.update(globals())

    body = cleanup_code(body)
    stdout = io.StringIO()
    err = out = None

    to_compile = f'async def func():\n{textwrap.indent(body, "  ")}'

    def paginate(text: str):
        '''Simple generator that paginates text.'''
        last = 0
        pages = []
        for curr in range(0, len(text)):
            if curr % 1980 == 0:
                pages.append(text[last:curr])
                last = curr
                appd_index = curr
        if appd_index != len(text) - 1:
            pages.append(text[last:curr])
        return list(filter(lambda a: a != '', pages))

    try:
        exec(to_compile, env)
    except Exception as e:
        err = await ctx.send(f'```py\n{e.__class__.__name__}: {e}\n```')
        return await ctx.message.add_reaction('\u2049')

    func = env['func']
    try:
        with redirect_stdout(stdout):
            ret = await func()
    except Exception as e:
        value = stdout.getvalue()
        err = await ctx.send(f'```py\n{value}{traceback.format_exc()}\n```')
    else:
        value = stdout.getvalue()
        if TOKEN in value:
            value = value.replace(TOKEN,"[lol]")
        if ret is None:
            if value:
                try:

                    out = await ctx.send(f'```py\n{value}\n```')
                except:
                    paginated_text = paginate(value)
                    for page in paginated_text:
                        if page == paginated_text[-1]:
                            out = await ctx.send(f'```py\n{page}\n```')
                            break
                        await ctx.send(f'```py\n{page}\n```')
        else:
            bot._last_result = ret
            try:
                out = await ctx.send(f'```py\n{value}{ret}\n```')
            except:
                paginated_text = paginate(f"{value}{ret}")
                for page in paginated_text:
                    if page == paginated_text[-1]:
                        out = await ctx.send(f'```py\n{page}\n```')
                        break
                    await ctx.send(f'```py\n{page}\n```')

    if out:
        await ctx.message.add_reaction('\u2705')  # tick
    elif err:
        await ctx.message.add_reaction('\u2049')  # x
    else:
        await ctx.message.add_reaction('\u2705')

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

@bot.command(name='presence', hidden=True)
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
    """Ping."""
    color = ctx.author.color
    e = discord.Embed(color=color, title='Pinging Kala')
    e.description = 'Please wait...'
    msg = await ctx.send(embed=e)
    em = discord.Embed(color=color, title='Ping! Bot Latency is: ')
    em.description = f"{bot.latency * 1000:.4f} ms"
    em.set_thumbnail(url="https://www.google.com/imgres?imgurl=http%3A%2F%2Fstatic.pong.com%2Fpins%2F2013%2F05%2Fg4tv-pong-flash-games-flash-games-break-most-addicting-flash_100857_D.jpg&imgrefurl=http%3A%2F%2Fwww.pong.com%2F&docid=r3uh_sUQeEOy1M&tbnid=cOAoG7-c6iUMQM%3A&vet=10ahUKEwjGgLug-KzbAhWppFkKHdtVAlwQMwhqKAAwAA..i&w=582&h=373&client=ubuntu&bih=951&biw=927&q=pong&ved=0ahUKEwjGgLug-KzbAhWppFkKHdtVAlwQMwhqKAAwAA&iact=mrc&uact=8#h=373&imgdii=vTA5ueEcweqlfM:&vet=10ahUKEwjGgLug-KzbAhWppFkKHdtVAlwQMwhqKAAwAA..i&w=582")
    await msg.edit(embed=em)
    
@bot.command()
async def cmdsrun(ctx):
    """See how many commands the bot has run!"""
    await ctx.send(bot.commands_run)
        
@bot.command()
async def invite(ctx):
    """Invite Kala to your guild."""
    await ctx.send('https://discordapp.com/oauth2/authorize?client_id=450419305671032832&scope=bot&permissions=1547005143')


bot.run(os.environ['TOKEN'])
