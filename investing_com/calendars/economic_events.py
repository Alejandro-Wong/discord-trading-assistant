import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from calendar_requests import calendar_filtered_data


def econ_calendar() -> pd.DataFrame:
    """
    Economic Calendar for the current week
    """
    url, headers, data = calendar_filtered_data('economic-calendar','thisWeek')
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print(response.status_code)

    json = response.json()['data']
    soup = BeautifulSoup(json, 'html.parser')

    dates = [date.text for date in soup.find_all('td', { 'class': 'theDay' })]
    times = [time.text for time in soup.find_all('td', { 'class': 'first'})]
    curr = [cur.text[-3:] for cur in soup.find_all('td', { 'class': 'flagCur'})]
    stars = [star for star in soup.find_all('td', { 'class': 'sentiment', 'data-img_key': True})]
    num_stars = []
    for star in stars:
        img_key = star.get('data-img_key')
        num_stars.append(int(img_key[4]))
    events = [event.text.strip() for event in soup.find_all('td', { 'class': 'event'})]

    df = pd.DataFrame()
    df['Time'] = pd.to_datetime(pd.Series(times), format="%H:%M").dt.time
    df['Country'] = pd.Series(curr)
    df['Stars'] = pd.Series(num_stars)
    df['Event'] = pd.Series(events)

    df['Date'] = dates[0]
    c = 0
    for i in range(1, len(df)):
        current_time = df.loc[i, 'Time']
        prev_time = df.loc[i - 1, 'Time']

        if current_time < prev_time and c < len(dates):
            c += 1
        
        df.loc[i, 'Date'] = dates[c]

    df = df[['Date','Time','Country','Stars','Event']]
    df['Date'] = pd.to_datetime(df['Date'])

    return df


def get_todays_events() -> pd.DataFrame:
    full_calendar = econ_calendar()
    today = datetime.date.today()

    today_events = full_calendar[full_calendar['Date'] == str(today)].reset_index(drop=True)
    if today_events.empty:
        return 
    else:
        return today_events


if __name__ == "__main__":

    print('ECONOMIC CALENDAR FOR THIS WEEK', '\n')
    print(econ_calendar())
    print('\n','\n')
    print("TODAY'S ECONOMIC EVENTS", '\n')
    print(get_todays_events())
    print('\n','\n')