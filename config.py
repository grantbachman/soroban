import os
import urlparse

def dev_config():
	ENV_MODE = 'development'
	DBNAME = 'soroban'
	HOST = 'localhost'
	DEBUG = True	

def prod_config():
	urlparse.uses_netloc.append('postgres')
	url = urlparse.urlparse(os.environ['DATABASE_URL'])
	ENV_MODE = 'production'
	DBNAME = url.path[1:]
	USER = url.username
	PASSWORD = url.password
	HOST = url.hostname
	DEBUG = False
