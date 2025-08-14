import json
import pandas as pd
from datetime import datetime 

import discord
from discord.ext import commands

from econ_cal.econ_cal import econ_calendar


class EconomicCalendar(commands.Cog):
    """
    Fetch economic calendar events from investing.com
    """

    def __init__(self, bot):
        self.bot = bot


    @commands.Cog.listener()
    async def on_ready(self):
        """
        Fetches, then creates txt + csv files for today's economic calendar
        """
        econ_cal = econ_calendar()
        econ_cal['Time'] = pd.to_datetime(econ_cal['Time'], format='%H:%M')
        econ_cal['Time'] = econ_cal['Time'].apply(lambda x: x.time())
        current_time = datetime.now().replace(microsecond=0)

        events = []
        events_json = {}
        for i, row in econ_cal.iterrows():
            event_time = datetime.combine(datetime.now().date(), row['Time'])
            events.append(f'🔸 {row['Time']} - {row['Event']} - {''.join(['⭐️' for i in range(row['Stars'])])}\n')

            if current_time < event_time:
                events_json[row['Event']] = False
            else: 
                events_json[row['Event']] = True

        events_str = ''.join(events)

        with open('./cogs/data/econ_cal_today.txt', 'w') as f:
            f.write(events_str)

        with open('./cogs/data/events.json', 'w') as f:
            json.dump(events_json, f, indent=4)
        
        econ_cal.to_csv('./econ_cal/csvs/econ_calendar.csv')
        print(f'Economic Calendar has been updated for today {datetime.now().date()}')


    async def show_events(self, message: discord.Message) -> None:
        """
        On command, shows full list of today's economic calendar events
        """
        with open('./cogs/data/econ_cal_today.txt', 'r') as f:
            econ_cal_today = f.read()

        await message.channel.send(f"Economic Calendar events for {datetime.now().date()}")
        await message.channel.send(f'{econ_cal_today}')
            

    # Commands
    @commands.command()
    async def events(self, ctx):
        await self.show_events(ctx)
    

async def setup(bot):
    await bot.add_cog(EconomicCalendar(bot))