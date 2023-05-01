import pandas as pd
import yfinance as yf

class Stock():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''

    def __fetch_yfinance(self) -> pd.DataFrame:
        # 獲取股票歷史股價數據和股息數據
        stock = yf.Ticker(self.code)
        dataset = stock.history(start=self.start_date, end=self.end_date)
        dataset = dataset.reset_index()
        dataset['Date'] = dataset['Date'].apply(lambda a: a.date)
        dataset = self.__format_dataset(dataset)
        return dataset

    def __format_dataset(self, dataset) -> pd.DataFrame:
        fm_dataset = pd.DataFrame()
        fm_dataset['date'] = dataset['Date']
        fm_dataset['price'] = dataset['Close']
        return fm_dataset

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        dataset = self.__fetch_yfinance()
        return dataset
