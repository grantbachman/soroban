import os
import urlparse
import re

# Read from .env file (if it exists), otherwise read from ENV variables

def get_env():
	try:
		with open('.env') as f:
			content = f.read()
	except IOError:
			content = ''

	if content:
		env = {}
		for line in content.splitlines():
			match = re.match(r'\A([A-Za-z0-9_]+)=(.*)\Z',line)
			env[match.group(1)]=match.group(2)
		return env
	else:
		return os.environ

def dev_config():
	return {
		'ENV_MODE' : 'development',
		'DBNAME' : 'soroban',
		'HOST' : 'localhost',
		'DEBUG' : True
	}

def prod_config():
	urlparse.uses_netloc.append('postgres')
	url = urlparse.urlparse(os.environ['DATABASE_URL'])
	return {
		'ENV_MODE' : 'production',
		'DBNAME' : url.path[1:],
		'USER' : url.username,
		'PASSWORD' : url.password,
		'HOST' : url.hostname,
		'DEBUG' : False
	}