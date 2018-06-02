import discord
from discord.ext import commands
import asyncio
import collections
import statistics
from datetime import datetime


from discord.ext.commands import command

class Latency:

    def __init__(self, bot):
        self.bot = bot
        self.message_latencies = collections.deque(maxlen=500)

    async def on_message(self, message):
        now = datetime.utcnow()
        self.message_latencies.append((now, now - message.created_at))

    @commands.command(aliases=['msgl'])
    async def messagelat(self, ctx):
        """Mean latency for last 500 messages."""
        embed = discord.Embed(color=ctx.author.color, title='Last 500 messages latency')
        embed.description = "{:.2f}ms".format(
            1000 * statistics.mean(
                lat.total_seconds() for ts, lat in self.message_latencies))
        await ctx.send(embed = embed)

    @commands.command()
    async def rtt(self, ctx):
        """Measures delay between message and reply.
        RCV: Discord message timestamp -> Bot processes message
             (This is affected by clock being out of sync with Discord)
        M2M: Discord generates message timestamp -> Discord generates reply timestamp
        RTT: Bot sends message -> Bot recieves own message
        """
        recv_time = ctx.message.created_at
        msg_content = "..."

        task = asyncio.ensure_future(ctx.bot.wait_for(
            "message", timeout=15,
            check=lambda m: (m.author == ctx.bot.user and
                             m.content == msg_content)))
        now = datetime.utcnow()
        sent_message = await ctx.send(msg_content)
        await task
        rtt_time = datetime.utcnow()
        embed = discord.Embed(color=ctx.author.color, title='Ping times')
        embed.description = content="RCV: {:.2f}ms,\nM2M: {:.2f}ms,\nRTT: {:.2f}ms".format(
                (now - recv_time).total_seconds() * 1000,
                (sent_message.created_at - recv_time).total_seconds() * 1000,
                (rtt_time - now).total_seconds() * 1000
            )
        await ctx.send(embed=embed)
def setup(bot):
    bot.add_cog(Latency(bot))
