import discord
from discord.ext import commands
import random
import asyncio
import time
import traceback
import sys

class Mod:
    """Moderator Commands"""
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, user: discord.Member):
        """Kick a user from your discord server."""
        try:
            await ctx.send(f"**{user.name}** has been kicked from the server.")
            await ctx.guild.kick(user)
        except discord.Forbidden:
            await ctx.send(f"Kala lacks the permission to kick **{user.name}**.")
        except commands.errors.MissingPermissions:
            await ctx.send("You don't have the nessecary perms to do that.")

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, user: discord.Member):
        """Ban a user from your discord server."""
        try:
            await ctx.send(f'**{user.name}** is now banned from the server!')
            await ctx.guild.ban(user)
        except discord.Forbidden:
            await ctx.send(f"Kala lacks the permission to ban **{user.name}**.")
        except commands.errors.MissingPermissions:
            await ctx.send("no perms bro")

    @commands.command(pass_context=True, aliases=["clear"])
    @commands.has_permissions(manage_messages=True)
    async def purge(self, ctx, amount):
        """Clear messages from the chat"""
        try:
            x = int(amount)
            if x < 2 or x > 500:
                return await ctx.send("Must be in range of 2 to 500 messages.")
            await ctx.channel.purge(limit=x)
            await ctx.send("Cleared {} messages for you. Enjoy the clear chat!".format(amount), delete_after=5)
        except ValueError:
            await ctx.send("Please select a number.")
        except commands.errors.MissingPermissions:
            await ctx.send("You lack the permissions to use this command")
        except Exception as e:
            await ctx.send("Something went wrong. Here it is: {}".format(e))
            print(e)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def mute(self, ctx, user: discord.Member = None):
        """Mute a user. Works only for 1 channel."""
        if user is None:
            return await ctx.send("Please tag the user in order to mute them.")
        try:
            await ctx.channel.set_permissions(user, send_messages=False)
            return await ctx.send(f"{user.mention} has been muted. Unmute them when you see fit.")
        except commands.errors.MissingPermissions:
            return await ctx.send("You lack perms")
        except discord.Forbidden:
            return await ctx.send("I lack the **Manage channel** permission.")


    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def unmute(self, ctx, user: discord.Member = None):
        """Unmute a user from 1 channel."""
        if user is None:
            return await ctx.send("Please tag the user in order to unmute them")
        try:
            await ctx.channel.set_permissions(user, send_messages=True)
            return await ctx.send(f"{user.mention} has been unmuted. Enjoy freedom. While it lasts.")
        except commands.errors.MissingPermissions:
            return await ctx.send("You lack perms")
        except discord.Forbidden:
            return await ctx.send("I lack the **Manage Channel** permission.")

    @commands.command()
    @commands.has_permissions(ban_members = True)
    async def lockdown(self, ctx, action):
        """Prevents anyone from chatting in the current channel."""
        if action.lower() == 'on':
            msg = await ctx.send("Locking down the channel...")
            for x in ctx.guild.members:
                await ctx.channel.set_permissions(x, send_messages=False)
            return await msg.edit(content="The channel has been successfully locked down. :lock: ")
        elif action.lower() == 'off':
            msg = await ctx.send("Unlocking the channel...")
            for x in ctx.guild.members:
                await ctx.channel.set_permissions(x, send_messages=True)
            return await msg.edit(content="The channel has been successfully unlocked. :unlock: ")
        else:
            return await ctx.send("Lockdown command:\n*lockdown [on/off]")

    @commands.command()
    @commands.has_permissions(administrator = True)
    async def dm(self, ctx, user: discord.Member, *, msg: str):
        """Dm someone. Usage: [prefix]dm [tag person] [msg]"""
        try:
            await user.send(msg)
            await ctx.message.delete()            
            await ctx.send("DM sent.")
        except commands.MissingPermissions:
            await ctx.send("You lack permission to use this command.")
        except:
            await ctx.send("Error! Usage: [prefix]dm [tag person] [msg]")

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

def setup(bot):
    bot.add_cog(Mod(bot))
