import os
import pandas as pd
import logging
from dotenv import load_dotenv

from thinkorswim.accounts import Accounts
from thinkorswim.trades import Trades

# logging.basicConfig(level=logging.INFO)

def active_positions() -> pd.DataFrame:
    """
    
    """
    load_dotenv()

    key = os.getenv('app_key')
    secret = os.getenv('app_secret')
    callback = os.getenv('callback_url')

    trades = Trades(key, secret, callback, 60)

    active_positions = trades.active_positions().reset_index()

    return active_positions
