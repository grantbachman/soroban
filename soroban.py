import os
import random
import pandas as pd
from types import *
from urllib2 import HTTPError
from httplib import BadStatusLine
from flask import Flask, render_template, redirect, url_for
from pandas.io.data import DataReader
from datetime import datetime, date, timedelta
import psycopg2
import config
from contextlib import closing
import pprint

app = Flask(__name__)

app.config.from_object('config.get_env')

# Returns the connection
def connect_db():
	env = config.get_env()
	if env['ENV_MODE'] == 'production':
		vars = (env['DBNAME'], env['USER'], env['PASSWORD'], env['HOST'])
		return psycopg2.connect("dbname=%s user=%s password=%s host=%s" % vars)	
	else:
		vars = (env['DBNAME'], env['HOST'])
		return psycopg2.connect("dbname=%s host=%s" % vars)
# Creates the table if it doesn't exist

def init_table():
		with closing(connect_db()) as db:
			db.cursor().execute("CREATE TABLE IF NOT EXISTS tweets \
				(id serial, \
				symbol varchar(6) not null, \
				target numeric(9,2) not null, \
				raising_target boolean not null, \
				tweeted boolean not null default false, \
				created_at timestamp not null, \
				tweeted_at timestamp )"
			)
			db.commit()

def print_table():
	conn = connect_db()
	cur = conn.cursor()
	cur.execute("SELECT * FROM tweets")
	rows = cur.fetchall()
	pprint.pprint(rows)

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

def get_all_stock_histories(from_file=False):
	prices,volumes = {},{}
	if from_file == True:
		prices = pd.read_csv('prices.csv', index_col = 0)
		volumes = pd.read_csv('volumes.csv', index_col = 0)		
	else:
		stocks = get_stock_list()
		for stock in stocks:
			x = get_stock_history(stock[0])
			if x is not None:
				prices[stock[0]], volumes[stock[0]] = x["Adj Close"], x["Volume"]
				prices, volumes = pd.DataFrame(prices), pd.DataFrame(volumes)
	return [prices, volumes]


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

def calc(from_file=False):
	prices, volumes = get_all_stock_histories(from_file)
	s_min_vol = volumes.mean() > 1000000 # Boolean Series
	df_min_vol_stocks = prices[list(s_min_vol.index[s_min_vol==True])]

	#l_underperform, l_marketperform, l_outperform = get_ratings(df_min_vol_stocks)
	s_lower_targets, s_rise_targets = get_targets(df_min_vol_stocks)
	return [s_lower_targets, s_rise_targets]	

def save_all_stocks(lower,higher):
	with closing(connect_db()) as db:
		for i in range(len(lower)):
			print "saving %s" % lower.index[i]
			db.cursor().execute("""INSERT INTO tweets
								 (symbol, target, raising_target, created_at)
								 VALUES (%s, %s, %s, %s);""", (lower.index[i], lower[i], False, datetime.now()))
			db.commit()
		for i in range(len(higher)):
			print "saving %s" % higher.index[i]
			db.cursor().execute("""INSERT INTO tweets
								(symbol, target, raising_target, created_at)
								VALUES (%s, %s, %s, %s);""", (higher.index[i], higher[i], True, datetime.now()))
			db.commit()

@app.route('/ratings')
def ratings():
    stock = {}
    return render_template('ratings.html',stock=stock)

if __name__ == '__main__':
	app.run()
