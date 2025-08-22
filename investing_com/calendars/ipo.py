import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from calendar_requests import calendar_filtered_data


def ipo_calendar(timeframe: str = 'upcoming') -> pd.DataFrame:
    """
    Upcoming and Recent IPOs
    """
    
    url, headers, data = calendar_filtered_data('ipo-calendar', f'{timeframe}')
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print(response.status_code)

    json = response.json()['data']
    soup = BeautifulSoup(json, 'html.parser')

    rows = soup.find_all('tr')
    new_rows = []
    for row in rows:
        filtered = [item.strip() for item in row.text.split('\n') if item.strip()]
        new_rows.append(filtered)

    columns = ['Date', 'Company', 'Ticker', 'Exchange', 'Value', 'IPO Price', 'Last']
    
    df = pd.DataFrame(new_rows, columns=columns)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Ticker'] = df['Ticker'].apply(lambda x: x[1:-1])

    return df


if __name__ == "__main__":

    print('UPCOMING IPOS','\n')
    print(ipo_calendar())
    print('\n','\n')
    print('RECENT IPOS','\n')
    print(ipo_calendar('recent'))
    print('\n','\n')