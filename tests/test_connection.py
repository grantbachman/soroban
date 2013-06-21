import unittest
import psycopg2
from connect import DBConnection
from contextlib import closing

class TestConnection(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		pass

	# Implicitly tests that database exists
	def test_db_connection_exists(self):
		conn = DBConnection().connection
		assert type(conn) is psycopg2._psycopg.connection

	def test_correct_columns_exist(self):
		must_exist = ['id', 'symbol', 'target',
					  'raising_target', 'created_at', 'tweeted_at']
		conn = DBConnection().connection
		cur = conn.cursor()
		for col_name in must_exist:
			cur.execute("""SELECT column_name
					   FROM information_schema.columns
					   WHERE table_name='tweets'
				   	   AND column_name=%s;""", (col_name,))
			assert len(cur.fetchall()) == 1


	def test_save_tweet(self):
		conn = DBConnection()
		tweet_vars = ('AAPL', '500.00', 'True')
		saved = conn.save_tweet(*tweet_vars)
		assert saved is True


