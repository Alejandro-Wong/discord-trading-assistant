base_url = 'https://finviz.com/screener.ashx?v=111'
signal_query = '&s='
filter_query = '&f='
order_query = '&o='
comma = ','
comma_multi = '%2C'

# Signal
signals = {
    'top_gainers': 'ta_topgainers',
    'top_losers': 'ta_toplosers',
    'new_high': 'ta_newhigh',
    'new_low': 'ta_newlow',
    'most_volatile': 'ta_mostvolatile',
    'most_active': 'ta_mostactive',
    'unusual_volume': 'ta_unusualvolume',
    'overbought': 'ta_overbought',
    'oversold': 'ta_oversold',
    'major_news': 'n_majornews',
    'downgrades': 'n_downgrades',
    'upgrades': 'n_upgrades',
    'earnings_before': 'n_earningsbefore',
    'earnings_after': 'n_earningsafter',
    'latest_buys': 'it_latestbuys',
    'latest_sells': 'it_latestsells',
    'horizontal_sr': 'ta_p_horizontal',
    'tl_resistance': 'ta_p_tlresistance',
    'tl_support': 'ta_p_tlsupport',
    'wedge_up': 'ta_p_wedgeup',
    'wedge_down': 'ta_p_wedgedown',
    'triangle_asc': 'ta_p_wedgeresistance',
    'triangle_desc': 'ta_p_wedgesupport',
    'wedge': 'ta_p_wedge',
    'channel_up': 'ta_p_channelup',
    'channel_down': 'ta_channeldown',
    'channel': 'ta_p_channel',
    'double_top': 'ta_p_doubletop',
    'double_bottom': 'ta_p_doublebottom',
    'multiple_top': 'ta_p_multipletop',
    'multiple_bottom': 'ta_p_multiplebottom',
    'head_and_shoulders': 'ta_p_headandsholders',
    'inv_head_and_shoulders': 'ta_p_headandsholdersinv'
}

# Exchange
exchanges = {
    'amex': 'exch_amex',
    'cboe': 'exch_cboe',
    'nasdaq': 'exch_nasd',
    'nyse': 'exch_nyse'
}

# Market Cap
market_caps = {
    'mega': 'cap_mega', # 200B +
    'large': 'cap_large', # 10B to 200B
    'mid': 'cap_mid', # 2B to 10B
    'small': 'cap_small', # 300M to 2B
    'micro': 'cap_micro', # 50M to 300M
    'nano': 'cap_nano', # under 50M
    'large_plus': 'cap_largeover', # Over 10B
    'mid_plus': 'cap_midover', # Over 2B
    'small_plus': 'cap_smallover', # Over 300M
    'micro_plus': 'cap_microover', # Over 50M 
    'large_minus': 'cap_largeunder', # Under 200B
    'mid_minus': 'cap_midunder', # Under 10B
    'small_minus': 'cap_smallunder', # Under 2B
    'micro_minus': 'cap_microunder', # Under 300M
}


# Earnings Date
earnings_dates = {
    'today': 'earningsdate_today',
    'today_before': 'earningsdate_todaybefore', # Today, before market open
    'today_after': 'earningsdate_todayafter', # Today, after market open
    'tomorrow': 'earningsdate_tomorrow',
    'tomorrow_before': 'earningsdate_tomorrowbefore',
    'tomorrow_after': 'earningsdate_tomorrowafter',
    'yesterday': 'earningsdate_yesterday',
    'yesterday_before': 'earningsdate_yesterdaybefore',
    'yesterday_after': 'earningsdate_yesterdayafter',
    'next_5_days': 'earningsdate_nextdays5',
    'prev_5_days': 'earningsdate_prevdays5',
    'this_week': 'earningsdate_thisweek',
    'next_week': 'earningsdate_nextweek',
    'prev_week': 'earningsdate_prevweek',
    'this_month': 'thismonth'
}

# Price
prices = {
    '<1': 'sh_price_u1',
    '<2': 'sh_price_u2',
    '<3': 'sh_price_u3',
    '<4': 'sh_price_u4',
    '<5': 'sh_price_u5',
    '<7': 'sh_price_u7',
    '<10': 'sh_price_u10',
    '<15': 'sh_price_u15',
    '<20': 'sh_price_u20',
    '<30': 'sh_price_u30',
    '<40': 'sh_price_u40',
    '<50': 'sh_price_u50',
    '>1': 'sh_price_o1',
    '>2': 'sh_price_o2',
    '>3': 'sh_price_o3',
    '>4': 'sh_price_o4',
    '>5': 'sh_price_o5',
    '>7': 'sh_price_o7',
    '>10': 'sh_price_o10',
    '>15': 'sh_price_o15',
    '>20': 'sh_price_o20',
    '>30': 'sh_price_o30',
    '>40': 'sh_price_o40',
    '>50': 'sh_price_o50',
    '>60': 'sh_price_o60',
    '>70': 'sh_price_o70',
    '>80': 'sh_price_o80',
    '>90': 'sh_price_o90',
    '>100': 'sh_price_o100',
    '1-5': 'sh_price_1to5',
    '1-10': 'sh_price_1to10',
    '1-20': 'sh_price_1to20',
    '5-10': 'sh_price_5to10',
    '5-20': 'sh_price_5to20',
    '5-50': 'sh_price_5to50',
    '10-20': 'sh_price_10to20',
    '10-50': 'sh_price_10to50',
    '20-50': 'sh_price_20to50',
    '50-100': 'sh_price_50to100'
}

# Indexes
indexes = {
    'sp500': 'idx_sp500',
    'ndx': 'idx_ndx',
    'dji': 'idx_dji',
    'rut': 'idx_rut'
}

# Country
country = {
    'usa': 'geo_usa'
}


filters = [exchanges, market_caps, earnings_dates, prices, indexes, country]



def search_filters(query: str) -> str:
    target = {}
    for filter in filters:
        if query in filter.keys():
            target = filter
    
    return target[query]