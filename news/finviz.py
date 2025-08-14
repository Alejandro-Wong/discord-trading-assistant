import pandas as pd
from pandas import DataFrame


import requests
from bs4 import BeautifulSoup


import news.screener_params as sp


class Finviz:
    """
    
    """


    def __init__(self):

        self.headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
            'Referer': 'https://finviz.com',
            'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7',
            'Sec-Ch-Ua': 'Not)A;Brand";v="8", "Chromium";v="138'
        }



    def build_url(self, signal: str=None, filters: list[str]=None, order_by: str=None) -> str:
        """
            Constructs URL for screener by adding all applicaple parameters to a list.
            Returns joined list for final URL
        """
        url_parts = [sp.base_url]

        # Signal
        if signal:
            url_parts.extend([sp.signal_query, sp.signals[signal]])
        
        # Filters
        if filters:
            url_parts.append(sp.filter_query)
            if len(filters) == 1:
                url_parts.append(sp.search_filters(filters[0]))
            elif len(filters) == 2:
                url_parts.extend([sp.search_filters(filters[0]), sp.comma, sp.search_filters(filters[1])])
            else:
                url_parts.append(sp.search_filters(filters[0]))
                for filter in filters[1:]:
                    url_parts.append(sp.comma_multi)
                    url_parts.append(sp.search_filters(filter))

        # Order
        if order_by:
            url_parts.extend([sp.order_query, order_by])

        return ''.join(url_parts)


    def screener(self, signal: str=None, filters: list[str]=None, order_by: str=None) -> pd.DataFrame:
        """
        DataFrame of Finviz free screener results. 
        For now, only allows filtering by Signal (list of pre-made signals)
        and ordering results by columns.
        """ 
        url = self.build_url(signal, filters, order_by)

        response = requests.get(url,headers=self.headers,)
        if response.status_code != 200:
            print(response.status_code)

        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', { 'class': 'styled-table-new' })
        columns = [i.text.strip() for i in table.find_all('th')]
        rows = []
        for row in table.find_all('tr'):
            rows.append([i.text.strip() for i in row.find_all('td')])
        rows = rows[1:]

        df = pd.DataFrame(columns=columns, data=rows)
        df = df.set_index('No.')

        return df
 
    
    def stocks_news(self) -> pd.DataFrame:
        """
        Latest stock related headlines
        Includes:
            - Seconds/Minutes since posted
            - Headline
            - Ticker(s)
            - Source
        """
        url = 'https://finviz.com/news.ashx?v=3'
        response = requests.get(url, headers=self.headers)
        soup = BeautifulSoup(response.text, 'html.parser')

        table = soup.find('table', { 'class': 'styled-table-new' })
        columns = ['Time Elapsed','Headline','Ticker','Source']

        rows = []
        for row in table.find_all('tr'):
            rows.append([i.text.splitlines() for i in row.find_all('td')])
        rows = [row[0] + [r for r in row[1] if r] for row in rows]

        df = pd.DataFrame(columns=columns, data=rows)
        df['Ticker'] = df['Ticker'].apply(lambda t: 
            (lambda p: p[0] if len(p) == 1 else p)
            ([i for i in (t.split(' ') if len(t) > 4 else [t]) 
            if not any(c in str(i) for c in '%+-')])
        )
        
        return df
