from datetime import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

class CrawlTaiwanETF():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''

    def __crawl_moneydj(self) -> pd.DataFrame:
        url = f'https://www.moneydj.com/ETF/X/Basic/Basic0005.xdjhtm?etfid={self.code}'
        print(f"crawl url: {url}")

        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        table = soup.findAll("table", class_ = "datalist")[0]
        list_rows = []
        rows = table.find_all('tr')

        for row in rows:
            row_td = [i.text for i in row.find_all('td')]
            if len(row_td)>1:
                list_rows.append(np.array(row_td)[[1, 6]])

        df = pd.DataFrame(list_rows, columns = ['date', 'dividends'] )
        df = self.__format_dataset(df)
        return df

    def __format_dataset(self, df) -> pd.DataFrame:
        df['date'] = df['date'].apply(lambda s: datetime.strptime(s, '%Y/%m/%d'))
        df['date'] = df['date'].apply(lambda a: a.date())
        df['dividends'] = df['dividends'].apply(lambda s: float(s))
        df['split'] = 0
        return df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        dataset = self.__crawl_moneydj()
        return dataset
