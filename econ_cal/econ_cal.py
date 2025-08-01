import pandas as pd

import requests
from bs4 import BeautifulSoup


def econ_calendar(country: str='USD') -> pd.DataFrame:
    """
    Fetches today's economic calendar from investing.com filters by currency, filter
    set to USD by default.
    """
    url = 'https://www.investing.com/economic-calendar/'
    headers = {
        'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'Referer': 'https://www.investing.com',
        'Accept': 'application/json, text/javascript, */*; q=0.01',
        }
    
    data = {
    'country[]': '5',
    'category[]': [
        '_employment',
        '_economicActivity',
        '_inflation',
        '_credit',
        '_centralBanks',
        '_confidenceIndex',
        '_balance',
        '_Bonds',
    ],
    'importance[]': [
        '2',
        '3',
    ],
    'timeZone': '8',
    'timeFilter': 'timeRemain',
    'currentTab': 'today',
    'submitFilters': '1',
    'limit_from': '0',
}
    
    response = requests.get(url, headers=headers, data=data)
    if response.status_code != 200:
        print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    table = soup.find('table', { 'id' : 'economicCalendarData' })

    headers = []
    rows = []
    stars = []

    for i, row in enumerate(table.find_all('tr')):
        if i == 0:
            headers = [i.text.strip() for i in row.find_all('th')]
        else:
            rows.append([i.text.strip() for i in row.find_all('td')])
            elements = row.find_all(attrs={'class': 'left textNum sentiment noWrap', 'data-img_key': True})
            for element in elements:
                img_key = element.get('data-img_key')
                stars.append(int(img_key[4]))

    headers.pop(7)
    date = rows[1]
    rows = rows[2:]
    for row in rows:
        if len(row) > 6:
            row.pop(7)
        else:
            continue

    df = pd.DataFrame(columns=headers, data=rows)
    df['Imp.'] = pd.Series(stars)
    df = df.rename(columns={'Cur.': 'Country', 'Imp.': 'Stars'})
    df = df[['Time','Country','Stars','Event']]

    df = df[df['Country'].str.strip() == country].reset_index(drop=True)
    df['Stars'] = df['Stars'].apply(lambda x: int(x))
    df.index.name = date[0]

    return df