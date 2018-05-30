from discord.ext import commands

class Context(commands.Context):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
    async def purge(self, limit):
        '''Shortcut to ctx.channel.purge'''
        return await self.channel.purge(limit=limit)
        
    @property
    def session(self):
        '''Returns bot session.'''
        return self.bot.session
    
    @property
    def db(self):
        '''Another shorter access to the database.'''
        return self.bot.db.bravo_db
