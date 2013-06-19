#!/usr/bin/env python

import unittest
import pandas as pd
from stock_data import StockData, Predict

class TestPredict(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	def test_prices_dataframe_is_set(self):
		prices = pd.DataFrame()
		p = Predict(prices)	
		assert p.prices is not None 

	def test_raise_price_targets_is_series(self):
		sd = StockData()
		sd.set_histories(from_file=True)
		p = Predict(sd.prices)
		raise_targets = p.find_raise_targets(-10,1.15,1.25)
		assert type(raise_targets) is pd.Series

	def test_lower_price_targets_is_series(self):
		sd = StockData()
		sd.set_histories(from_file=True)
		p = Predict(sd.prices)
		lower_targets = p.find_lower_targets(-30,.75,.85)
		assert type(lower_targets) is pd.Series

