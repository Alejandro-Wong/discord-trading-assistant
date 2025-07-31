import os 
import json

import discord
from discord.ext import commands

from market_overview.market_overview import refresh_charts


class PMO(commands.Cog):
    """
    Displays min-max-normalized multi-line line charts comparing the performances
    of:
    Major Index(ETFs) - SPY, QQQ, DIA, IWM
    SPDR Sectors - XLU, XLY, XLK... etc
    """

    def __init__(self, bot):
        self.bot = bot
        self.png_path = './market_overview/pngs/'
        

    @commands.Cog.listener()
    async def on_ready(self):
        """
        Updates index and sector ETFs performance comparison charts       
        """
        refresh_charts()
        print("Index and Sector Performance charts have been updated")


    async def post_linecharts(self, message: discord.Message):
        """
        Posts index and sector ETFs performance comparison charts to channel
        """
        for filename in os.listdir(self.png_path):
            if filename.endswith('.png'):
                await message.channel.send(file=discord.File(f'{self.png_path}{filename}'))


    # Commands            
    @commands.command()
    async def mktoverview(self, ctx):
        await self.post_linecharts(ctx)


async def setup(bot):
    await bot.add_cog(PMO(bot))       