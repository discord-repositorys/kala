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
    
    

    @commands.command(pass_context=True, aliases=['si', 'sinfo'])
    async def serverinfo(self, ctx, *, guild_name = None):
        """Lists some info about the current or passed server."""
        
        # Check if we passed another guild
        guild = None
        if guild_name == None:
            guild = ctx.guild
        else:
            for g in self.bot.guilds:
                if g.name.lower() == guild_name.lower():
                    guild = g
                    break
                if str(g.id) == str(guild_name):
                    guild = g
                    break
        if guild == None:
            # We didn't find it
            await ctx.send("I couldn't find that guild...")
            return
        
        server_embed = discord.Embed(color=ctx.author.color)
        server_embed.title = guild.name
        
        
        
        
        server_embed.description = "Server Stats"
        online_members = 0
        bot_member     = 0
        bot_online     = 0
        for member in guild.members:
            if member.bot:
                bot_member += 1
                if not member.status == discord.Status.offline:
                        bot_online += 1
                continue
            if not member.status == discord.Status.offline:
                online_members += 1
        # bot_percent = "{:,g}%".format((bot_member/len(guild.members))*100)
        user_string = "{:,}/{:,} online ({:,g}%)".format(
                online_members,
                len(guild.members) - bot_member,
                round((online_members/(len(guild.members) - bot_member) * 100), 2)
        )
        b_string = "bot" if bot_member == 1 else "bots"
        user_string += "\n{:,}/{:,} {} online ({:,g}%)".format(
                bot_online,
                bot_member,
                b_string,
                round((bot_online/bot_member)*100, 2)
        )
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
        #server_embed.add_field(name="Members", value="{:,}/{:,} online ({:.2f}%)\n{:,} {} ({}%)".format(online_members, len(guild.members), bot_percent), inline=True)
        server_embed.add_field(name="Members ({:,} total)".format(len(guild.members)), value=user_string, inline=True)
        server_embed.add_field(name="Roles", value=str(len(guild.roles)), inline=True)
        chandesc = "{:,} text, {:,} voice".format(len(guild.text_channels), len(guild.voice_channels))
        server_embed.add_field(name="Channels", value=chandesc, inline=True)
        server_embed.add_field(name="Default Role", value=guild.default_role, inline=True)
        server_embed.add_field(name="Owner", value=guild.owner.name + "#" + guild.owner.discriminator, inline=True)
        server_embed.add_field(name="AFK Channel", value=guild.afk_channel, inline=True)
        server_embed.add_field(name="Verification", value=verification_levels[guild.verification_level])
        server_embed.add_field(name="Explicit Content Filter", value=content_filter[guild.explicit_content_filter])
        server_embed.add_field(name="2FA Requirement", value=mfa_levels[guild.mfa_level])
        server_embed.add_field(name="Ban Count", value=ban_count)
        server_embed.add_field(name="Voice Region", value=guild.region, inline=True)
        server_embed.add_field(name="Considered Large", value=guild.large, inline=True)
	# Find out where in our join position this server is
        joinedList = []
        popList    = []
        for g in self.bot.guilds:
            joinedList.append({ 'ID' : g.id, 'Joined' : g.me.joined_at })
            popList.append({ 'ID' : g.id, 'Population' : len(g.members) })
        
        # sort the guilds by join date
        joinedList = sorted(joinedList, key=lambda x:x['Joined'])
        popList = sorted(popList, key=lambda x:x['Population'], reverse=True)
        
        check_item = { "ID" : guild.id, "Joined" : guild.me.joined_at }
        total = len(joinedList)
        position = joinedList.index(check_item) + 1
        server_embed.add_field(name="Join Position", value="{:,} of {:,}".format(position, total), inline=True)
        
        # Get our population position
        check_item = { "ID" : guild.id, "Population" : len(guild.members) }
        total = len(popList)
        position = popList.index(check_item) + 1
        server_embed.add_field(name="Population Rank", value="{:,} of {:,}".format(position, total), inline=True)
        
        emojitext = ""
        emojicount = 0
        for emoji in guild.emojis:
            if emoji.animated:
                emojiMention = "<a:"+emoji.name+":"+str(emoji.id)+">"
            else:
                emojiMention = "<:"+emoji.name+":"+str(emoji.id)+">"
            test = emojitext + emojiMention
            if len(test) > 1024:
                # TOOO BIIIIIIIIG
                emojicount += 1
                if emojicount == 1:
                    ename = "Emojis ({:,} total)".format(len(guild.emojis))
                else:
                    ename = "Emojis (Continued)"
                server_embed.add_field(name=ename, value=emojitext, inline=True)
                emojitext=emojiMention
            else:
                emojitext = emojitext + emojiMention

        if len(emojitext):
            if emojicount == 0:
                emojiname = "Emojis ({} total)".format(len(guild.emojis))
            else:
                emojiname = "Emojis (Continued)"
            server_embed.add_field(name=emojiname, value=emojitext, inline=True)


        if len(guild.icon_url):
            server_embed.set_thumbnail(url=guild.icon_url)
        else:
            # No Icon
            server_embed.set_thumbnail(url=ctx.author.default_avatar_url)
        server_embed.set_footer(text="Server ID: {}".format(guild.id))
        await ctx.channel.send(embed=server_embed)

    @commands.command(aliases=['ui', 'user'])
    async def userinfo(self, ctx, user: discord.Member = None):
        '''Get user info for yourself or someone in the guild'''
        if user is None:
            user = ctx.author
		if user.game is None or user.game.url is None:
	    	if str(user.status) == "online":
	    	status_color = embed_color_success
	    	status_name = "Online"
		elif str(user.status) == "idle":
	    	status_color = embed_color_attention
	    	status_name = "Away / Idle"
		elif str(user.status) == "dnd":
			status_color = embed_color_error
			status_name = "Do Not Disturb"
		elif str(user.status) == "offline" or str(user.status) == "invisible":
			status_color = 0x000000
			status_name = "Offline"
		else:
	    	status_color = 0x593695
	    	status_name = "Streaming"
		if user.game is None:
			activity = f'**Doing**: Absolutely Nothing!'
		elif user.game.url is None:
			activity = f'**Playing**: {member.game}'
		else:
			activity = f'**Streaming**: [{member.game}]({member.game.url})'
        color = ctx.author.color
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
        desc = f'{user.name} is currently in {status_name} mode.'
        member_number = sorted(guild.members, key=lambda m: m.joined_at).index(user) + 1
        em = discord.Embed(color=color, description=desc, timestamp=time)
        em.add_field(name=f'Username', value=f'{user.name}#{user.discriminator}')
        em.add_field(name=f'User ID', value= user.id)
        em.add_field(name=f'Servers Shared', value=f'{shared}')
        em.add_field(name=f'Highest Role', value=highrole)
        em.add_field(name='Activity', value=activity
        em.add_field(name=f'Account Created At', value = user.created_at.__format__('Date: **%d/%b/%Y**\nTime: **%H:%M:%S**'))
        em.add_field(name=f'Member Number', value=member_number)
        em.add_field(name=f'Joined At', value=user.joined_at.__format__('%d/%b/%Y at %H:%M:%S'))
        em.add_field(name=f'Roles', value=rolenames)
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
        embed.add_field(name=f'{self.bot.get_emoji(439557226969956363)} Version', value='0.0.2')
        embed.add_field(name=f'{self.bot.get_emoji(424265677642268676)} Start Date', value="5/27/18")
        embed.add_field(name=f'{self.bot.get_emoji(422527903658672148)} Coding Language', value=f'{self.bot.get_emoji(418934774623764491)} Python, discord.py rewrite')
        await ctx.send(embed=embed)

    

def setup(bot):
    bot.add_cog(Info(bot))
