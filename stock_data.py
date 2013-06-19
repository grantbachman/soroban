#!/usr/bin/env python

from datetime import datetime, timedelta
import pandas as pd
import random
from pandas.io.data import DataReader
from urllib2 import HTTPError
from httplib import BadStatusLine


# For determining future stock prices
class Predict(object):

	def __init__(self, prices):
		self.prices = prices

	# Make find_raise/find_lower functions just one function
	def find_raise_targets(self,lookback_days,up_min,up_max):
		bool_raise = self.prices.ix[-1]/self.prices.ix[lookback_days] - 1 > 0.2
		raise_symbols = list(bool_raise.index[bool_raise==True])
		s_raise_targets = self.prices.ix[-1][raise_symbols].apply(\
			lambda x: random.uniform(x*up_min,x*up_max)) 
		return s_raise_targets

	def find_lower_targets(self,lookback_days,down_max,down_min):
		bool_lower = self.prices.ix[-1]/self.prices.ix[lookback_days] - 1 < -0.2
		lower_symbols = list(bool_lower.index[bool_lower==True])
		s_lower_targets = self.prices.ix[-1][lower_symbols].apply(\
			lambda x: random.uniform(x*down_max,x*down_min)) 
		return s_lower_targets



# For pulling and filtering stocks
class StockData(object):

	def __init__(self):
		self.stock_list = self.retrieve_stock_list()
		self.prices = None
		self.volumes = None

	# returns a list of tuples (symbol, name)
	def retrieve_stock_list(self):
		nyse = [tuple(x.strip().split('\t')) for x in open("NYSE.txt")]		
		nyse.pop(0)
		nasdaq = [tuple(x.strip().split('\t')) for x in open("NASDAQ.txt")]		
		nasdaq.pop(0)
		nyse.extend(nasdaq)
		nyse = [x for x in nyse if x[0].find('-') == -1]
		return nyse

	# returns a dataframe of prices
	def get_history(self, stock):
		prices = None
		try:
			start_date = datetime.today() - timedelta(days=365)
			prices = DataReader(stock, "yahoo", start=start_date)
		except (HTTPError, BadStatusLine):
				pass
		return prices

	# Sets instance variables 'prices' and 'volumes' with market data
	def set_histories(self, from_file=False):
		if from_file == True:
			prices = pd.read_csv('prices.csv', index_col=0)
			volumes = pd.read_csv('volumes.csv', index_col=0)
		else:
			stocks = retrieve_stock_list()
			for stock in stocks:
				history = get_history(stock[0])	
				if history is not None:
					prices[stock[0]] = history["Adj Close"]
					volumes[stock[0]] = history["Volumes"]
					prices, volumes = pd.DataFrame(prices), pd.DataFrame(volumes)
		self.prices = prices
		self.volumes = volumes

	# returns a dataframe of stocks with their prices
	# whose average volume is greater than the minimum
	def filter_by_volume(self, min=1000000):
		s_min_vol = self.volumes.mean() > min # Boolean Series
		df_min_vol_stocks = self.prices[list(s_min_vol.index[s_min_vol == True])]
		return df_min_vol_stocks
