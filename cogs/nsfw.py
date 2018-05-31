import discord
from discord.ext import commands
import aiohttp
import random
import json



class Nsfw:
    '''
    xd
    '''
    def __init__(self, bot):
        self.bot = bot
        self.hentai = [
 'feet', 'yuri', 'trap', 'futanari', 'hololewd', 'lewdkemo', 'solog', 'feetg', 'cum', 'erokemo', 'les', 'wallpaper', 'lewdk', 'ngif', 'meow', 'tickle', 'lewd', 'feed', 'eroyuri', 'eron', 'cum_jpg', 'bj', 'nsfw_neko_gif', 'solo', 'kemonomimi', 'nsfw_avatar', 'anal', 'slap', 'hentai', 'avatar', 'erofeet', 'holo', 'keta', 'blowjob', 'pussy', 'tits', 'holoero', 'pussy_jpg', 'pwankg', 'classic', 'femdom', 'neko', 'cuddle', 'erok', 'fox_girl', 'boobs', 'Random_hentai_gif', 'smallboobs']


    @commands.command(hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def boobs(self, ctx):
        '''Boobs using oboobs api'''
        if not ctx.channel.is_nsfw():
          await ctx.send("You tried to put nsfw in a non-nsfw channel.")
          return
        """Random"""
        api_base = 'http://api.oboobs.ru/boobs/'
        number = random.randint(1, 10303)
        url_api = api_base + str(number)
        async with aiohttp.ClientSession() as session:
           async with session.get(url_api) as data:
                data = await data.json()
                data = data[0]
        image_url = 'http://media.oboobs.ru/' + data['preview']
        em = discord.Embed(color=0x11f95e)
        em.set_author(name="Your boobs you requested:")
        em.set_image(url=image_url)
        await ctx.send(embed=em)
        
        
    @commands.command(hidden=True)
    @commands.cooldown(1, 5, commands.BucketType.user)
    async def butts(self, ctx):
        '''Get butts off the internet'''
        if not ctx.channel.is_nsfw():
          await ctx.send("You tried to put nsfw in a non-nsfw channel.")
          return
        """Random"""
        api_base = 'http://api.obutts.ru/butts/'
        number = random.randint(1, 10303)
        url_api = api_base + str(number)
        async with aiohttp.ClientSession() as session:
           async with session.get(url_api) as data:
                data = await data.json()
                data = data[0]
        image_url = 'http://media.obutts.ru/' + data['preview']
        em = discord.Embed(color=0x11f95e)
        em.set_author(name="Butt Image")
        em.set_image(url=image_url)
        await ctx.send(embed=em)
        

    #@commands.command(hidden=True)
    #async def feet(self, ctx, is_gif=None):
        #"""Gets a random picture of feet. DO NOT USE IF UNDER 18!"""
        ##if not ctx.channel.nsfw:
            #return await ctx.send("Please don't put nsfw images in a non-nsfw channel. The command has been terminated.")
        #if not is_gif:
            #resp = await self.bot.session.get("https://nekos.life/api/v2/img/feet")
        #else:
            #resp = await self.bot.session.get("https://nekos.life/api/v2/img/feetg")
        #resp = await resp.json()
        #em = discord.Embed(color=discord.Color(value=0x00ff00), title="Here you go! Enjoy. :eggplant: ")
        #em.set_author(name=f"Feet requested by: {ctx.author}", icon_url=ctx.author.avatar_url)
        #em.set_image(url=resp['url'])
        #await ctx.send(embed=em)  
        
    @commands.command(hidden=True)
    async def feet(self, ctx, is_gif=None):
        """Gets a random picture of feet. DO NOT USE IF UNDER 18!"""
        if not ctx.channel.is_nsfw():
            return await ctx.send("Please don't put nsfw images in a non-nsfw channel. The command has been terminated.")
        if not is_gif:
            async with aiohttp.ClientSession().get('https://nekos.life/api/v2/img/feet') as resp:
            resp = await resp.json()
        else:
            async with aiohttp.ClientSession().get('https://nekos.life/api/v2/img/feetg') as resp:
            resp = await resp.json()
        embed = discord.Embed(color=ctx.author.color, title='Here, have some feet.')
        embed.set_author(name=f'Feet requested by: {ctx.author}.', icon_url=ctx.author.avatar_url)
        embed.set_image(url=resp['url'])
        await ctx.send(embed = embed)
        

def setup(bot): 
    bot.add_cog(Nsfw(bot))
