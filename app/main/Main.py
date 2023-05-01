import pandas as pd
from app.fetch_history.Stock import Stock
from app.fetch_history.Fund import Fund
from app.fetch_dividends.CrawlTaiwanStock import CrawlTaiwanStock
from app.fetch_dividends.CrawlTaiwanETF import CrawlTaiwanETF
from app.fetch_dividends.StaticVWRD import StaticVWRD
from app.calculation.ExecuteTrade import ExecuteTrade
from app.calculation.PresentValue import PresentValue
from app.util.Summary import Summary

class Main():

    def __init__(self) -> None:
        self.code = ""
        self.start_date = ""
        self.end_date = ""
        self.investment_amount = 1000
        self.purchase_day = 1
        self.is_fund = False
        self.using_taiwan_stock_crawl = True
        self.using_taiwan_etf_crawl = False

    def __get_history_df(self) -> pd.DataFrame:
        if self.is_fund:
            app = Fund()
        else:
            app = Stock()

        app.code = self.code
        app.start_date = self.start_date
        app.end_date = self.end_date
        history_df = app.launch()

        return history_df

    def __get_dividends_df(self) -> pd.DataFrame:
        if self.using_taiwan_etf_crawl:
            app = CrawlTaiwanETF()
        if self.using_taiwan_stock_crawl:
            app = CrawlTaiwanStock()
        if self.code == 'VWRD.L':
            app = StaticVWRD()

        app.code = self.code
        app.start_date = self.start_date
        app.end_date = self.end_date
        dividends_df = app.launch()

        return dividends_df

    def launch(self) -> None:
        """
        啟動主程式

        :return: DataFrame
        """
        history_df = self.__get_history_df()
        dividends_df = self.__get_dividends_df()

        app = ExecuteTrade()
        app.investment_amount = self.investment_amount
        app.purchase_day = self.purchase_day
        app.history_df = history_df
        trade_record_df = app.launch()

        app = PresentValue()
        app.history_df = history_df
        app.dividends_df = dividends_df
        app.trade_record_df = trade_record_df
        app.dividends_df = dividends_df
        value_record_df = app.launch()

        app = Summary()
        app.code = self.code
        app.start_date = self.start_date
        app.end_date = self.end_date
        app.trade_record_df = trade_record_df
        app.value_record_df = value_record_df
        app.launch()

        # return trade_record_df, value_record_df
