from ohlcv.ohlcv import OHLC

def title_to_filename(title: str) -> str:
    """
    Takes a title and converts to filename format
    """
    unwanted_char = ['(',')','[',']','{','}']

    for char in title:
        if char in unwanted_char:
            title = title.replace(char,'')

    return title.lower().replace(' ','_')


def ytd_closes_to_csvs(tickers: list, path: str) -> None:
    """
    Fetch YTD daily closing prices for a list of tickers
    """
    period = 'ytd'
    interval = '1d'
    for ticker in tickers:
        df = OHLC(ticker, period, interval).from_yfinance()
        close = df['Close']
        close.to_csv(f'{path}{ticker}.csv')
    