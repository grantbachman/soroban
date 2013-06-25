#!/usr/bin/env python

import psycopg2
from config import get_env
from datetime import datetime
import sys

class DBConnection(object):

	env = None
	connection = None

	def __init__(self):
		self.env = get_env()
		self.connection = self.to_db()

	def to_db(self):
		env = self.env
		if env['ENV_MODE'] == 'production':
			vars = (env['DBNAME'], env['USER'], env['PASSWORD'], env['HOST'])
			return psycopg2.connect("dbname=%s user=%s password=%s host=%s" % vars)	
		else:
			vars = (env['DBNAME'], env['HOST'])
			return psycopg2.connect("dbname=%s host=%s" % vars)	

	def mark_as_tweeted(self, id):
		cur = self.connection.cursor()
		try:
			cur.execute("""UPDATE tweets SET tweeted = %s, tweeted_at = %s WHERE id = %s""", (True, datetime.now(), id)) 
			return cur.fetchone()[0]
		except psycopg2.ProgrammingError:
			return -1

	def get_num_untweeted_stocks(self):
		cur = self.connection.cursor()
		try:
			cur.execute("""SELECT COUNT(*) FROM tweets WHERE tweeted = False""")
			return cur.fetchone()[0]
		except psycopg2.ProgrammingError:
			return -1

	def save_tweet(self, symbol, target, raising_target):
		try:
			self.connection.cursor().execute("""INSERT INTO tweets
									(symbol, target, raising_target, created_at)
									VALUES (%s, %s, %s, %s)""",
									(symbol, target, raising_target, datetime.now()))

			self.connection.commit()
			return True 
		except psycopg2.ProgrammingError:
			return False
