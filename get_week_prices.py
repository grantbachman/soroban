from datetime import datetime, timedelta
from connect import DBConnection

if __name__ == '__main__':
	est = (datetime.utcnow() + timedelta(hours=-4)).timetuple()
	conn = DBConnection()
	count_untweeted = conn.get_num_untweeted_stocks()
	if est[6] == 6 or count_untweeted == 0:
		sd = StockData()
		sd.set_histories(from_file=True)	
		p = Predict(sd.prices)
		raise_targets = p.find_raise_targets(-10,1.15,1.25)
		lower_targets = p.find_lower_targets(-30,.75,.85)
		p.save_targets(raise_targets, True)
		p.save_targets(lower_targets, False)
