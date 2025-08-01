import os
import json
import pandas as pd
from dotenv import load_dotenv
from datetime import datetime, timedelta

import discord
from discord.ext import tasks, commands


class EconCalNotifications(commands.Cog):
    """
    Sends automated notification a certain amount of time before an economic event
    """

    def __init__(self, bot):
        load_dotenv()
        self.bot = bot
        self.gen_channel = int(os.getenv('general_channel'))
        
        self.check_upcoming_events.start()

        self.df = pd.read_csv('./econ_cal/csvs/econ_calendar.csv', index_col=[0])
        self.df['Time'] = pd.to_datetime(self.df['Time'], format='%H:%M:%S')


    def get_time_difference(self, time_a: datetime, time_b: datetime) -> str:
        """
        Find difference in between two times, returns string description of time difference
        """
        a = datetime.combine(datetime.now().date(), time_a.time())
        b = datetime.combine(datetime.now().date(), time_b.time())

        diff = a - b
        total_seconds = diff.total_seconds()

        hours = int(total_seconds // 3600)
        minutes = int((total_seconds % 3600) // 60)
        seconds = total_seconds if hours == 0 and minutes == 0 else int((total_seconds % 3600) % 60) 

        if hours and minutes:
            return f'{hours} {'hours' if hours > 1 else 'hour'}, {minutes} {'minutes' if minutes > 1 else 'minute'}'
        elif not hours and minutes:
            return f'{minutes} {'minutes' if minutes > 1 else 'minute'}'
        elif hours and not minutes:
            return f'{hours} {'hours' if hours > 1 else 'hour'}'
        else:
            return f'{seconds} seconds'


    async def upcoming_events(self, message: discord.Message) -> None:
        """
        On command, shows next event on the economic calendar and time remaining until release
        """
        current_time = datetime.now().replace(microsecond=0)

        for i, row in self.df.iterrows():
            if current_time.time() <= row['Time'].time():
                await message.channel.send(
                    f'Next event: {row['Event']} at {row['Time'].time().strftime('%H:%M')} (in {self.get_time_difference(row['Time'], current_time)})'
                )
                break
            else:
                continue

        if current_time.time() > self.df['Time'].iloc[-1].time():
            await message.channel.send(f'There are no more upcoming events for today. The last event was {row['Event']} at {row['Time'].time().strftime('%H:%M')}')


    @tasks.loop(minutes=5)
    async def check_upcoming_events(self) -> None:
        """
        Sends notification of next economic calendar event 10 minutes before release       
        """
        channel = self.bot.get_channel(self.gen_channel)
        current_time = datetime.now().replace(microsecond=0)
        
        for i, row in self.df.iterrows():
            target_time = datetime.combine(datetime.now().date(), row['Time'].time())

            if target_time - timedelta(minutes=10) <= current_time < target_time:
                with open('./cogs/data/events.json', 'r') as f:
                    events_json = json.load(f)
                    # Alert event only once
                    if events_json[row['Event']] == False:
                        events_json[row['Event']] = True
                        with open('./cogs/data/events.json', 'w') as f:
                            json.dump(events_json, f, indent=4)
                            
                        await channel.send(f'⌛️ Upcoming economic event: {row['Event']} at {row['Time'].time()} ⌛️')

    # Commands
    @commands.command()
    async def nextevent(self, ctx):
        await self.upcoming_events(ctx)

    @check_upcoming_events.before_loop
    async def before_announce(self):
        await self.bot.wait_until_ready()
    

async def setup(bot):
    await bot.add_cog(EconCalNotifications(bot))