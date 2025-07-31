import json
import discord
from discord.ext import  commands
from thinkorswim.active_positions import active_positions


class Positions(commands.Cog):
    """
    Information on current positions
    """

    def __init__(self, bot):
        self.bot = bot


    async def get_positions(self, message: discord.Message) -> None:
        """
        Shows active positions       
        """
        with open('./cogs/data/active_positions.json', 'r') as f:
            positions = json.load(f)['active']

            await message.channel.send(f'Current active positions: {', '.join(positions)}')


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Gets active positions, saves as json
        """
        active = active_positions()
        tickers = [ticker for ticker in active['index']]

        active_json = {}
        active_json['active'] = tickers
        with open ('./cogs/data/active_positions.json', 'w') as f:
            json.dump(active_json, f)
        print('Active positions updated')
    

    # Commands
    @commands.command()
    async def positions(self, ctx):
        await self.get_positions(ctx)


async def setup(bot):
    await bot.add_cog(Positions(bot))