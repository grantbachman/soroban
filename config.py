import os
import urlparse
import re

# reads env vars from .dev_env and .prod_env files

# returns a hash of environment variables
def get_env():
	files = {'development': '.dev_env',
			  'production': '.prod_env'}

	# if no env var is set, set to development
	if not os.environ.get('ENV_MODE'):
		os.environ['ENV_MODE'] = 'development'

	try:
		with open(files[os.environ['ENV_MODE']]) as f:
			content = f.read()
	except IOError:
		pass

	env = {}
	# set env-dictionary by parsing file
	for line in content.splitlines():
		match = re.match(r'\A([A-Za-z0-9_]+)=(.*)\Z',line)
		env[match.group(1)]=match.group(2)

	# parse Heroku's DATABASE_URL variable
	if env['ENV_MODE'] == 'production': 
		urlparse.uses_netloc.append('postgres')
		url = urlparse.urlparse(env['DATABASE_URL'])
		env['DBNAME'] = url.path[1:]
		env['USER'] = url.username
		env['PASSWORD'] = url.password
		env['HOST'] = url.hostname
	return env
