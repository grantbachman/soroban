import unittest
from stock_data import StockData
import pandas as pd

class TestStockData(unittest.TestCase):

	def setUp(self):
		self.stocks = StockData()		

	def test_retrieve_stock_is_list(self):
		assert type(self.stocks.stock_list) is list

	def test_stock_list_has_data(self):
		assert len(self.stocks.stock_list) > 5400

	@unittest.skip("need to learn to mock things")
	def test_retrieve_single_stock_is_dataframe(self):
		history = self.stocks.get_history("AAPL")
		assert type(history) is pd.DataFrame

	@unittest.skip("need to learn to mock things")
	def test_single_stock_has_data(self):
		history = self.stocks.get_history("AAPL")
		assert len(history) > 245

	def test_set_histories_sets_variables(self):
		self.stocks.set_histories(from_file=True)
		prices, volumes = self.stocks.prices, self.stocks.volumes
		assert type(prices) is pd.DataFrame
		assert type(volumes) is pd.DataFrame
		assert type(prices['AAPL']) is pd.Series
		assert type(volumes['GOOG']) is pd.Series

	def test_filter_by_volume(self):
		self.stocks.set_histories(from_file=True)
		self.stocks.filter_by_volume()
		filtered = self.stocks.filter_by_volume(min=1000000)
		assert len(self.stocks.prices.columns) > len(filtered.columns)





