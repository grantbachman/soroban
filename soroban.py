import os
import random
import pandas as pd
from types import *
from urllib2 import HTTPError
from httplib import BadStatusLine
from flask import Flask, render_template, redirect, url_for
from pandas.io.data import DataReader
from datetime import datetime, date, timedelta


app = Flask(__name__)

@app.route('/')
def home():
	return redirect(url_for('ratings'))

def get_stock_list():
	# get list of stocks (NYSE/NASDAQ) into a list of (symbol, equity) tuples 
	nyse = [tuple(x.strip().split('\t')) for x in open("NYSE.txt")]
	nyse.pop(0)
	nasdaq = [tuple(x.strip().split('\t')) for x in open("NASDAQ.txt")]
	nasdaq.pop(0)
	nyse.extend(nasdaq)
	nyse = [x for x in nyse if x[0].find('-') == -1]	
	return nyse

def get_stock_history(stock):
	prices = None
	try:
		start_date = date.today() - timedelta(days=365)
		prices = DataReader(stock,"yahoo",start=start_date)
	except (HTTPError,BadStatusLine):
		pass
	return prices

def get_all_stock_histories():
	stocks = get_stock_list()
	prices,volumes = {},{}
	for stock in stocks:
		x = get_stock_history(stock[0])
		if x is not None:
			prices[stock[0]] = x["Adj Close"]	
			volumes[stock[0]] = x["Volume"]
			#print stock
	return [pd.DataFrame(prices), pd.DataFrame(volumes)]


def get_targets(prices):
	# Raise target if up 20% in 10 days
	rise = prices.ix[-1]/prices.ix[-10] - 1 > 0.2
	rise_symbols = list(rise.index[rise==True])
	# Lower target if down 20% in 30 days
	lower = prices.ix[-1]/prices.ix[-30] - 1 < -0.2
	lower_symbols = list(lower.index[lower==True])
	s_rise_targets = prices.ix[-1][rise_symbols].apply(lambda x: random.uniform(x*1.15,x*1.25))
	s_lower_targets = prices.ix[-1][lower_symbols].apply(lambda x: random.uniform(x*0.75,x*0.85))
	return [s_lower_targets, s_rise_targets]

def get_ratings(prices):
	# "Outperform" if down 15% in last year and up 10% in last month
	out = (prices.ix[-1]/prices.ix[0] - 1 < -0.15) & (prices.ix[-1]/prices.ix[-25] - 1 > 0.10)
	out_symbols = list(out.index[out == True])
	# "Underperform" if up 15% in last year and down 5% in last month
	under = (prices.ix[-1]/prices.ix[0] - 1 > 0.15) & (prices.ix[-1]/prices.ix[-25] - 1 < 0.05)
	under_symbols = list(under.index[under == True])
	market_symbols = set(prices.columns) - set(out_symbols) - set(under_symbols) 	
	return [under_symbols, market_symbols, out_symbols]

def calc():
	prices, volumes = get_all_stock_histories()
	s_min_vol = volumes.mean() > 1000000 # Boolean Series
	df_min_vol_stocks = prices[list(s_min_vol.index[s_min_vol==True])]

	#l_underperform, l_marketperform, l_outperform = get_ratings(df_min_vol_stocks)
	return [s_lower_targets, s_rise_targets]	

@app.route('/ratings')
def ratings():
    stock = {}
    return render_template('ratings.html',stock=stock)

if __name__ == '__main__':
	app.run(debug=True)
