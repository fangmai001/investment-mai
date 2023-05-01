from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

class PresentValue():

    def __init__(self) -> None:
        self.investment_amount = 5_000 # 每個月的投資金額
        self.purchase_day = 1 # 每個月的第N個交易日購買
        self.history_df = pd.DataFrame()
        self.dividends_df = pd.DataFrame()
        self.trade_record_df = pd.DataFrame()

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        history_df = self.history_df
        dividends_df = self.dividends_df
        trade_record_df = self.trade_record_df

        # 現值計算
        value_record_dict = {
            'date': [],
            'accumulate_stock_count': [],
            'total_cost': [],
            'total_cost_with_dividend': [],
            'total_value': [],
            'profit_rate': [],
            'profit_rate_with_dividend': [],
            'market_price': [],
        }

        is_first_record = True
        for index, row in history_df.iterrows():
            trade_info_df = trade_record_df[trade_record_df['date'] == row['date']]
            dividend_info_df = dividends_df[dividends_df['date'] == row['date']]
            is_trade_day = not trade_info_df.empty
            is_dividend_day = not dividend_info_df.empty

            if is_trade_day:
                trade_stock_value = trade_info_df['stock_value'].values[0]
                trade_stock_count = trade_info_df['stock_count'].values[0]
                trade_stock_total_cost = trade_info_df['stock_total_cost'].values[0]
            else:
                trade_stock_value = 0
                trade_stock_count = 0
                trade_stock_total_cost = 0

            if is_first_record:
                last_accumulate_stock_count = 0
                last_total_cost = 0
                last_total_cost_with_dividend = 0
                last_total_value = 0
            else:
                last_accumulate_stock_count = value_record_dict['accumulate_stock_count'][-1]
                last_total_cost = value_record_dict['total_cost'][-1]
                last_total_cost_with_dividend = value_record_dict['total_cost_with_dividend'][-1]
                last_total_value = value_record_dict['total_value'][-1]

            record_date = row['date']
            accumulate_stock_count = last_accumulate_stock_count + trade_stock_count
            total_cost = last_total_cost + trade_stock_total_cost
            total_cost_with_dividend = last_total_cost_with_dividend + trade_stock_total_cost
            total_value = accumulate_stock_count * row['price']
            market_price = row['price']
            profit_rate = ((total_value - total_cost) / total_cost) if ((total_value != 0) and (total_value != 0)) else 0

            if is_dividend_day:
                dividend = dividend_info_df['dividends'].values[0]
                income = accumulate_stock_count * dividend
                total_cost_with_dividend = total_cost_with_dividend - income
                # accumulate_stock_count = accumulate_stock_count + (dividend_info_df['split']*100)

            profit_rate_with_dividend = ((total_value - total_cost_with_dividend) / total_cost_with_dividend) if ((total_value != 0) and (total_value != 0)) else 0

            value_record_dict['date'].append(record_date)
            value_record_dict['accumulate_stock_count'].append(accumulate_stock_count)
            value_record_dict['total_cost'].append(total_cost)
            value_record_dict['total_cost_with_dividend'].append(total_cost_with_dividend)
            value_record_dict['total_value'].append(total_value)
            value_record_dict['profit_rate'].append(profit_rate)
            value_record_dict['profit_rate_with_dividend'].append(profit_rate_with_dividend)
            value_record_dict['market_price'].append(market_price)
            is_first_record = False
        value_record_df = pd.DataFrame(value_record_dict)

        return value_record_df
