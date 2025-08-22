import re
import requests
import pandas as pd
import datetime
from bs4 import BeautifulSoup
from calendar_requests import calendar_filtered_data

def earnings() -> pd.DataFrame:
    """
    Get upcoming earnings for the current week.
    """
    url, headers, data = calendar_filtered_data('earnings-calendar','thisWeek')
    response = requests.post(url, headers=headers, data=data)

    if response.status_code != 200:
        print(response.status_code)

    json = response.json()['data']
    soup = BeautifulSoup(json, 'html.parser')

    dates = [date.text for date in soup.find_all('td', { 'class': 'theDay' })]
    tickers = [ticker.text for ticker in soup.find_all('a', { 'class': 'bold middle'})]
    companies = [company.text for company in soup.find_all('span', {'class': 'earnCalCompanyName'})]
    forecasts = [fcast.text for fcast in soup.find_all('td', { 'class': 'leftStrong'})]

    # eps and revenue have same class name, split by even and odd indexes
    even_idx = []
    odd_idx = []

    for i in range(len(forecasts)):
        if i % 2 == 0:
            even_idx.append(i)
        else:
            odd_idx.append(i)
    
    eps_fcasts = [forecasts[i].split('\xa0')[2] for i in even_idx]
    rev_fcasts = [forecasts[i].split('\xa0')[2] for i in odd_idx]

    eps_actual = [eps.text for eps in soup.find_all(class_=re.compile('eps_actual'))]
    rev_actual = [rev.text for rev in soup.find_all(class_=re.compile('rev_actual'))]
    mcaps = [mcap.text for mcap in soup.find_all('td', { 'class': 'right'}) if mcap.text]
    times = [time['data-tooltip'].split(' ')[2] for time in soup.find_all('span', {'class': 'reverseToolTip'})]



    df = pd.DataFrame()
    df['Ticker'] = pd.Series(tickers)
    df['Company'] = pd.Series(companies)
    df['EPS Forecast'] = pd.Series(eps_fcasts)
    df['EPS Actual'] = pd.Series(eps_actual)
    df['Revenue Forecast'] = pd.Series(rev_fcasts)
    df['Revenue Actual'] = pd.Series(rev_actual)
    df['Market Cap'] = pd.Series(mcaps)
    df['Time'] = pd.Series(times)
    df['Date'] = dates[0]
    
    # Change to next date when current is open and previous was close
    c = 0
    for i in range(1, len(df)):
        if df.loc[i, 'Time'] == 'open' and df.loc[i -1, 'Time'] == 'close':
            c += 1

        df.loc[i, 'Date'] = dates[c]

    df['Date'] = pd.to_datetime(df['Date'])
    df['EPS Actual'] = df['EPS Actual'].apply(lambda x: float(x) if x != '--' else x)
    df['Revenue Actual'] = df['Revenue Actual'].fillna('--')
    df = df[['Date','Ticker','Company','EPS Forecast','EPS Actual','Revenue Forecast','Revenue Actual','Market Cap','Time']]

    return df


def get_todays_earnings() -> pd.DataFrame:
    week_earnings = earnings()
    today = datetime.date.today()

    today_earnings = week_earnings[week_earnings['Date'] == str(today)].reset_index(drop=True)
    if today_earnings.empty:
        return
    else:
        return today_earnings
    
if __name__ == "__main__":

    print("THIS WEEK'S EARNINGS",'\n')
    print(earnings())
    print('\n','\n')
    print("EARNINGS TODAY", '\n')
    print(get_todays_earnings())
    print('\n','\n')