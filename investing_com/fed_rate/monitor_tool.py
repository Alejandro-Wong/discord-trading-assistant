import requests
import pandas as pd
from bs4 import BeautifulSoup



def fed_rate_monitor() -> pd.DataFrame:
    """
    Get the probabilities for different target rates for the next several Fed Interest Rate Decisions.
    """
    url = 'https://www.investing.com/central-banks/fed-rate-monitor'

    headers = {
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
        'referer': 'https://www.investing.com/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
    }

    response = requests.post(url, headers=headers)

    if response.status_code != 200:
        print(response.status_code)

    soup = BeautifulSoup(response.text, 'html.parser')

    info_fed = soup.find_all('div', {'class': 'infoFed'})
    datetime = []
    for row in info_fed:
        filtered = [item.strip() for item in row.text.split('\n') if item.strip()]
        datetime.append(filtered[1][:-3])

    tables = soup.find_all('table', {'class': 'fedRateTbl'})
    target_rate = []
    curr_prob = []
    prev_day_prob = []
    prev_week_prob = []

    for table in tables:
        tr = table.find_all('tr')
        for row in tr:
            if row.find('td'):
                td = row.find_all('td') 
                target_rate.append(td[0].text.strip('\t\n'))
                curr_prob.append(td[1].text.strip('%'))
                prev_day_prob.append(td[2].text.strip('%'))
                prev_week_prob.append(td[3].text.strip('%'))

    # DataFrame construction
    data = {
        'Target': pd.Series(target_rate), 
        'Current Probability %': pd.Series(curr_prob),
        'Prev Day Probability %': pd.Series(prev_day_prob),
        'Prev Week Probability %': pd.Series(prev_week_prob)
    }

    df = pd.DataFrame(data)

    # Change to next date when previous target is 4.25 - 4.50 or 4.50 - 4.75
    count = 0
    df['Datetime'] = datetime[0]
    for i in range(1, len(df)):
        if df.loc[i - 1, 'Target'] == '4.25 - 4.50' or df.loc[i - 1, 'Target'] == '4.50 - 4.75':
            count += 1
        
        df.loc[i, 'Datetime'] = datetime[count]

    # Adjust order of df
    df = df[['Datetime','Target','Current Probability %','Prev Day Probability %','Prev Week Probability %']]

    # Adjust data types
    df['Datetime'] = pd.to_datetime(df['Datetime'], format='%b %d, %Y %I:%M%p')
    df['Current Probability %'] = df['Current Probability %'].apply(lambda x: float(x))
    df['Prev Day Probability %'] = df['Prev Day Probability %'].apply(lambda x: float(x))
    df['Prev Week Probability %'] = df['Prev Week Probability %'].apply(lambda x: float(x))

    return df

if __name__ == "__main__":
    print(fed_rate_monitor())