import pandas as pd
from decimal import Decimal, ROUND_UP
"""
Functions for extracting data relevant to calculating daily profit/loss from Charles Schwab 
accounts' orders and transactions 
"""

def round_complex(value: float):
    """
    Round numbers that somehow don't round using built-in round()
    """
    return Decimal(value).quantize(Decimal('0.01'), rounding=ROUND_UP)


def create_clean_dataframe(data:dict)-> pd.DataFrame:
    """ 
    Returns cleaned DataFrame of either Transactions or Order data
    """
    df = pd.DataFrame(data)
    df['datetime'] = pd.to_datetime(df['datetime']).dt.strftime('%Y-%m-%d %H:%M:%S')
    df['datetime'] = pd.to_datetime(df['datetime'])
    df['date'] = df['datetime'].dt.strftime('%Y-%m-%d')
    df['time'] = df['datetime'].dt.time.astype(str)

    if 'price' in data.keys():
        df = df[['date','time','symbol','account','price','net_amount']]
        df = df.groupby(['date','time','symbol','account','price'], as_index=False).agg({'net_amount':'sum'})
    elif 'quantity' in data.keys():
        df['quantity'] = df['quantity'].astype(int)
        df['account'] = df['account'].astype(str)
        df = df[['date','time','symbol','account','instruction','quantity']]

    df = df.sort_values(by=['date','time']).reset_index(drop=True)

    return df


def extract_order_data(orders:list[dict]) -> pd.DataFrame:
    """
    Iterates through list of dictionaries and returns a DataFrame of relevant order data
    """
    # Check if input is list[dict]
    if not isinstance(orders, list):
        raise TypeError('Function not receiving type list[dict], check API connection')
    else:

        # Keys
        f_quantity = 'filledQuantity'
        symbol = 'symbol'
        instruction = 'instruction'
        close_time = 'closeTime'
        account_num = 'accountNumber'
        olc = 'orderLegCollection'

        # Lists and dict to create dataframe
        close_times = []
        symbols = []
        account_nums = []
        instructions = []
        quantities = []
        
        data = {'datetime':close_times, 
                'symbol':symbols, 
                'account':account_nums, 
                'instruction':instructions, 
                'quantity': quantities}

        for order in orders:
            # Search for filledQuantity, filledQuantity > 0.0
            try:
                quant = order[f_quantity]
                if quant > 0.0:
                    quantities.append(quant)

                    # Search 'orderLegCollection' for 'symbol' and 'instruction'
                    try:
                        orderleg = order[olc]
                        symbols.append(orderleg[0]['instrument'][symbol])
                        instructions.append(orderleg[0][instruction])
                    except KeyError:
                        print(f"{orderleg} not found")

                    # Search 'closeTime'
                    try:
                        close = order[close_time]
                        close_times.append(close)
                    except KeyError:
                        print(f"{close} not found")

                    # Search 'accountNumber'
                    try:
                        account = order[account_num]
                        account_nums.append(account)
                    except KeyError:
                        print(f"{account} not found")

            except KeyError:
                # print(f"{f_quantity} not found")
                pass

        # Create Dataframe
        df = create_clean_dataframe(data)

        return df
    

def extract_orders(orders:list[dict]) -> pd.DataFrame:
    """
    Some relevant data needed for proper profit/loss calculation is buried 
    in deeper layers of orders' list of dictionaries.

    This function iterates through these deeper layers and applies extract_order_data
    to create sub DataFrames that are eventually combined into the main DataFrame.
    Returns complete DataFrame of all relevant order data.
    """
    main_df = extract_order_data(orders) # Regular orders df
    other_dfs = []                       # Special orders dfs

    # Extract data from special orders
    for order in orders:
        if 'childOrderStrategies' in order.keys():
            cos_layer1 = order['childOrderStrategies'][0]
            if 'childOrderStrategies' in cos_layer1.keys():
                cos_layer2 = cos_layer1['childOrderStrategies']
                other_dfs.append(extract_order_data(cos_layer2))

    # Combine other_dfs
    if other_dfs:
        spec_df = pd.concat(other_dfs)
        # Combine main with spec
        df = pd.concat([main_df, spec_df])
    else:
        df = main_df

    df = df.sort_values(by=['date','time'])

    return df


def extract_transactions(transactions:list[dict]) -> pd.DataFrame:
    """
    Iterates through list of dictionaries and returns a DataFrame of relevant transactions data
    """
    # Keys
    time = 'time'
    account_num = 'accountNumber'
    net_amount = 'netAmount'
    symbol = 'symbol'
    price = 'price'
    transfer = 'transferItems'
    instrument = 'instrument'

    # Lists and dict to create dataframe
    times = []
    account_nums = []
    net_amounts = []
    symbols = []
    prices = []

    data = {'datetime':times,
            'symbol':symbols,
            'account':account_nums,
            'price':prices,
            'net_amount':net_amounts}

    for tr in transactions:
        # Search 'time'
        try:
            t = tr[time]
            times.append(t)
        except KeyError:
            print(f"{t} not found")
        
        # Search 'accountNumber'
        try:
            account = tr[account_num]
            account_nums.append(account)
        except KeyError:
            print(f"{account} not found")

        # Search 'netAmount'
        try:
            net = tr[net_amount]
            net_amounts.append(net)
        except:
            print(f"{net} not found")

        # Search 'transferItems' for 'symbol' and 'price'
        try:
            transf = tr[transfer]
            instrum = transf[-1][instrument]
            symbols.append(instrum[symbol])
            prices.append(transf[-1][price])
        except KeyError:
            print(f"{transf} not found")

    # Create DataFrame
    df = create_clean_dataframe(data)

    return df


def extract_positions(account_details: dict) -> pd.DataFrame:
    """
    Get average entry price and open p/l from active positions
    """
    securities = account_details['securitiesAccount']

    ticker = []
    avg_price = []
    open_pl = []

    try:
        positions = securities['positions']
        for position in positions:
            ticker.append(position['instrument']['symbol'])
            avg_price.append(round_complex(position['averagePrice']))
            open_pl.append(position['longOpenProfitLoss'])
    except Exception:
        print('One or more accounts may not currently have active positions')
        pass

    ticker_series = pd.Series(ticker)
    price_series = pd.Series(avg_price)
    pl_series = pd.Series(open_pl)

    df_dict = {
        'Ticker': ticker_series, 
        'AvgEntry': price_series, 
        'OpenP/L': pl_series
    }
    df = pd.DataFrame(df_dict)
    df = df.set_index('Ticker')

    return df
    


    
