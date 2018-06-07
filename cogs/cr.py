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
            skra = json.load(f.read())
        e = skra[name]
        emo = self.bot.get_emoji(int(e))
        return emo if emo is not None else None


    async def get_tag(self, id):
        y = await self.bot.db.bravo.crtags.find_one({"id": str(id)})
        return y['tag'] if y is not None else None

    @commands.command(aliases=['crsave'])
    async def save(self, ctx, crtag):
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
    async def profile(self, ctx, crtag=None):
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
            e.add_field(name='Favorite Card', value=f"{profile.stats.favoriteCard.name} {self.emoji('profile.stats.favoriteCard.name')}")
            if not profile.rank:
                globalrank = "Not ranked globally"
            else:
                globalrank = profile.rank
            e.add_field(name='Global Rank', value=f"{globalrank} {self.emoji('legendtrophy')}")
            e.add_field(name="Challenge Wins", value=f"{profile.stats.challengeWins} {self.emoji('12wins')}")
            e.add_field(name="Challenge Losses", value=f"{profile.stats.challengeLosses}")
            e.add_field(name="Max Challenge Wins", value=f"{profile.stats.challengeMaxWins} {self.emoji('12wins')}")
            e.add_field(name="Challenge Cards Won", value=f"{profile.stats.challengeCardsWon} {self.emoji('cards')}")
            e.add_field(name="Tourmanent Match Wins", value=f"{profile.stats.tournamentWins} {self.emoji('trophy')}")
            e.add_field(name="Tournament Match Losses", value=f"{profile.stats.tournamentLosses}")
            e.add_field(name="Tournament Cards Won", value=f"{profile.stats.tourmanentCardsWon} {self.emoji('12wins')}")
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

def setup(bot):
    bot.add_cog(CR(bot))
