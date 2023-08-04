import os
from datetime import datetime
import numpy as np
import pandas as pd
import requests
from bs4 import BeautifulSoup

class CrawlTaiwanStock():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''

    def __crawl_goodinfo(self) -> pd.DataFrame:
        code = self.code.split('.')[0]
        url = f'https://goodinfo.tw/tw/StockDividendSchedule.asp?STOCK_ID={code}'
        print(f"crawl url: {url}")

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/112.0.0.0 Safari/537.36"
        }
        r = requests.get(url, headers = headers)
        r.encoding='utf-8'
        #解析器：lxml(官方推薦，速度最快)
        soup = BeautifulSoup(r.text, 'lxml')

        list_rows = []
        rows = soup.find_all('tr')
        for row in rows:
            row_td = [i.text for i in row.find_all('td')]
            if len(row_td)==19 and row_td[3] != '':
                # print(row_td)
                list_rows.append(np.array(row_td)[[3, 14, 17]])
        df = pd.DataFrame(list_rows, columns = ['date', 'dividends', 'split'] )

        # 排除那種「即將除息」等非日期字元
        df['date'] = df['date'].apply(lambda s: s[:8])

        df['date'] = df['date'].apply(lambda s: datetime.strptime(s, "%y'%m/%d"))
        df['date'] = df['date'].apply(lambda s: s.date())
        df['dividends'] = df['dividends'].apply(lambda s: float(s))
        df['split'] = df['split'].apply(lambda s: float(s))

        df.to_csv(f"import/dividends_{self.code}_{self.start_date}_{self.end_date}.csv")
        return df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """

        filepath = f"import/dividends_{self.code}_{self.start_date}_{self.end_date}.csv"
        if os.path.isfile(filepath):
            dataset = pd.read_csv(filepath, index_col=[0])
            dataset['date'] = dataset['date'].apply(lambda s: datetime.strptime(s, "%Y-%m-%d"))
            dataset['date'] = dataset['date'].apply(lambda s: s.date())
        else:
            dataset = self.__crawl_goodinfo()
        return dataset
