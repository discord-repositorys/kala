import discord
from discord.ext import commands
import asyncio
import json

class Messages:
  def __init__(self, bot):
    self.bot = bot
    
  @commands.command()
  @commmands.has_permissions(manage_guild=True)
  async def setup(self, ctx):
    with open('../servers.json') as f:
      data = json.loads(f.read())
    server = ctx.guild
    data[str(server.id)] = {}
    x = await ctx.send('Welcome to the Kala interactive setup.\nNote: This feature is in beta, and is not stable.\nUse at your descrection')
    await asyncio.sleep(5)
    await ctx.send('Enable welcome messages?')
    msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
    if msg.content.lower() == 'yes':
      await ctx.send('What would you like the message to say?')
      await ctx.send('I support {user}, {server}, and {member_count} in my messages.')
      msg = await bot.wait_for('message', check=lambda m: m.author == ctx.author)
      msg = f'{msg.content}'
      await ctx.send('Which channel should I send the message to?')
      welc_channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
      if welc_channel.content.startswith('<#'):
        await ctx.send(f'Welcome channel set to: {welc_channel.content} with welcome message: {msg}')
      else:
        await ctx.send('Invalid channel. Please mention the channel in order for us to continue.')
        await ctx.send('Which channel should I send the message to?')
        welc_channel = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
        await ctx.send(f'elcome channel set to: {welc_channel.content} with welcome message: {msg}')
    
    else: 
      msg = None
      welc_channel = None
      pass
    
    await ctx.send('Enable leave message?')
		leave_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if leave_msg.content.lower() == 'yes':
			await ctx.send('What should the message say?')
			await ctx.send('You can use {user} {server} and {member_count} to use them in your message')
			leave_msg = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
			await ctx.send(f'Leave message set to {leave_msg.content}')	
		else:
			leave_msg = None
      pass
    
    await ctx.send('Enable mod-log?')
		mod_log = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
		if mod_log.content.lower() == 'yes':
			await ctx.send('What channel should the mod-log be?')
			mod_log = await self.bot.wait_for('message', check=lambda m: m.author == ctx.author)
			await ctx.send(f'Mod-log set to channel {mod_log.content}')
		else:
			mod_log = None
			pass
			
		data[str(server.id)]['name'] = server.name 
		data[str(server.id)]['prefix'] = prefix.content.strip('"')
		if welc_channel and msg != None:
			data[str(server.id)]['welc_channel'] = welc_channel.content.strip('"')
			data[str(server.id)]['welc_msg'] = msg.strip('"')
		else:
			data[str(server.id)]['welc_channel'] = welc_channel
			data[str(server.id)]['welc_msg'] = msg
		if leave_msg != None:
			data[str(server.id)]['leave_msg'] = leave_msg.content.strip('"')
		else:
			data[str(server.id)]['leave_msg'] = leave_msg
		if mod_log != None:
			data[str(ctx.guild.id)]['mod_log'] = mod_log.content.strip("'")
		else:
			data[str(ctx.guild.id)]['mod_log'] = mod_log
		data = json.dumps(data, indent=4, sort_keys=True)
		
		with open('cogs/utils/servers.json', 'w') as f:
			f.write(data)
    await ctx.send('Setup complete. Enjoy your server!')
    
  @commands.command()
  @commands.has_permissions(manage_guild=True)
  async def config(self, ctx, setting=None, *, change=None):
    if setting == None:
			await ctx.send('Here is what you can change: prefix, welcome_message, welcome_channel, leave_message, mod_log')
		with open('../servers.json') as f:
			data = json.loads(f.read())
		if setting == 'prefix':
			data[str(ctx.guild.id)]['prefix'] = change
			await ctx.send(f'Prefix set to `{change}`')
		if setting == 'welcome_message':
			data[str(ctx.guild.id)]['welc_msg'] = change
			await ctx.send(f'Welcome message set to `{change}`')
		if setting == 'welcome_channel':
			data[str(ctx.guild.id)]['welc_channel'] = change
			await ctx.send(f'Welcome channel set to {change}')
		if setting == 'leave_message':
			data[str(ctx.guild.id)]['leave_msg'] = change
			await ctx.send(f'Leave message set to `{change}`')
		if setting == 'mod_log':
			data[str(ctx.guild.id)]['mod_log'] = change
			await ctx.send(f'Mod-log set to {change}')
		data = json.dumps(data, indent=4, sort_keys=True)
		with open('cogs/utils/servers.json', 'w') as f:
			f.write(data)
		
		
def setup(bot):
  bot.add_cog(Messages(bot))
