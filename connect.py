#!/usr/bin/env python

import psycopg2
from config import get_env
from datetime import datetime

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

	def save_tweet(self, symbol, target, raising_target):
		try:
			self.connection.cursor().execute("""INSERT INTO tweets
									(symbol, target, raising_target, created_at)
									VALUES (%s, %s, %s, %s)""",
									(symbol, target, raising_target, datetime.now()))
			return True 
		except psycopg2.ProgrammingError:
			return False
