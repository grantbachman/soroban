import soroban as s
from datetime import datetime, timedelta

if __name__ == '__main__':
	est = (datetime.utcnow() + timedelta(hours=-4)).timetuple()
	if est[6] == 6:
		lower, higher = s.calc(from_file=False)
		s.save_all_stocks(lower,higher)
