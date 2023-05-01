
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

class StaticVWRD():

    def __init__(self) -> None:
        # self.code = ''
        self.start_date = ''
        self.end_date = ''

    def __read_csv(self) -> pd.DataFrame:
        df = pd.read_excel('import/VWRD(dividends).xlsx')
        df = df.drop(list(range(6)))
        df = df.drop(list(df.index[-2:]))
        df['date'] = df['Unnamed: 3']
        df['dividends'] = df['Unnamed: 6']
        df = df.drop(columns = df.columns.to_numpy()[:-2])
        df = df.reset_index(drop=True)
        df['date'] = df['date'].apply(lambda s: datetime.strptime(s, '%d %b %Y'))
        df['date'] = df['date'].apply(lambda a: a.date())
        df['dividends'] = df['dividends'].apply(lambda s: float(s[1:]))
        return df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        dataset = self.__read_csv()
        return dataset
