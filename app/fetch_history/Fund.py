from datetime import datetime
import pandas as pd
import requests

class Fund():

    def __init__(self) -> None:
        self.code = ''
        self.start_date = ''
        self.end_date = ''

    def __crawl_moneydj(self) -> pd.DataFrame:
        url = f'https://www.moneydj.com/funddj/bcd/tBCDNavList.djbcd?a={self.code}&B={self.start_date}&C={self.end_date}&D='
        r = requests.get(url)
        t = r.text
        date_list = t.split(' ')[0].split(',')
        net_value_list = t.split(' ')[1].split(',')
        df = pd.DataFrame({
            'Date': date_list,
            'Net Value': net_value_list
        })
        df['Date'] = df['Date'].apply(lambda s: datetime.strptime(s, '%Y%m%d'))
        df['Date'] = df['Date'].apply(lambda a: a.date())
        df['Net Value'] = df['Net Value'].apply(lambda s: float(s))
        # df = df.rename(columns={'Net Value': 'Close'})
        df = self.__format_dataset(df)
        return df

    def __format_dataset(self, dataset) -> pd.DataFrame:
        fm_dataset = pd.DataFrame()
        fm_dataset['date'] = dataset['Date']
        fm_dataset['price'] = dataset['Net Value']
        return fm_dataset

    def launch(self) -> pd.DataFrame:
        """
        啟動主程式

        :return: DataFrame
        """
        dataset = self.__crawl_moneydj()
        return dataset
