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
import wikipedia
import openweathermapy.core as weather


class InvalidHTTPResponse(Exception):
    """Used if non-200 HTTP Response got from server."""
pass

class Utility:
    """Utility Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['roll', 'die', 'rd'])
    async def rolldice(self, ctx):
        """Rolls a 6 sided die."""
        choices = ['1', '2', '3', '4', '5', '6']
        color = discord.Color.green()
        embed = discord.Embed(color=color, title='I rolled a ', description=random.choice(choices))
        await ctx.send(embed=embed)

    @commands.command(aliases=['av'])
    async def avatar(self, ctx, user: discord.Member = None):
        """Reveal a user's avatar."""
        if user is None:
            av = ctx.message.author.avatar_url
            if '.gif' in av:
                av += "&f=.gif"
            color = discord.Color.green()
            em = discord.Embed(color=color, title=ctx.message.author.name)
            em.set_author(name='Profile Picture')
            em.set_image(url=av)
            await ctx.send(embed=em)                  
        else:
            av = user.avatar_url
            if '.gif' in av:
                av += "&f=.gif"
            color = discord.Color.green()
            em = discord.Embed(color=color, title=user.name)
            em.set_author(name='Profile Picture')
            em.set_image(url=av)
            await ctx.send(embed=em)
    @commands.command()
    async def poll(self, ctx, *, args):
        """Creates a poll with reactions. Seperate choices with |."""
        if not "|" in args:
            return await ctx.send("Seperate the question and choices with |.\nUsage: k.poll What is the question? | OPT 1 | OPT 2")
        try:
            await ctx.message.delete()
        except:
            pass
        choices = args.split("|")
        desc = ""
        counter = 0
        em = discord.Embed(color=discord.Color(value=0x00ff00), title=choices[0])
        choices.remove(choices[0])
        if len(choices) > 9:
            return await ctx.send("You can have a maximum of 9 choices for a poll.")
        for x in choices:
            counter += 1
            desc += f"{str(counter)} - {x}\n"
        em.description = desc
        msg = await ctx.send(embed=em)
        # emojis = {
        #     "1": ":one:",
        #     "2": ":two",
        #     "3": ":three:",
        #     "4": ":four:",
        #     "5": ":five:",
        #     "6": ":six:",
        #     "7": ":seven:",
        #     "8": ":eight:",
        #     "9": ":nine:"
        # }
        counter = 0
        for x in choices:
            counter += 1
            await msg.add_reaction(f"{str(counter)}\u20e3")

    @commands.command()
    async def feedback(self, ctx, *, feedback=None):
        """Send feedback about the bot."""
        if feedback is None:
            color = discord.Color.red()
            em = discord.Embed(color=color, title=f'{self.bot.get_emoji(450881764978589696)} Error!')
            em.description = 'You have failed to enter your feedback!'
            await ctx.send(embed=em)
        else:
            try:
                lol = self.bot.get_channel(450896646373376000)
                color = discord.Color.green()
                em = discord.Embed(color=color, title='Feedback')
                em.description = feedback
                em.set_author(name=f"Sent by: {ctx.author.name}", icon_url=ctx.author.avatar_url)
                em.set_footer(text=f"Sent from {ctx.guild.name} in #{ctx.channel.name}", icon_url=ctx.guild.icon_url)
                await lol.send(embed=em)
                em.description = f'{self.bot.get_emoji(450881658271301632)} Feedback Sent! Devs will make sure the problem is fixed asap!'
                await ctx.send(embed=em)
            except Exception as e:
                color = discord.Color(value=0xf44e42)
                em = discord.Embed(color=color, title='Error :x:')
                em.description = f"More details: \n\n{e}"
                await ctx.send(embed=em)

    @commands.command()
    async def choose(self, ctx, *, args):
        """Can't choose. Let this bot do it for you. Seperate choices with a comma."""
        lol = self.bot.get_emoji(450878135936876554)
        msg = await ctx.send(lol)
        args = args.split("|")
        await asyncio.sleep(3)
        await msg.edit(content=f"I choose:\n**{random.choice(args)}**")

    @commands.command(aliases=['ri', 'rinfo'])
    async def roleinfo(self, ctx, *, rolename):
        try:
            role = discord.utils.get(ctx.guild.roles, name=rolename)
        except:
            return await ctx.send("Role not found. Please make sure the role name is correct. (Case Sensitive!)")
        em = discord.Embed(color=role.color, title=f'Role Info: {rolename}')
        p = ""
        if role.permissions.administrator:
            p += "Administrator :white_check_mark: \n"
        else:
            p += "Administrator :x: \n"
        if role.permissions.create_instant_invite:
            p += "Create Instant Invite :white_check_mark: \n"
        else:
            p += "Create Instant Invite :x:\n"
        if role.permissions.kick_members:
            p += "Kick Members :white_check_mark: \n"
        else:
            p += "Kick Members :x:\n"
        if role.permissions.ban_members:
            p += "Ban Members :white_check_mark: \n"
        else:
            p += "Ban Members :x:\n"
        if role.permissions.manage_channels:
            p += "Manage Channels :white_check_mark: \n"
        else:
            p += "Manage Channels :x:\n"
        if role.permissions.manage_guild:
            p += "Manage Server :white_check_mark: \n"
        else:
            p += "Manage Server :x:\n"
        if role.permissions.add_reactions:
            p += "Add Reactions :white_check_mark: \n"
        else:
            p += "Add Reactions :x:\n"
        if role.permissions.view_audit_log:
            p += "View Audit Log :white_check_mark: \n"
        else:
            p += "View Audit Log :x:\n"
        if role.permissions.read_messages:
            p += "Read Messages :white_check_mark: \n"
        else:
            p += "Read Messages :x:\n"
        if role.permissions.send_messages:
            p += "Send Messages :white_check_mark: \n"
        else:
            p += "Send Messages :x:\n"
        if role.permissions.send_tts_messages:
            p += "Send TTS Messages :white_check_mark: \n"
        else:
            p += "Send TTS Messages :x:\n"
        if role.permissions.manage_messages:
            p += "Manage Messages :white_check_mark: \n"
        else:
            p += "Manage Messages :x:\n"
        if role.permissions.embed_links:
            p += "Embed Links :white_check_mark: \n"
        else:
            p += "Embed Links :x:\n"
        if role.permissions.attach_files:
            p += "Attach Files :white_check_mark: \n"
        else:
            p += "Attach Files \n" 
        if role.permissions.read_message_history:
            p += "Read Message History :white_check_mark: \n"
        else:
            p += "Read Message History :x:\n"
        if role.permissions.mention_everyone:
            p += "Mention @everyone :white_check_mark: \n"
        else:
            p += "Mention @everyone :x:\n"
        if role.permissions.external_emojis:
            p += "Use External Emojis :white_check_mark: \n"
        else:
            p += "Use External Emojis :x:\n"
        if role.permissions.change_nickname:
            p += "Change Nicknames :white_check_mark: \n"
        else:
            p += "Change Nicknames :x:\n"
        if role.permissions.manage_nicknames:
            p += "Manage Nicknames :white_check_mark: \n"
        else:
            p += "Manage Nicknames :x:\n"
        if role.permissions.manage_roles:
            p += "Manage Roles :white_check_mark: \n"
        else:
            p += "Manage Roles :x:\n"
        if role.permissions.manage_webhooks:
            p += "Manage Webhooks :white_check_mark: \n"
        else:
            p += "Manage Webhooks :x:\n"
        if role.permissions.manage_emojis:
            p += "Manage Emojis :white_check_mark: \n"
        else:
            p += "Manage Emojis :x:\n"
        v = "" 
        if role.permissions.connect:
            v += "Connect :white_check_mark: \n"
        else:
            v += "Connect :x:\n"
        if role.permissions.speak:
            v += "Speak :white_check_mark: \n"
        else:
            v += "Speak :x:\n"
        if role.permissions.mute_members:
            v += "Mute Members :white_check_mark: \n"
        else:
            v += "Mute Members :x:\n"
        if role.permissions.deafen_members:
            v += "Deafen Members :white_check_mark: \n"
        else:
            v += "Deafen Members :x:\n"
        if role.permissions.move_members:
            v += "Move Members :white_check_mark: \n"
        else:
            v += "Move Members :x:\n"
        if role.permissions.use_voice_activation:
            v += "Use Voice Activation :white_check_mark: \n"
        else:
            v += "Use Voice Activation :x:\n"
        em.description = f"**General Permissions** \n\n{p} \n\n\n**Voice Permissions** \n\n{v}"
        em.add_field(name='ID', value=role.id)
        em.add_field(name='Position from Bottom', value=role.position)
        if role.mentionable:
            a = 'Mentionable'
        else:
            a = 'Not Mentionable'
        em.add_field(name='Mentionable', value=a)
        em.add_field(name='Time Created', value=str(role.created_at.strftime("%A, %b %m, %Y at %I:%M %p")))
        member = ""
        for x in role.members:
            member += f"{x.name} \n"
        em.add_field(name='Members in the Role', value=member)
        await ctx.send(embed=em)
            
    @commands.command()
    async def weather(self, ctx, *, city: str):
        settings = {"APPID": 'ab1962b0bdb0f00d417974d705b86595'}
        data = weather.get_current('{}'.format(city), units='metric', **settings)
        data2 = weather.get_current(city, units='standard', **settings)
        keys = ['main.temp', 'main.humidity', 'coord.lon', 'coord.lat']
        x = data.get_many(keys)
        loc = data('name')
        country = data('sys.country')
        lon = data('coord.lon')
        lat = data('coord.lat')
        temp = data('main.temp')
        temp2 = temp * 9/5 + 32
        high = data('main.temp_max')
        low = data('main.temp_min')
        high2 = high * 9/5 + 32
        low2 = low * 9/5 + 32
        embed = discord.Embed(title='{}, {}'.format(loc, country), color=0x00FF00)
        embed.add_field(name='Absolute Location', value='Longitude, Latitude\n{}, {}'.format(lon, lat))
        embed.add_field(name='Temperature', value='{}F, {}C'.format(temp2, temp))
        embed.add_field(name='Humidity', value='{}%'.format(data('main.humidity')))
        embed.add_field(name='Wind Speed', value='{}m/s'.format(data('wind.speed')))       
        embed.add_field(name='Low and High Temp', value='{}F - {}F\n{}C - {}C'.format(low2, high2, low, high))
        embed.set_footer(text='Weather Data from OpenWeatherMap.org')
        embed.set_thumbnail(url='../OpenWeatherMap_logo.png')
        await ctx.send(embed=embed)

    @commands.group(invoke_without_command=True)
    async def role(self, ctx, userid, *args):
        """Sets a role to a user
        
        Usage: k.role @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    @commands.has_permissions(manage_server=True)
    async def set(self, ctx, userid, *args):
        """Sets a role to a user
        
        Usage: k.role set @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.add_roles(role)
            await ctx.send("Set role {} for {}!".format(args, user.mention))

    @role.command()
    @commands.has_permissions(manage_server=True)
    async def remove(self, ctx, userid, *args):
        """Removes a role from a user
        
        Usage: k.role remove @user <role name>"""
        permissions = dict(iter(ctx.message.channel.permissions_for(ctx.message.author)))
        if not permissions['manage_roles']:
            await ctx.send("You need 'Manage roles' permission to do this!")
            return
        args = ' '.join(args)
        args = str(args)
        mentions = ctx.message.mentions
        for user in mentions:
            role = discord.utils.get(ctx.guild.roles, name=args)
            await user.remove_roles(role)
            await ctx.send("Remove role {} for {}!".format(args, user.mention))

    
    @commands.command(pass_context=True)
    async def urban(self, ctx, *args):
        """Searches urbandictionary for a definition.
        Arguments:
        `*args` : list  
        The quer(y/ies)"""
        args = ' '.join(args)
        args = str(args)
        apilink = "http://api.urbandictionary.com/v0/define?term=" + args
        async with aiohttp.ClientSession() as session:
            async with session.get(apilink) as r:
                if r.status == 200:
                    datajson = await r.json()
                else:
                    print("Invalid HTTP Response:" + str(r.status))
                    raise InvalidHTTPResponse()
        listcount = 0
        if not datajson['list']:
            await ctx.send("Result not found!")
            return
        try:
            while datajson['list'][listcount]['definition'].count('') > 1001:
                listcount = listcount + 1
        except IndexError:
            await ctx.send("Sorry, but we seem to reach the Discord character limit!")
        result = datajson['list'][listcount]
        embed=discord.Embed(title="**" + result['word'] + "**", url=result['permalink'], description="by: " + result['author'], color=0xc4423c)
        embed.add_field(name="Definition", value=result['definition'], inline=False)
        embed.add_field(name="Example", value=result['example'], inline=True)
        embed.set_footer(text=u"👍 " + str(result['thumbs_up']) + " | " + u"👎 " + str(result['thumbs_down']))
        await ctx.send(embed=embed)
        
    @commands.command(name='top_role', aliases=['toprole'])
    @commands.guild_only()
    async def show_toprole(self, ctx, *, member: discord.Member=None):
        """Simple command which shows the members Top Role."""

        if member is None:
            member = ctx.author

        embed = discord.Embed(title="Highest role")
        embed.description = f'The top role for {member.display_name} is {member.top_role.name}'
        await ctx.send(embed=embed)
    
    @commands.command(name='perms', aliases=['perms_for', 'permissions'])
    @commands.guild_only()
    async def check_permissions(self, ctx, *, member: discord.Member=None):
        """A simple command which checks a members Guild Permissions.
        If member is not provided, the author will be checked."""

        if not member:
            member = ctx.author

        
        perms = '\n'.join(perm for perm, value in member.guild_permissions if value)

        
        embed = discord.Embed(title='Permissions for:', description=ctx.guild.name, colour=member.colour)
        embed.set_author(icon_url=member.avatar_url, name=str(member))

        
        embed.add_field(name='\uFEFF', value=perms)

        await ctx.send(content=None, embed=embed)
        
   
    

def setup(bot):
    bot.add_cog(Utility(bot))
