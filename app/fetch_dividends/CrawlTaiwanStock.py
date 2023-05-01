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
        df['date'] = df['date'].apply(lambda s: datetime.strptime(s, "%y'%m/%d"))
        df['dividends'] = df['dividends'].apply(lambda s: float(s))
        df['split'] = df['split'].apply(lambda s: float(s))
        return df

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        dataset = self.__crawl_goodinfo()
        return dataset
