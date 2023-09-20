import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

class Summary():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''
        self.trade_record_df = pd.DataFrame()
        self.value_record_df = pd.DataFrame()

    def __print_log(self) -> str:
        final_profit_rate = self.value_record_df['profit_rate'].values[-1]
        final_profit_rate_with_dividend = self.value_record_df['profit_rate_with_dividend'].values[-1]
        final_income = self.value_record_df['total_value'].values[-1] - self.value_record_df['total_cost_with_dividend'].values[-1]
        total_cost = self.value_record_df['total_cost'].values[-1]

        result_summary_str = ''
        result_summary_str = result_summary_str + self.code
        result_summary_str = result_summary_str + '\n'
        result_summary_str = result_summary_str + f"{self.start_date}-{self.end_date}"
        result_summary_str = result_summary_str + '\n'
        result_summary_str = result_summary_str + f"總報酬: {np.round(final_profit_rate * 100, 2)}%"
        result_summary_str = result_summary_str + '\n'
        result_summary_str = result_summary_str + f"總報酬(含息): {np.round(final_profit_rate_with_dividend * 100, 2)}%"
        result_summary_str = result_summary_str + '\n'
        result_summary_str = result_summary_str + f"總損益: {'{:,.0f}$'.format(final_income)}"
        result_summary_str = result_summary_str + '\n'
        result_summary_str = result_summary_str + f"總投資金額: {'{:,.0f}$'.format(total_cost)}$"
        result_summary_str = result_summary_str + '\n'
        return result_summary_str

    def __value_vs_cost(self) -> None:
        # 繪製股票價值和股息收入的折線圖
        fig, ax = plt.subplots()
        # ax.plot(portfolio_value, label="Stock Value")
        # ax.plot(monthly_dividend_income.cumsum(), label="Dividend Income")
        # ax.plot(portfolio_value + monthly_dividend_income.cumsum(), label="Total Portfolio Value")
        ax.plot(self.value_record_df["total_value"], label="total_value")
        ax.plot(self.value_record_df["total_cost"], label="total_cost")
        ax.plot(self.value_record_df["total_cost_with_dividend"], label="total_cost_with_dividend")
        # ax.plot(history["Close"], label="Close")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("$")

        plt.show()

    def __profit(self) -> None:
        # 繪製股票價值和股息收入的折線圖
        fig, ax = plt.subplots()
        ax.plot([ 0 for _ in range(self.value_record_df.index.size)], label="profit_rate")
        ax.plot(self.value_record_df["profit_rate"], label="profit_rate")
        ax.plot(self.value_record_df["profit_rate_with_dividend"], label="profit_rate_with_out")
        ax.legend(loc="upper left")
        ax.set_xlabel("Date")
        ax.set_ylabel("Profit Rate(%)")

        plt.show()

    def __export_csv(self) -> None:
        self.trade_record_df.to_csv(f'export/trade_record_df({self.code}).csv')
        self.value_record_df.to_csv(f'export/value_record_df({self.code}).csv')

    def launch(self) -> str:
        log = ''
        log = log + self.__print_log()
        self.__value_vs_cost()
        self.__profit()
        # self.__export_csv()
        return log
