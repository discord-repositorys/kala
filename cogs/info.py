import discord
from discord.ext import commands
import random
import asyncio
import datetime
import time
import traceback
import sys
import aiohttp

startTime = datetime.datetime.now()

class Info:
    """Info Commands"""
    def __init__(self, bot):
        self.bot = bot
    
    

    @commands.command(aliases=['si', 'sinfo'])
    async def serverinfo(self, ctx):
        """Get some Server info!"""
        guild = ctx.guild
        guild_age = (ctx.message.created_at - guild.created_at).days
        created_at = f"Server created on {guild.created_at.strftime('%b %d %Y at %H:%M')}. That\'s over {guild_age} days ago!"
        color = discord.Color.green()
        roles = [x.name for x in guild.roles]
        role_length = len(roles)
        roles = ', '.join(roles)
        textchannels = len(guild.text_channels)
        voicechannels = len(guild.voice_channels)
        time = str(guild.created_at.strftime("%b %m, %Y, %A, %I:%M %p"))
        try:
            ban_count = len(await guild.bans())
        except discord.Forbidden:
            ban_count = "Kala Lacks the `ban members` permission. (In order to retrieve bans)"
        verification_levels = {
            0: "**None** No Security measures have been taken.",
            1: "**Low** Light Security measures have been taken. (Verified Email)",
            2: "**Moderate** Moderate Security measures have been taken. (Registered on Discord for longer than 5 minutes)",
            3: "**High** High Security measures have been taken. (Member of server for longer than 10 minutes)",
            4: "**Fort Knox** Almost inpenetrable Security measures have been taken. (Verified Phone)"
        }
        content_filter = {
            0: "**None** No Scanning enabled. (Don't scan any messages.)",
            1: "**Moderate** Moderate Scanning enabled. (Scan messages from members without a role.)",
            2: "**High** High Scanning enabled. (Scans every message.)"
        }
        mfa_levels = {
            0: "Does not require 2FA for members with Admin permission.",
            1: "Requires 2FA for members with Admin permission."
        }
        regular_emojis = len([x for x in guild.emojis if not x.animated])
        animated_emojis = len([x for x in guild.emojis if x.animated])

        embed = discord.Embed(title=guild.name, color=color)
        embed.set_thumbnail(url=guild.icon_url)
        embed.add_field(name=f'{self.bot.get_emoji(441337849933987841)} Server ID', value=str(guild.id))
        embed.add_field(name=f'{self.bot.get_emoji(441337821941202944)} Owner', value=str(guild.owner))
        embed.add_field(name=f'{self.bot.get_emoji(450791226459815936)} Total Members', value=str(guild.member_count))
        embed.add_field(name=f'{self.bot.get_emoji(446784125022633994)} Non-Bots', value=len([x for x in ctx.guild.members if not x.bot]))
        embed.add_field(name=f'{self.bot.get_emoji(441337812256817153)} Bots', value=len([x for x in ctx.guild.members if x.bot]))
        embed.add_field(name=f'{self.bot.get_emoji(441352932034740225)} Channel Categories', value=len(guild.categories))
        embed.add_field(name=f'{self.bot.get_emoji(441337844322009119)} Total Channels', value=len(guild.channels))
        embed.add_field(name=f'{self.bot.get_emoji(450809901007110145)} Text Channels', value=textchannels)
        embed.add_field(name=f'{self.bot.get_emoji(450810384954425355)} Voice Channels', value=voicechannels)
        embed.add_field(name=f"{self.bot.get_emoji(450878790491701249)} AFK Channel & Time:", value = f"Channel: **{ctx.guild.afk_channel}**" "Time: **{} minutes**".format(int(ctx.guild.afk_timeout / 60)))
        embed.add_field(name=f'{self.bot.get_emoji(432191587850780682)} Emoji Count', value=regular_emojis + animated_emojis)
        embed.add_field(name=f'{self.bot.get_emoji(430340787121815572)} Normal Emojis', value=regular_emojis)
        embed.add_field(name=f'{self.bot.get_emoji(430853715059277863)} Animated Emojis', value=animated_emojis)
        embed.add_field(name=f'{self.bot.get_emoji(450816002331246632)} Server Region', value=str(guild.region))
        embed.add_field(name=f'{self.bot.get_emoji(450816423766523931)} Role Count', value=str(role_length))
        embed.add_field(name=f'{self.bot.get_emoji(450819025958600706)} Server Verification Level', value=verification_levels[guild.verification_level])
        embed.add_field(name=f'{self.bot.get_emoji(422810427311915009)} Explicit Content Filter', value=content_filter[guild.explicit_content_filter])
        embed.add_field(name=f'{self.bot.get_emoji(450819866598047755)} 2FA Requirement', value=mfa_levels[guild.mfa_level])
        embed.add_field(name=f'{self.bot.get_emoji(450820345000099840)} Ban Count', value=ban_count)
        embed.set_footer(text='Created - %s' % time)
        await ctx.send(embed=embed)


    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        '''Get user info for yourself or someone in the guild'''
        if user is None:
            user = ctx.author
        color = discord.Color.green()
        guild = ctx.message.guild
        roles = sorted(user.roles, key=lambda r: r.position)
        rolenames = ', '.join([r.name for r in roles if r != '@everyone']) or 'None'
        shared = sum(1 for m in self.bot.get_all_members() if m.id == user.id)
        highrole = user.top_role.name
        if highrole == "@everyone":
            role = "N/A"

        if user.avatar_url[54:].startswith('a_'):
            avi = 'https://cdn.discordapp.com/avatars/' + user.avatar_url[35:-10]
        else:
            avi = user.avatar_url

        
        time = ctx.message.created_at
        desc = f'{user.name} is currently in {user.status} mode.'
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(color=color, description=desc, timestamp=time)
        em.add_field(name=f'{self.bot.get_emoji(430850541959118880)} Username', value=f'{user.name}#{user.discriminator}')
        em.add_field(name=f'{self.bot.get_emoji(450882580716453888)} User ID', value= user.id)
        em.add_field(name=f'{self.bot.get_emoji(450867126639788038)} Servers Shared', value=f'{shared}')
        em.add_field(name=f'{self.bot.get_emoji(433736508038578179)} Highest Role', value=highrole)
        
        em.add_field(name=f'{self.bot.get_emoji(450878488736432128)} Account Created At', value = user.created_at.__format__('Date: **%d/%b/%Y**\nTime: **%H:%M:%S**'))
        em.add_field(name=f'{self.bot.get_emoji(432191587850780682)} Member Number', value=member_number)
        em.add_field(name=f'{self.bot.get_emoji(393514807371890688)} Joined At', value=user.joined_at.__format__('%d/%b/%Y at %H:%M:%S'))
        em.add_field(name=f'{self.bot.get_emoji(449683164110127104)} Roles', value=rolenames)
        em.set_footer(text = f"Member since: {user.joined_at.__format__('%d/%b/%Y at %H:%M:%S')}")
        em.set_thumbnail(url=avi or None)
        await ctx.send(embed=em)

    @commands.command()
    async def uptime(self, ctx):
        # Gets the current uptime for the bot
        timedifference_seconds = (datetime.datetime.now().second - startTime.second)
        timedifference_minutes = (datetime.datetime.now().minute - startTime.minute)
        timedifference_hours = (datetime.datetime.now().hour - startTime.hour)
        old_timedifference = (datetime.datetime.now() - startTime)
        print("I have been up for {0} hours, {1} minutes, and {2} seconds".format(timedifference_hours, timedifference_minutes, timedifference_seconds))
        await ctx.send("I have been up for {}".format(old_timedifference))

    @commands.command(aliases=['kalastats'])
    async def kala(self, ctx):
        """Get some bot stats about me!"""
        member = 0
        for i in self.bot.guilds:
            for x in i.members:
                member += 1
        color = discord.Color(value=0xe212d1)
        embed = discord.Embed(color=color, title="Kala Bot Statistics")
        embed.description = "Kala#6605 Stats"
        embed.set_thumbnail(url="https://cdn.discordapp.com/attachments/449682597937807363/450339949384826880/asdf.png")
        embed.add_field(name=f"{self.bot.get_emoji(449682671862546443)} Creator", value=f'BloodyPikachu#0638 {self.bot.get_emoji(449682671862546443)}')
        embed.add_field(name=f"{self.bot.get_emoji(450791022541406209)} Servers", value=f"{len(self.bot.guilds)}")
        embed.add_field(name=f'{self.bot.get_emoji(450791226459815936)} Users', value=member)
        embed.add_field(name=f'{self.bot.get_emoji(412747044403544074)} Ping', value=f'{self.bot.latency * 100:.4f} ms')
        embed.add_field(name=f'{self.bot.get_emoji(439557226969956363)} Version', value='0.0.1')
        embed.add_field(name=f'{self.bot.get_emoji(424265677642268676)} Start Date', value="5/27/18")
        embed.add_field(name=f'{self.bot.get_emoji(422527903658672148)} Coding Language', value=f'{self.bot.get_emoji(418934774623764491)} Python, discord.py rewrite')
        await ctx.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Info(bot))
