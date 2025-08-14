import os
import json
import pandas as pd
from datetime import datetime 
from dotenv import load_dotenv

import discord
from discord.ext import tasks, commands

from news.finviz import Finviz
from funcs import stringlist_to_list


class Headlines(commands.Cog):
    """
    Fetch most recent ten headlines from the Finviz stock news page.
    """

    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.gen_channel = int(os.getenv('general_channel'))
        # self.stocks_news = None
        self.most_recent_news.start()
        self.active_position_news.start()
        

    async def read_headlines(self, message: discord.Message) -> None:
        """
        On command, shows latest 10 headlines        
        """
        await message.channel.send("Here are the latest headlines from Finviz's stock news page: ")

        with open('./cogs/data/latest_headlines.txt', 'r') as f:
            latest_headlines = f.read()

        await message.channel.send(f'{latest_headlines}')


    # Fetch headlines
    @tasks.loop(minutes=5)
    async def most_recent_news(self):
        """
        Constantly fetches latest 10 headlines, saves to txt file 
        """
        stocks_news = Finviz().stocks_news()[:10]
        stocks_news.to_csv('./news/csvs/latest_headlines.csv')
        
        headlines = []
        for i, row in stocks_news.iterrows():
            ticker = ', '.join(row['Ticker']) if isinstance(row['Ticker'], list) else row['Ticker']
            headlines.append(f'🔹 {row['Headline']} - **{ticker}** - {row['Time Elapsed']} ago\n')

        headlines_str = ''.join(headlines)

        with open('./cogs/data/latest_headlines.txt', 'w') as f:
            f.write(headlines_str)

        print(f'Headlines have been updated: {datetime.now().time().replace(microsecond=0)}')


    # Active position headlines
    @tasks.loop(minutes=5)
    async def active_position_news(self):
        """
        Checks latest headlines for tickers that are in active positions. Saves relevant headlines to txt              
        """
        channel = self.bot.get_channel(self.gen_channel)
        latest = pd.read_csv('./finviz/csvs/latest_headlines.csv', index_col=[0])
        latest['Ticker'] = latest['Ticker'].apply(stringlist_to_list)

        with open('./cogs/data/active_positions.json', 'r') as f:
            positions = json.load(f)['active']

        headlines = []
        for i, row in latest.iterrows():
            ticker = row['Ticker']
            if isinstance(ticker, list):
                for t in ticker:
                    if t in positions:
                        headlines.append(f'🔹 {row['Headline']} - **{t}** - {row['Time Elapsed']} ago\n')
            else:
                if ticker in positions:
                    headlines.append(f'🔹 {row['Headline']} - **{ticker}** - {row['Time Elapsed']} ago\n')

        if headlines:
            headlines_str = ''.join(headlines)
            await channel.send(headlines_str)
            
            # with open('./cogs/data/position_headlines.txt', 'w') as f:
            #     f.write(headlines_str)


    # Commands
    @commands.command()
    async def headlines(self, ctx):
        await self.read_headlines(ctx)
 
    @most_recent_news.before_loop
    async def before_headlines(self):
        await self.bot.wait_until_ready()

    @active_position_news.before_loop
    async def before_active(self):
        await self.bot.wait_until_ready()

async def setup(bot):
    await bot.add_cog(Headlines(bot))