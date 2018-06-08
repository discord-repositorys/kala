import discord
import sys
import os
import json
import ezjson
import clashroyale
import traceback
from discord.ext import commands
from motor.motor_asyncio import AsyncIOMotorClient


class CR:
    def __init__(self, bot):
        self.bot = bot
        self.token = os.environ.get('CRAPI')
        self.client = clashroyale.Client(token=self.token, is_async=True)

    
    def check_tag(self, crtag):
        for char in crtag:
            if char.upper() not in '0289PYLQGRJCUV':
                return False
            return True

    def emoji(self, name):
        with open("emojiscr.json") as f:
            skra = json.loads(f.read())
        e = skra[str(name)]
        emo = self.bot.get_emoji(int(e))
        return emo if emo is not None else None


    async def get_tag(self, id):
        y = await self.bot.db.bravo.crtags.find_one({"id": str(id)})
        return y['tag'] if y is not None else None

    @commands.command()
    async def crsave(self, ctx, crtag):
        """Save a Clash Royale tag to your Discord account."""
        await ctx.trigger_typing()
        if crtag is None:
            e = discord.Embed(color=ctx.author.color, title="Please enter a tag to save.")
            e.description = f'Example: {ctx.prefix}save #tag'
        crtag = crtag.strip('#').replace("O", "0")
        if not self.check_tag(crtag):
            e = discord.Embed(color=ctx.author.color, title="Invalid Tag.") 
            e.description = "Please make sure you have enterd your tag correctly." 
            return await ctx.send(embed=e)
        await self.bot.db.bravo.crtags.update_one({"id": str(ctx.author.id)}, {"$set": {"tag": crtag}}, upsert=True)
        e = discord.Embed(color=ctx.author.color, title='Saved!')
        e.description = 'Your Clash Royale tag has been saved!'
        await ctx.send(embed=e)
    
    
    @commands.command()
    async def crprofile(self, ctx, crtag=None):
        """Get your Clash Royale stats. All in one command."""
        await ctx.trigger_typing()
        try:
            if crtag is None:
                crtag = await self.get_tag(ctx.author.id)
                if not crtag:
                    e = discord.Embed(color=ctx.author.color, title="Tag not found!")
                    e.description = 'No Clash Royale tag was found for you. Please save your tag, then try again.'
                    await ctx.send(embed=e)
            try:
                profile = await self.client.get_player(crtag)
            except (clashroyale.errors.NotResponding, clashroyale.errors.ServerError) as f:
                print(f)
                e = discord.Embed(color=ctx.author.id, title='API Error!')
                e.description = f'{f.code}:\n{f.error}'
                return await ctx.send(embed=e)
            e = discord.Embed(color=ctx.author.color, title=f'{profile.name} (#{profile.tag})')
            e.description = 'Profile powered by: [RoyaleAPI.com](https://royaleapi.com/)'
            e.add_field(name=f'Player {profile.name}', value=ctx.author)
            e.add_field(name='Trophies', value=f"{profile.trophies} {self.emoji('trophy')}")
            e.add_field(name='Personal Best', value=f"{profile.stats.maxTrophies} {self.emoji('trophy')}")            
            e.add_field(name='Arena', value=f'{profile.arena.name}')
            e.add_field(name='XP Level', value=f"{profile.stats.level} {self.emoji('xp')}")
            e.add_field(name="Total Played Games", value=f"{profile.games.total} {self.emoji('battle')}")
            e.add_field(name="Wins", value=f"{profile.games.wins} {self.emoji('battle')}")
            e.add_field(name='Losses', value=f"{profile.games.losses}")
            e.add_field(name='Draws', value=f"{profile.games.draws} {self.emoji('battle')}")
            e.add_field(name="Win Percentage", value=f"{profile.games.winsPercent * 100}% {self.emoji('battle')}")
            e.add_field(name="Loss Percentage", value=f"{profile.games.lossesPercent * 100}% {self.emoji('battle')}")
            e.add_field(name='Draw Percentage', value=f"{profile.games.drawsPercent * 100}% {self.emoji('battle')}")
            e.add_field(name='Win Rate', value=f"{(profile.games.wins / (profile.games.wins + profile.games.losses) * 100):.3f}% {self.emoji('battle')}")
            if not profile.rank:
                globalrank = "Not ranked globally"
            else:
                globalrank = profile.rank
            e.add_field(name='Global Rank', value=f"{globalrank} {self.emoji('legendtrophy')}")
            e.add_field(name="Max Challenge Wins", value=f"{profile.stats.challengeMaxWins} {self.emoji('12wins')}")
            e.add_field(name="Challenge Cards Won", value=f"{profile.stats.challengeCardsWon} {self.emoji('cards')}")
            e.add_field(name="Tournament Cards Won", value=f"{profile.stats.tournamentCardsWon} {self.emoji('12wins')}")
            try:
                clan = await profile.get_clan()
                e.add_field(name=f"Clan ({clan.name})", value=f"{clan.name} #{clan.tag}")
                clanroles = {
                    "member": "Member",
                    "elder": "Elder",
                    "Leader": "Leader",
                    "coLeader": "Co-Leader"
                }
                e.add_field(name="Role", value=f"{clanroles[profile.clan.role]}")
                e.add_field(name="Clan Trophies", value=f"{clan.score} {self.emoji('trophy')}")
                e.add_field(name="Members", value=f"{len(clan.members)}/50")
                e.add_field(name="Donated Cards", value=profile.clan.donations)
                e.add_field(name="Received Cards", value=profile.clan.donationsReceived)
                e.set_footer(text="Made with <3 by BloodyPikachu, 4JR, and dat banana boi")
            except AttributeError:
                e.add_field(name="Clan", value=f"No Clan")
            await ctx.send(embed=e)
        except Exception as e:
            print(traceback.format_exc())
            
            
    @commands.command()
    async def crclan(self, ctx, clantag=None):
        """Grab some info about a clan from hotdig.info ;)"""
        await ctx.trigger_typing()
        if clantag is None:
            crtag = await self.get_tag(ctx.author.id)
            if not crtag:
                e = discord.Embed(title="Oh No!", color=ctx.author.color)
                e.add_field(name="No tag saved!", value=f"Please use {ctx.prefix}crsave to save your Clash Royale tag.")
                return await ctx.send(embed=e)
        try:
            profile = await self.client.get_player(crtag)
            clan = await profile.get_clan()
        except AttributeError:
            em = discord.Embed(color=ctx.author.color, title="Um...Really?")
            em.add_field(name="Uh...", value="I think you have to be in a clan for this to work.")
            await ctx.send(embed=em)
        embed.description = f'{clan.description}'
        embed.add_field(name='Clan Trophies', value=f'{clan.score}')
        embed.add_field(name='Members', value=f'{clan.memberCount}/50')
        embed.add_field(name='Type', value=f'{clan.type}')
        embed.add_field(name='Weekly Donations', value=f'{clan.donations}')
        embed.add_field(name='Location', value=f'{clan.location.name}')
        if not clan.war:
            war = "Not in Progress"
        else:
            if clan.war.state == "warDay":
                war = "War Day :crossed_swords:"
            elif clan.war.state == "collectionDay":
                war = f"Collection Day {self.emoji('deck')}"
        embed.add_field(name="Clan War Status", value=war)
        embed.add_field(name='Trophy Requirement', value=f'{clan.requiredScore}')
        embed.set_thumbnail(url=f'{clan.badge.image}')
        await ctx.send(embed=embed)

def setup(bot):
    bot.add_cog(CR(bot))
