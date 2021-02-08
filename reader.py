import pandas as pd
import requests
import time


class GettingData:
    def __init__(self, ticker):
        """
        :param ticker: тикер компании
        """
        self.ticker = ticker

    def get_data(self):
        """
        Запросы к Alpha Vantage
        :return: нужные данные в формате csv
        """
        api = '_KEY_'
        function = 'TIME_SERIES_DAILY'
        output_size = 'full'
        datatype = 'csv'
        url = f"https://www.alphavantage.co/query?function={function}&symbol={self.ticker}&outputsize={output_size}&apikey={api}&datatype={datatype}"
        data = requests.get(url).text
        return data

    def save_csv(self):
        """
        Сохранение результатов запроса в csv-файл
        :return: название csv-файла; string
        """
        with open(f'{self.ticker}.csv', 'w') as f:
            f.write(self.get_data())
        return f'{self.ticker}.csv'


class Reader:
    def __init__(self, csv_file, ticker, start_time, end_time):
        """
        :param csv_file: название csv-файла
        :param ticker: тикер компании
        :param start_time: начало рассматриваемого периода
        :param end_time: конец рассматриваемого периода
        """
        self.csv_file = csv_file
        self.ticker = ticker
        self.start_time = start_time
        self.end_time = end_time

    def get_df(self):
        """
        Чтение csv-файла и преобразование нужных данных в pandas-датайфрейм
        :return: pandas-датафрейм
        """
        columns = ['timestamp', 'close']
        df = pd.read_csv(self.csv_file)
        df = df[columns].rename(columns={'timestamp': 'Date', 'close': f'{self.ticker}'})
        df = df.loc[(df['Date'] >= self.start_time) & (df['Date'] <= self.end_time)]
        df = df.set_index('Date')
        return df


def download_data(tickers):
    """
    Загрузка всех данных и приведение к общей pandas-таблице
    :param tickers: список тикеров рассматриваемых компаний
    :return: pandas-датафрейм, с которым будем работать в дальнейшем
    """
    df = Reader(GettingData(tickers[0]).save_csv(), f'{tickers[0]}', '2017-01-03', '2020-12-01').get_df()
    del tickers[:1]
    time.sleep(60)
    while tickers is not []:
        if len(tickers) > 5:
            n = 5
            for i in range(n):
                df[f'{tickers[i]}'] = (Reader(GettingData(tickers[i]).save_csv(), f'{tickers[i]}', '2017-01-03', '2020-12-01').get_df())[f'{tickers[i]}']
            time.sleep(60)
            del tickers[:n]
        else:
            n = len(tickers)
            for i in range(n):
                df[f'{tickers[i]}'] = (Reader(GettingData(tickers[i]).save_csv(), f'{tickers[i]}', '2017-01-03', '2020-12-01').get_df())[f'{tickers[i]}']
            break
    return df


DJI_tickers = ['MMM',
               'AXP', 'AAPL', 'BA', 'CAT', 'CVX',
               'CSCO', 'KO', 'DOW', 'XOM', 'GS',
               'HD', 'IBM', 'INTC', 'JNJ', 'JPM',
               'MCD', 'MRK', 'MSFT', 'NKE', 'PFE',
               'PG', 'TRV', 'UNH', 'RTX', 'VZ',
               'V', 'WMT', 'WBA', 'DIS']

# final_data = download_data(DJI_tickers)
# print(final_data)