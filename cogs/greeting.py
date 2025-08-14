import os 
import json
from datetime import datetime

import discord
from discord.ext import commands


class Greeting(commands.Cog):
    """
    Greet bot to get relevant market info
    """

    def __init__(self, bot):
        self.bot = bot
        self.greetings = ['hello','good morning','morning','yo','hey','hi','ayo','afternoon','evening','sup']
        self.signoffs = ['later','bye','cya','goodnight','good night','night','goodbye','peace','farewell']
        self.png_path = './market_overview/pngs/'


    async def read_headlines(self, message: discord.Message) -> None:
        """
        Lists latest 10 headlines from Finviz's Stocks News page 
        """
        await message.channel.send("Here are the latest headlines from Finviz's stock news page: ")

        with open('./cogs/data/latest_headlines.txt', 'r') as f:
            latest_headlines = f.read()

        await message.channel.send(f'{latest_headlines}')


    async def post_linecharts(self, message: discord.Message):
        """
        Shows performance comparison line charts for index and SPDR sectors ETFs
        """
        for filename in os.listdir(self.png_path):
            if filename.endswith('.png'):
                await message.channel.send(file=discord.File(f'{self.png_path}{filename}'))


    async def show_events(self, message: discord.Message) -> None:
        """
        Shows today's economic calendar events
        """
        await message.channel.send(f"These are the economic calendar events for today, {datetime.now().date()}: ")

        with open('./cogs/data/econ_cal_today.txt', 'r') as f:
            econ_cal_today = f.read()

        await message.channel.send(f'{econ_cal_today}')


    def greeting(self):
        """
        Greets user on login
        """
        now = datetime.now().replace(microsecond=0)

        morning = datetime(now.year, now.month, now.day, 5, 0, 0)
        afternoon = datetime(now.year, now.month, now.day, 12, 0, 0)
        evening = datetime(now.year, now.month, now.day, 17, 0 ,0)

        if morning <= now <= afternoon:
            return 'Good Morning'
        elif afternoon <= now <= evening:
            return 'Good Afternoon'
        else:
            return 'Good Evening'
        

    @commands.Cog.listener()
    async def on_message(self, message: discord.Message):
        """
       Triggers relevant market information on greeting
        """
        if message.author == self.bot.user:
            return

        if message.content.lower() in self.greetings:

            greeting = self.greeting()
            await message.channel.send(f'{greeting}')
            await self.read_headlines(message)
            await self.post_linecharts(message)
            await self.show_events(message)

            # else:
            #     await message.channel.send('Hello again')

        else:
            return
                
        await self.bot.process_commands(message)


async def setup(bot):
    await bot.add_cog(Greeting(bot))