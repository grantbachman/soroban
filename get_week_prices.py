import soroban as s

if __name__ == '__main__':
	lower, higher = s.calc(from_file=True)
	s.save_all_stocks(lower,higher)
