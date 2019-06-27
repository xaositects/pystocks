import sys
sys.path.append('/home/rmiller/Projects/pystocks/lib')
sys.path.append('/home/rmiller/.local/lib/python2.7/site-packages')
import requests
from mod_python import apache
from bs4 import BeautifulSoup
#import numpy as np
#import pandas as
import pandas_datareader.data as web
from datetime import datetime
#import matplotlib.pyplot as plt

#import matplotlib.cm as cm
import seaborn as sns


# import customer functions
vis = apache.import_module('/home/rmiller/Projects/pystocks/lib/stock-analysis/vis.py')
helper = apache.import_module('/home/rmiller/Projects/pystocks/lib/stock-analysis/helper.py')
from vis import plot_candlestick_ohlc
from helper import get_close_price,calculate_metrics


class Charts:
    def __init__(self):
        pass

    def get_ticker_and_sector(self, url='https://en.wikipedia.org/wiki/List_of_S%26P_500_companies'):
        """
        get the s&p 500 stocks from Wikipedia:
        https://en.wikipedia.org/wiki/List_of_S%26P_500_companies

        ---
        return: a dictionary with ticker names as keys and sectors as values
        """

        r = requests.get(url)
        data = r.text
        soup = BeautifulSoup(data, 'lxml')

        # we only want to parse the first table of this wikipedia page
        table = soup.find('table')

        sp500 = {}
        # loop over the rows and get ticker symbol and sector name
        for tr in table.find_all('tr')[1:]:
            tds = tr.find_all('td')
            ticker = tds[0].text
            sector = tds[3].text
            sp500[ticker] = sector

        return sp500

    def get_stock_data(self, ticker, start_date, end_date):
        """ get stock data from google with stock ticker, start and end dates """
        data = web.DataReader(ticker, 'google', start_date, end_date)
        return data

    def get_sp_data(self):
        """ get the stock data from the past 5 years """
        # end_date = datetime.now()
        end_date = datetime(2017, 8, 14)
        start_date = datetime(end_date.year - 5, end_date.month , end_date.day)

        sp500 = self.get_ticker_and_sector()
        sp500['SPY'] = 'SPY' # also include SPY as reference
        print('Total number of tickers (including SPY): {}'.format(len(sp500)))

        bad_tickers =[]
        for i, (ticker, sector) in enumerate(sp500.items()):
            try:
                stock_df = self.get_stock_data(ticker, start_date, end_date)
                stock_df['Name'] = ticker
                stock_df['Sector'] = sector
                if stock_df.shape[0] == 0:
                    bad_tickers.append(ticker)
                #output_name = ticker + '_data.csv'
                #stock_df.to_csv(output_name)
                if i == 0:
                    all_df = stock_df
                else:
                    all_df = all_df.append(stock_df)
            except:
                bad_tickers.append(ticker)
        print(bad_tickers)

        all_df.to_csv('./data/all_sp500_data_2.csv')

        """ Write failed queries to a text file """
        if len(bad_tickers) > 0:
            with open('./data/failed_queries_2.txt','w') as outfile:
                for ticker in bad_tickers:
                    outfile.write(ticker+'\n')
