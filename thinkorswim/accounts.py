# import logging
import pandas as pd
from datetime import datetime, timezone, timedelta

import schwabdev
from thinkorswim.account_funcs import extract_orders, extract_transactions, extract_positions

# logging.basicConfig(level=logging.INFO)


class Accounts:
    """
    Get all orders and transactions for all linked accounts
    """

    def __init__(self, client_key: str, client_secret: str, callback: str, days: int):
        self.client = schwabdev.Client(client_key, client_secret, callback)
        self.linked_accounts = self.client.account_linked().json()
        self.all_accounts = [self.linked_accounts[i].get('hashValue') for i in range(len(self.linked_accounts))]
        self.days = days

    def details(self):
        details = self.client.account_details_all().json()
        acct_type = pd.Series([details[i]['securitiesAccount']['type'] for i in range(len(details))])
        acct_num = pd.Series([details[i]['securitiesAccount']['accountNumber'] for i in range(len(details))])
        cash_bal = pd.Series([details[i]['securitiesAccount']['initialBalances']['cashBalance'] for i in range(len(details))])
        acct_val = pd.Series([details[i]['securitiesAccount']['initialBalances']['accountValue'] for i in range(len(details))])

        df_dict = {'AcctType': acct_type, 'Acct#': acct_num, 'Balance': cash_bal, 'AcctValue': acct_val}

        df = pd.DataFrame(df_dict)
        df = df.set_index('Acct#')

        return df
    
    def all_positions(self):
        """
        
        """
        positions_all_accounts = []
        for account in self.all_accounts:
            positions_all_accounts.append(self.client.account_details(account, fields="positions").json())
        
        dataframes = []
        for position in positions_all_accounts:
            dataframes.append(extract_positions(position))
        
        positions_df = pd.concat([d for d in dataframes if not d.empty])

        return positions_df


    def all_orders(self) -> pd.DataFrame:
        """
        Orders for all accounts combined to a single DataFrame

        columns:
        datetime | symbol | account | instruction | quantity
        """
        orders_all_accounts = []
        for account in self.all_accounts:
            orders_all_accounts.append(self.client.account_orders(
                account, datetime.now(timezone.utc) - timedelta(days=self.days),
                datetime.now(timezone.utc)).json()
            )
        
        dataframes = []
        for orders in orders_all_accounts:
            dataframes.append(extract_orders(orders))

        orders_df = pd.concat([d for d in dataframes])

        return orders_df


    def all_transactions(self) -> pd.DataFrame:
        """
        Transactions for all accounts combined to a single DataFrame

        columns:
        datetime | symbol | account | price | net_amount
        """
        transactions_all_accounts = []
        for account in self.all_accounts:
            transactions_all_accounts.append(self.client.transactions(
                account, datetime.now(timezone.utc) - timedelta(days=self.days),
                datetime.now(timezone.utc), "TRADE").json()
            )
        
        dataframes = []
        for transactions in transactions_all_accounts:
            dataframes.append(extract_transactions(transactions))
        
        transactions_df = pd.concat(d for d in dataframes)

        return transactions_df
    

    def merged_dataframe(self) -> pd.DataFrame:
        """
        Combines transactions and orders dataframes
        datetime | symbol | account | instruction | price | quantity | net_amount
        """
        orders = self.all_orders()
        transactions = self.all_transactions()

        df = pd.merge(orders, transactions, how='right')
        df = df.set_index('date')

        return df