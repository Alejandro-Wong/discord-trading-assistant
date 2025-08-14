from ohlcv.ohlcv import OHLC
from market_overview.funcs import ytd_closes_to_csvs

def update_csvs():

    # Index ETFs
    INDEX_ETFS = ['SPY','QQQ','DIA','IWM']

    # Sectors
    SPDR_SECTORS = ['XLC','XLY','XLP','XLE','XLF','XLV','XLI','XLB','XLK','XLU','SPY']

    ytd_closes_to_csvs(INDEX_ETFS, './market_overview/csvs/index_etfs/')
    ytd_closes_to_csvs(SPDR_SECTORS, './market_overview/csvs/spdr_sectors/')