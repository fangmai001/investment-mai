from datetime import timedelta
from datetime import datetime
from dateutil.relativedelta import relativedelta
import numpy as np
import pandas as pd

class ExecuteTrade():

    def __init__(self) -> None:
        self.investment_amount = 5_000 # 每個月的投資金額
        self.purchase_day = 1 # 每個月的第N個交易日購買
        self.history_df = pd.DataFrame()

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        investment_amount = self.investment_amount
        purchase_day = self.purchase_day
        history_df = self.history_df

        # 交易紀錄
        trade_record_dict = {
            'date': [],
            'stock_value': [],
            'stock_count': [],
            'stock_total_cost': [],
        }

        # 每月 purchase_day 進行購買
        loop_start_dt = history_df.head(1)['date'].values[0].replace(day=1)
        loop_end_dt = history_df.tail(1)['date'].values[0].replace(day=1)
        loop_current_dt = loop_start_dt
        while loop_current_dt <= loop_end_dt:
            month_start_dt = loop_current_dt.replace(day=1)
            month_end_dt = month_start_dt + relativedelta(months = 1, days = -1)
            # print(month_start_dt, month_end_dt)

            loop_current_df = history_df[(history_df['date'] >= month_start_dt) & (history_df['date'] <= month_end_dt)]
            purchase_df = loop_current_df.iloc[purchase_day - 1]
            # print(purchase_df)

            trade_date = purchase_df['date']
            trade_stock_value = purchase_df['price']
            trade_stock_count = np.floor(investment_amount / trade_stock_value)
            trade_stock_total_cost = trade_stock_value * trade_stock_count

            trade_record_dict['date'].append(trade_date)
            trade_record_dict['stock_value'].append(trade_stock_value)
            trade_record_dict['stock_count'].append(trade_stock_count)
            trade_record_dict['stock_total_cost'].append(trade_stock_total_cost)

            loop_current_dt = loop_current_dt + relativedelta(months = 1)
        trade_record_df = pd.DataFrame(trade_record_dict)

        return trade_record_df
