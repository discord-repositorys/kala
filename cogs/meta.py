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
import copy
import unicodedata
import inspect

class Meta:
    """Meta Commands"""
    def __init__(self, bot):
        self.bot = bot
        
    @commands.command()
    async def charinfo(self, ctx, *, characters: str):
        """Shows you information about a number of characters.
        Only up to 25 characters at a time.
        """

        def to_string(c):
            digit = f'{ord(c):x}'
            name = unicodedata.name(c, 'Name not found.')
            return f'`\\U{digit:>08}`: {name} - {c} \N{EM DASH} <http://www.fileformat.info/info/unicode/char/{digit}>'
        msg = '\n'.join(map(to_string, characters))
        if len(msg) > 2000:
            return await ctx.send('Output too long to display.')
        await ctx.send(msg)
        
    @commands.command(aliases=['invite'])
    async def join(self, ctx):
        """Joins a server."""
        perms = discord.Permissions.none()
        perms.read_messages = True
        perms.external_emojis = True
        perms.send_messages = True
        perms.manage_roles = True
        perms.manage_channels = True
        perms.ban_members = True
        perms.kick_members = True
        perms.manage_messages = True
        perms.embed_links = True
        perms.read_message_history = True
        perms.attach_files = True
        perms.add_reactions = True
        await ctx.send(f'<{discord.utils.oauth_url(self.bot.client_id, perms)}>')
        
    async def get_google_entries(self, query):
        url = f'https://www.google.com/search?q={uriquote(query)}'
        params = {
            'safe': 'on',
            'lr': 'lang_en',
            'hl': 'en'
        }

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 6.3; Win64; x64) Gecko/20100101 Firefox/53.0'
        }

        # list of URLs and title tuples
        entries = []

        # the result of a google card, an embed
        card = None

        async with self.bot.session.get(url, params=params, headers=headers) as resp:
            if resp.status != 200:
                log.info('Google failed to respond with %s status code.', resp.status)
                raise RuntimeError('Google has failed to respond.')

            root = etree.fromstring(await resp.text(), etree.HTMLParser())

            # for bad in root.xpath('//style'):
            #     bad.getparent().remove(bad)

            # for bad in root.xpath('//script'):
            #     bad.getparent().remove(bad)

            # with open('google.html', 'w', encoding='utf-8') as f:
            #     f.write(etree.tostring(root, pretty_print=True).decode('utf-8'))

            """
            Tree looks like this.. sort of..
            <div class="rc">
                <h3 class="r">
                    <a href="url here">title here</a>
                </h3>
            </div>
            """

            card_node = root.xpath(".//div[@id='rso']/div[@class='_NId']//" \
                                   "div[contains(@class, 'vk_c') or @class='g mnr-c g-blk' or @class='kp-blk']")

            if card_node is None or len(card_node) == 0:
                card = None
            else:
                card = self.parse_google_card(card_node[0])

            search_results = root.findall(".//div[@class='rc']")
            # print(len(search_results))
            for node in search_results:
                link = node.find("./h3[@class='r']/a")
                if link is not None:
                    # print(etree.tostring(link, pretty_print=True).decode())
                    entries.append((link.get('href'), link.text))

        return card, entries

        
    @commands.command(aliases=['google'])
    async def g(self, ctx, *, query):
        """Searches google and gives you top result."""
        await ctx.trigger_typing()
        try:
            card, entries = await self.get_google_entries(query)
        except RuntimeError as e:
            await ctx.send(str(e))
        else:
            if card:
                value = '\n'.join(f'[{title}]({url.replace(")", "%29")})' for url, title in entries[:3])
                if value:
                    card.add_field(name='Search Results', value=value, inline=False)
                return await ctx.send(embed=card)

            if len(entries) == 0:
                return await ctx.send('No results found... sorry.')

            next_two = [x[0] for x in entries[1:3]]
            first_entry = entries[0][0]
            if first_entry[-1] == ')':
                first_entry = first_entry[:-1] + '%29'

            if next_two:
                formatted = '\n'.join(f'<{x}>' for x in next_two)
                msg = f'{first_entry}\n\n**See also:**\n{formatted}'
            else:
                msg = first_entry

            await ctx.send(msg)
        
def setup(bot):
    bot.add_cog(Meta(bot))
