import discord
from discord.ext import commands
import random
import random as pyrandom
import asyncio
import datetime
import time
import traceback
import sys
import aiohttp
import base64
import urllib
import json
from discord.ext.commands import clean_content


ZALGO_CHARS = [chr(x) for x in range(768, 879)]


class Fun:
    """Fun Commands"""
    def __init__(self, bot):
        self.bot = bot
				
		@commands.command()
		async def emojis(self, ctx):
				"""Display lacal emojis"""
				emojistr=''
				emojis=ctx.guild.emojis
				if len(emojis) == 0:
					emojistr = 'No emojis in this server.'
				else: 
						for emote in emojis:
							emojistr +=' '+str(emote)+' '
				await ctx.send(emojistr)
				
				
    @commands.command(pass_context=True)
    async def say(self, ctx, *, msg: clean_content()):
        """Make the bot say something. Prevents bot triggering and mentioning other users."""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        finally:
            embed = discord.Embed(color=ctx.author.color, title=f'{ctx.author} said:')
            embed.description = msg
            await ctx.send(embed=embed)
	
    @commands.command()
    async def zalgo(self, ctx, *, text):
        """I̤̠̬T̢̐͟ Ì̦̮Sͣͣ͠ C̋͢͠Ơ̸̂M̥̟̂I̟̾̐N̊̔Ǵ͞ F͉̃ͅO̠̳ͭR̾̄̉ Y͚̜͡O̮̮̩Ù͚͎."""
       
        await ctx.send("".join(
            c + "".join(
                random.choice(ZALGO_CHARS) for _
                in range(pyrandom.randint(2, 7) * c.isalnum()))
            for c in text
	))
        
	
    @commands.command(aliases=['re'])
    async def randomemoji(self, ctx):
        """Sends a random emoji"""
        try:
            await ctx.send(str(random.choice([emoji for emoji in ctx.bot.emojis if emoji.require_colons])))
        except ValueError:
            await ctx.message.add_reaction(':EeveeShy:450878135936876554')

    @commands.command()
    async def star(self, ctx, *, msg):
        """Create a star out of a string 1-25 characters long."""
        if (len(msg) > 25):
            return await ctx.send("String must be less than 26 characters")
        elif (len(msg) == 0):
            return await ctx.send("String must be at least 1 character")

        str = '```\n'

        mid = len(msg) - 1

        for i in range(len(msg) * 2 - 1):
            if (mid == i):
                str += msg[::-1] + msg[1:] + "\n"
            else:
                let = abs(mid - i)
                str += " " * (mid - let)
                str += msg[let]
                str += " " * (let - 1)
                str += msg[let]
                str += " " * (let - 1)
                str += msg[let]
                str += "\n"

        str += "```"
        await ctx.send(str)
	
    @commands.command()
    async def rollint(self, ctx, *, num: int=100):
        """Random number from 0 to num."""
        if num <= 0:
            return await ctx.send("Try a number greater than 0.")
        await ctx.send("{0}".format(pyrandom.randint(0, num)))
	
    @commands.command()
    async def roast(self, ctx, user: discord.Member = None):
      async with aiohttp.ClientSession().get('https://insult.mattbas.org/api/insult.json') as resp:
        data = await resp.json(content_type=None)
      await ctx.send(data['insult'])

    
    @commands.command(aliases=['wtp', 'wdp'])
    async def whosthatpokemon(self, ctx):
		
      num = random.randint(1, 926)
      async with aiohttp.ClientSession().get(f'https://pokeapi.co/api/v2/pokemon-form/{num}/') as resp:
        data = await resp.json()
      embed = discord.Embed(title="Who\'s that pokemon!?", color = ctx.author.color)
      embed.set_image(url=data['sprites']['front_default'])
      embed.set_footer(text='Use all lowercase. Doesn\'t register with uppercase letters.')
      await ctx.send(embed = embed)
      guess = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
      if guess.content == data['name']:
        await ctx.send(f'Correct! That Pokemon is: {data["name"]}!')
      else:
        await ctx.send(f'Wrong! That Pokemon is: {data["name"]}!')

    
	
    @commands.command()
    async def emojify(self, ctx, *, text: str):
        """Turns your text into emojis!"""
        try:
            await ctx.message.delete()
        except discord.Forbidden:
            pass
        to_send = ""
        for char in text:
            if char == " ":
                to_send += " "
            elif char.lower() in 'qwertyuiopasdfghjklzxcvbnm':
                to_send += f":regional_indicator_{char.lower()}:  "
            elif char in '1234567890':
                numbers = {
                    "1": "one",
                    "2": "two",
                    "3": "three",
                    "4": "four",
                    "5": "five",
                    "6": "six",
                    "7": "seven",
                    "8": "eight",
                    "9": "nine",
                    "0": "zero"
                }
                to_send += f":{numbers[char]}: "
            else:
                return await ctx.send("Characters must be either a letter or number. Anything else is unsupported.")
        if len(to_send) > 2000:
            return await ctx.send("Emoji is too large to fit in a message!")
        await ctx.send(to_send)
    
    @commands.group(invoke_without_command=True)
    async def base64(self, ctx):
        '''Encode and decode base64 Text time to annoy your friends with encoded text.'''
        await ctx.send("Base64 Encode/Decode\nCommands: encode: Encode text\ndecode: Decode text")

    @base64.command()
    async def encode(self, ctx, *, msg: str):
        '''Encode base64 text'''
        try:
            x = base64.b64encode(msg.encode("ascii")).decode("ascii")
            if len(x) > 1950: return await ctx.send("Results too long")
            await ctx.send(f"```{x}```")
        except Exception as e:
            await ctx.send("Something went wrong.")
            print(e)
        
    @base64.command()
    async def decode(self, ctx, *, msg: str):
        '''Decode base64 text'''
        try:
            x = base64.b64decode(msg)
            if len(x) > 1950: return await ctx.send("Results too long")
            await ctx.send(f"```{x.decode('ascii')}```")
        except Exception as e:
            await ctx.send("Invalid Base64 Text")
            print(e)

    @commands.command(aliases=["xmas"])
    async def christmas(self, ctx):
        now = datetime.datetime.utcnow()
        xmas = datetime.datetime(now.year, 12, 25)
        if xmas < now:
            xmas = xmas.replace(year=now.year + 1)
        delta = xmas - now
        weeks, remainder = divmod(int(delta.total_seconds()), 604800)
        days, remainder2 = divmod(remainder, 86400)
        hours, remainder3 = divmod(remainder2, 3600)
        minutes, seconds = divmod(remainder3, 60)
        embed = discord.Embed(color=ctx.author.color)
        embed.add_field(name=":gift::christmas_tree::santa:Time left until Christmas:santa::christmas_tree::gift:", value=f"{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.")
        await ctx.send(embed=embed)


    @commands.command(aliases=['ween'])
    async def halloween(self, ctx):
        now = datetime.datetime.utcnow()
        ween = datetime.datetime(now.year, 10, 31)
        if ween < now:
            ween = ween.replace(year=now.year + 1)
        delta = ween - now
        weeks, remainder = divmod(int(delta.total_seconds()), 604800)
        days, remainder2 = divmod(remainder, 84000)
        hours, remainder3 = divmod(remainder2, 3600)
        minutes, seconds = divmod(remainder3, 60)
        embed = discord.Embed(color=ctx.author.color)
        embed.add_field(name=":jack_o_lantern:Time left until Halloween:jack_o_lantern:", value=f'{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.')
        await ctx.send(embed=embed)

    @commands.command(aliases=['ny'])
    async def newyear(self, ctx):
        now = datetime.datetime.utcnow()
        ny = datetime.datetime(now.year, 1, 1)
        if ny < now:
            ny = ny.replace(year=now.year + 1)
        delta = ny - now
        weeks, remainder = divmod(int(delta.total_seconds()), 604800)
        days, remainder2 = divmod(remainder, 84000)
        hours, remainder3 = divmod(remainder2, 3600)
        minutes, seconds = divmod(remainder3, 60)
        embed = discord.Embed(color=ctx.author.color)
        embed.add_field(name=f":confetti_ball:{self.bot.get_emoji(450881603149889539)}Time left until New Year{self.bot.get_emoji(450881603149889539)}:confetti_ball:", value=f'{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.')
        await ctx.send(embed=embed)

    @commands.command(aliases=['bd', 'bday'])
    async def birthday(self, ctx):
        now = datetime.datetime.utcnow()
        ny = datetime.datetime(now.year, 6, 14)
        if ny < now:
            ny = ny.replace(year=now.year + 1)
        delta = ny - now
        weeks, remainder = divmod(int(delta.total_seconds()), 604800)
        days, remainder2 = divmod(remainder, 84000)
        hours, remainder3 = divmod(remainder2, 3600)
        minutes, seconds = divmod(remainder3, 60)
        embed = discord.Embed(color=ctx.author.color)
        embed.add_field(name=f":confetti_ball::cake::birthday:Time left until BloodyPikachu's BDAY:cake::birthday::confetti_ball:", value=f'{weeks} weeks, {days} days, {hours} hours, {minutes} minutes, {seconds} seconds.')
        await ctx.send(embed=embed)
	   

def setup(bot):
    bot.add_cog(Fun(bot))
