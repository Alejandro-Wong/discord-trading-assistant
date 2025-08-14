import pandas as pd

from thinkorswim.accounts import Accounts
from thinkorswim.account_funcs import round_complex

class Trades(Accounts):
    """
    Get current positions and profit/loss from closed trades
    """

    def __init__(self, client_key: str, client_secret: str, callback: str, days: int):

        super().__init__(client_key, client_secret, callback, days)

        self.df = self.merged_dataframe().dropna()
        self.positions = self.all_positions()
        self.long = ['BUY_TO_OPEN','SELL_TO_OPEN','BUY']
        self.short = ['SELL_TO_CLOSE','BUY_TO_CLOSE','SELL']
        
        self.pl = {}
        for date in self.df.index:
            self.pl[date] = 0 
        self.entry = {}
        self.exit = {}
        self.trades = {}

        for i, row in self.df.iterrows():

            symbol = row['symbol']
            price = row['price']
            net_amount = row['net_amount']
            quantity = row['quantity']
            instruction = row['instruction']

            # Sometimes NaN shows up in instruciton column
            if not isinstance(instruction, str):
                raise ValueError("Check orders dataframe for NaN values. Data may need to be refetched")

            if instruction in self.long:
                if symbol not in self.entry.keys():
                    self.entry[symbol] = [net_amount, quantity, [price]]
                else:
                    self.entry[symbol][0] += net_amount
                    self.entry[symbol][1] += quantity
                    self.entry[symbol][2].append(price)

            elif instruction in self.short:
                if symbol not in self.exit.keys():
                    self.exit[symbol] = [net_amount, quantity, [price]]
                else:
                    self.exit[symbol][0] += net_amount
                    self.exit[symbol][1] += quantity
                    self.exit[symbol][2].append(price)

            if symbol in self.entry.keys() and symbol in self.exit.keys():
                if self.entry[symbol][1] == self.exit[symbol][1]:
                    if symbol not in self.trades.keys():
                        self.trades[symbol] = [i, (round_complex(self.entry[symbol][0]) + round_complex(self.exit[symbol][0]))]
                    else:
                        self.trades[symbol][1] += (round_complex(self.entry[symbol][0]) + round_complex(self.exit[symbol][0]))
                    self.pl[i] += round_complex(self.trades[symbol][1])
                    del self.entry[symbol]
                    del self.exit [symbol]

                elif self.entry[symbol][1] != self.exit[symbol][1]:
                    pass

            elif symbol not in self.entry.keys() and symbol in self.exit.keys():
                del self.exit[symbol]


    def profit_loss(self) -> pd.Series:
        """
        Total daily profit/loss
        """
        pl = pd.Series(index=self.pl.keys(), data=self.pl.values(), name='P/L')

        return pl
    
    
    def trade_entries(self) -> pd.DataFrame:
        """
        Entry cost/credit, quantity bought or shorted, and average price per share
        """
        df = pd.DataFrame(index=self.entry.keys(), data=self.entry.values())
        if df.empty:
            return
        else:
            df = df.rename(columns={0:'Cost', 1:'EntryQuantity', 2:'AvgEntryPrice'})
            df['AvgEntryPrice'] = df['AvgEntryPrice'].apply(lambda x: round(sum(x) / len(x), 2) if len(x) > 0 else 0)

            return df
    

    def trade_exits(self) -> pd.DataFrame:
        """
        Proceeds, quantity sold or covered, average price per share
        """
        df = pd.DataFrame(index=self.exit.keys(), data=self.exit.values())
        if df.empty:
            return
        else:
            df = df.rename(columns={0:'Proceeds', 1:'ExitQuantity', 2:'AvgExitPrice'})
            df['AvgExitPrice'] = df['AvgExitPrice'].apply(lambda x: round(sum(x) / len(x), 2) if len(x) > 0 else 0)

            return df
    

    def active_positions(self) -> pd.DataFrame:
        """
        Active positions
        """
        entries = self.trade_entries()
        exits = self.trade_exits()

        if type(entries) == pd.DataFrame and type(exits) == pd.DataFrame:
            merge = pd.merge(entries,exits, left_index=True, right_index=True, how='outer')
            merge = merge.fillna(0)
        
            df = pd.merge(merge, self.positions, left_index=True, right_index=True, how='outer')
            df['ExitQuantity'] = df['ExitQuantity'].astype(int)
            df['TotalCost'] = df['Cost'] + df['Proceeds']
            df['ProfitSecured'] = df['ExitQuantity'] * abs((df['AvgExitPrice'] - df['AvgEntryPrice']))
            df['TotalP/L'] = df['OpenP/L'] + df['ProfitSecured']
            df['QuantityRemaining'] = df['EntryQuantity'] - df['ExitQuantity']
            df = df[['EntryQuantity','AvgEntry','ExitQuantity','AvgExitPrice','QuantityRemaining','TotalCost','ProfitSecured','TotalP/L']]

            return df
        else:
            return entries
         


    def closed_trades(self) -> pd.DataFrame:
        """
        Profit/loss per individual trade
        """
        df = pd.DataFrame(index=self.trades.keys(), data=self.trades.values()).reset_index()
        df = df.rename(columns={'index':'Ticker', 0:'Date', 1:'P/L'})
        df = df.set_index('Date')
 
        return df