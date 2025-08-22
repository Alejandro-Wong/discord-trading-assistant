
def calendar_filtered_data(cal_type: str, timeframe: str, country: int=5, stars: list[int]=[2,3]) -> tuple[str, dict, dict]:
    """
    URL, headers, filter data for either economic, earnings, or IPO calendar. Filter by timeframe, country, and level of importance (stars).
    """

    if timeframe not in ['today','thisWeek', 'yesterday', 'tomorrow', 'nextWeek', 'upcoming', 'recent']:
        raise ValueError("Invalid timeframe. Must be either 'today','thisWeek', 'yesterday', 'tomorrow', 'nextWeek', 'upcoming', or 'recent' (case sensitve).")
    if cal_type not in ['economic-calendar','earnings-calendar','ipo-calendar']:
        raise ValueError("Invalid calendar type. Must be either 'economic-calendar','earnings-calendar', or 'ipo-calendar' (case sensitive).")
    
    headers = {
        'accept': '*/*',
        'referer': f'https://www.investing.com/{cal_type}/',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/138.0.0.0 Safari/537.36',
        'x-requested-with': 'XMLHttpRequest',
    }

    econ_url = 'https://www.investing.com/economic-calendar/Service/getCalendarFilteredData'
    earn_url = 'https://www.investing.com/earnings-calendar/Service/getCalendarFilteredData'
    ipo_url = 'https://www.investing.com/ipo-calendar/Service/getCalendarFilteredData'

    url = econ_url if cal_type == 'economic-calendar' else earn_url if cal_type == 'earnings-calendar' else ipo_url if cal_type == 'ipo-calendar' else None

    econ_filter_data = {
        'country[]': f'{country}',
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
        'importance[]': 
            stars,
        'timeZone': '8',
        'timeFilter': 'timeRemain',
        'currentTab': f'{timeframe}',
        'submitFilters': '1',
        'limit_from': '0',}
    
    earnings_filter_data = {
        'country[]': f'{country}',
        'sector[]': [
            '24',
            '25',
            '26',
            '27',
            '28',
            '29',
            '30',
            '31',
            '32',
            '33',
            '34',
            '35',
            '36',
        ],
        'importance[]': stars,
        'currentTab': f'{timeframe}',
        'submitFilters': '1',
        'limit_from': '0',
    }

    ipo_filter_data = {
        'country[]': f'{country}',
        'currentTab': f'{timeframe}',
        'limit_from': '0',
    }


    data = econ_filter_data if cal_type == 'economic-calendar' else earnings_filter_data if cal_type == 'earnings-calendar' else ipo_filter_data if cal_type == 'ipo-calendar' else None

    return url, headers, data

