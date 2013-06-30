import soroban as s
import os
import config
import random
import pprint
from twitter import *
from datetime import datetime, timedelta
from contextlib import closing
from connect import DBConnection
from config import get_env

if __name__ == '__main__':
	env = get_env()
	# only execute Mon-Fri 8am-4pm EST
	est = (datetime.utcnow() + timedelta(hours=-4)).timetuple()
	# est[6] = day (Mon = 0, Fri = 4)
	# est[3] = hour (8am = 8, 3pm = 16)
	#if est[6] in range(5) and
	if est[3] in range(8,16):
		conn = DBConnection()
		cur = conn.connection.cursor()
		cur.execute("""SELECT * FROM tweets WHERE tweeted = False""")
		rows = cur.fetchall()
		num_rows = len(rows)
		# tweet times left in week formula
		# daysofweek = 4
		# dayofweek = 0 on Monday, 4 on Friday
		# endofdayhour = 16
		# currenthour = 8 at 8am, 16 at 4pm
		# (daysinweek - dayofweek) * 9 - (endofdayhour - currenthour) + 1
		tweet_times_left = (4 - est[6]) * 9 + (16 - est[3])

		auth = OAuth(env['TWITTER_OAUTH_TOKEN'], env['TWITTER_OAUTH_SECRET'],
					 env['TWITTER_CONSUMER_KEY'], env['TWITTER_CONSUMER_SECRET'])
		t = Twitter(auth=auth)
		while num_rows / tweet_times_left >= 1:
			stock=random.choice(rows)
			move = 'Raising' if stock[3] else 'Lowering'
			status = "%s our target for $%s to $%s." % (move, stock[1], stock[2])
			print status
			t.statuses.update(status=status)
			conn.mark_as_tweeted(stock[0])
			conn.connection.commit()
			num_rows -= 1
	else:
		print "Sorry, the day is over."