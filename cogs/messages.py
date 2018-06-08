import discord
from discord.ext import commands
import datetime


class Messages:
    '''Make some Welcome And Goodbye messages for your server!'''

    def __init__(self, bot):
        self.bot = bot

    
    @commands.command()
    @commands.has_permissions(manage_guild=True)
    async def welcome(self, ctx, type):
        '''Enable or disable a welcome message for your server
        Code used from Remixbot
        '''
        def pred(m):
            return m.author == ctx.author and m.channel == ctx.message.channel

        config = await self.bot.db.config.find_one({'_id': str(ctx.guild.id)})
        if not config:
            config = {'_id': str(ctx.guild.id), 'welctype': False}

        if type.lower() in ('n', 'no', 'disabled', 'disable', 'off'):
            config['welctype'] = False
            await self.bot.db.config.update({'_id': str(ctx.guild.id)}, {'$set': config})
            await ctx.send('You have disabled welcome messages for this server.')
        else:
            config['welctype'] = True
            await ctx.send('Which channel do you want the welcome messages to be set to? Use a channel mention.')
            channel = await self.bot.wait_for('message', check=pred, timeout=60.0)
            id = channel.content.strip('<#').strip('>')
            if id == channel.content:
                return await ctx.send('Please mention a channel.')
            config['welcchannel'] = str(id)
            await ctx.send('What do you want the message to be?\nUsage:```\n{mention}: Mentions the joining user.\n{name}: Replaces this with the user\'s name.\n{server}: Server name.\n{membercount}: Returns the number of members in the guild.\n```')
            msg = await self.bot.wait_for('message', check=pred, timeout=60.0)
            config['welc'] = str(msg.content).replace('"', '\"')
            await self.bot.db.config.update({'_id': str(ctx.guild.id)}, {'$set': config})
            await ctx.send('Your welcome message has been successfully set.')
            
def setup(bot): 
    bot.add_cog(Messages(bot)) 
