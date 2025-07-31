from market_overview.update_csvs import update_csvs
from market_overview.charts import multi_line_chart


def refresh_charts():
    update_csvs()
    multi_line_chart('YTD Index ETF Performance (Last 30 Days)', './market_overview/csvs/index_etfs/', './market_overview/pngs/', 30, False)
    multi_line_chart('YTD SPDR Sectors Performance (Last 30 Days)', './market_overview/csvs/spdr_sectors/', './market_overview/pngs/', 30, False)

