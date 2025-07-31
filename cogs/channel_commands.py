import discord
from discord.ext import commands

class ChannelCommands(commands.Cog):
    """
    General commands for channel
    """

    def __init__(self, bot):
        self.bot = bot
    
    
    @commands.command()
    async def clear(self, ctx):
        await ctx.channel.purge()

async def setup(bot):
    await bot.add_cog(ChannelCommands(bot))