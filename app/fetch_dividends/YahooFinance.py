from datetime import datetime
import pandas as pd
import yfinance as yf

class YahooFinance():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''
        self.consider_tax = False

    def __format_dataset(self, df) -> pd.DataFrame:
        dataset_dict = { 'date': [], 'dividends': [], 'split': [] }
        for key, val in df.to_dict().items():
            date_str = key.strftime('%Y/%m/%d')
            dataset_dict['date'].append(date_str)
            dataset_dict['dividends'].append(val)
            dataset_dict['split'].append(0)
        df = pd.DataFrame(dataset_dict)
        df['date'] = df['date'].apply(lambda s: datetime.strptime(s, '%Y/%m/%d'))
        df['date'] = df['date'].apply(lambda s: s.date())
        df['dividends'] = df['dividends'].apply(lambda s: float(s))
        if self.consider_tax:
            df['dividends'] = df['dividends'].apply(lambda s: s * 0.7)
        df = df.sort_values(by='date', ascending=False, ignore_index=True)
        return df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        stock = yf.Ticker(self.code)
        dataset = stock.dividends
        if len(list(dataset)) == 0:
            dataset = pd.DataFrame({ 'date': [], 'dividends': [], 'split': [] })
        else:
            dataset = self.__format_dataset(dataset)

        return dataset
