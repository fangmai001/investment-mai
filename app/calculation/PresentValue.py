from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

class PresentValue():

    def __init__(self) -> None:
        self.history_df = pd.DataFrame()
        self.dividends_df = pd.DataFrame()
        self.trade_record_df = pd.DataFrame()

    def __get_value_record(self, with_dividends = False) -> pd.DataFrame:
        history_df = self.history_df
        dividends_df = self.dividends_df
        trade_record_df = self.trade_record_df

        # 現值計算
        value_record_dict = {
            'date': [],
            'accumulate_stock_count': [],
            'total_cost': [],
            'total_value': [],
            'profit_rate': [],
            'market_price': [],
        }

        is_first_record = True
        for index, row in history_df.iterrows():
            trade_info_df = trade_record_df[trade_record_df['date'] == row['date']]
            dividend_info_df = dividends_df[dividends_df['date'] == row['date']]
            is_trade_day = not trade_info_df.empty
            is_dividend_day = not dividend_info_df.empty

            trade_stock_value = 0
            trade_stock_count = 0
            trade_stock_total_cost = 0

            last_accumulate_stock_count = 0
            last_total_cost = 0
            last_total_value = 0

            if is_trade_day:
                trade_stock_value = trade_info_df['stock_value'].values[0]
                trade_stock_count = trade_info_df['stock_count'].values[0]
                trade_stock_total_cost = trade_info_df['stock_total_cost'].values[0]

            if not is_first_record:
                last_accumulate_stock_count = value_record_dict['accumulate_stock_count'][-1]
                last_total_cost = value_record_dict['total_cost'][-1]
                last_total_value = value_record_dict['total_value'][-1]

            record_date = row['date']
            market_price = row['price']
            accumulate_stock_count = last_accumulate_stock_count + trade_stock_count
            total_cost = last_total_cost + trade_stock_total_cost
            total_value = accumulate_stock_count * market_price

            if with_dividends and is_dividend_day:
                dividend = dividend_info_df['dividends'].values[0]
                split = dividend_info_df['split'].values[0]
                accumulate_stock_count = accumulate_stock_count + (split * 100)
                income = accumulate_stock_count * dividend
                total_cost = total_cost - income

            if ((total_value != 0) and (total_cost != 0)):
                profit_rate = ((total_value - total_cost) / total_cost)
            else:
                profit_rate = 0

            value_record_dict['date'].append(record_date)
            value_record_dict['accumulate_stock_count'].append(accumulate_stock_count)
            value_record_dict['total_cost'].append(total_cost)
            value_record_dict['total_value'].append(total_value)
            value_record_dict['profit_rate'].append(profit_rate)
            value_record_dict['market_price'].append(market_price)
            is_first_record = False
        value_record_df = pd.DataFrame(value_record_dict)

        return value_record_df

    def __dividends_merge(self, value_record_df, value_with_dividends_record_df) -> pd.DataFrame:
        value_record_df['total_cost_with_dividend'] = value_with_dividends_record_df['total_cost']
        value_record_df['profit_rate_with_dividend'] = value_with_dividends_record_df['profit_rate']
        return value_record_df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        with_dividends = False
        value_record_df = self.__get_value_record(with_dividends)
        with_dividends = True
        value_with_dividends_record_df = self.__get_value_record(with_dividends)
        value_record_df = self.__dividends_merge(value_record_df, value_with_dividends_record_df)

        return value_record_df
