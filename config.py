import os
import urlparse
import re

# reads env vars from .dev_env and .prod_env files

def get_env():

	if not os.environ.get('ENV_MODE'):
		os.environ['ENV_MODE'] = 'development'

	if os.environ.get('ENV_MODE') == 'production':
		db_url=os.environ.get('DATABASE_URL')
		if db_url is not None:
			urlparse.uses_netloc.append('postgres')
			url = urlparse.urlparse(db_url)
			os.environ['DBNAME'] = url.path[1:]
			os.environ['USER'] = url.username
			os.environ['PASSWORD'] = url.password
			os.environ['HOST'] = url.hostname

	# if development environment, throw env_file contents into env variables
	if os.environ.get('ENV_MODE') == 'development':
		try:
			with open('.dev_env') as f:
				content = f.read()

			for line in content.splitlines():
				match = re.match(r'\A([A-Za-z0-9_]+)=(.*)\Z',line)
				os.environ[match.group(1)]=match.group(2)
		except:
			pass

	return os.environ
