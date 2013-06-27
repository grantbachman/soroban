import unittest
import config
import os

class TestEnvVars(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		os.environ.pop('ENV_MODE', None)
		os.environ.pop('HOST', None)
		os.environ.pop('DBNAME', None)

	def test_envmode_is_dev_when_not_set(self):
		config.get_env()	
		assert os.environ.get('ENV_MODE') == 'development'

	def test_correct_vars_in_dev(self):
		var = config.get_env()
		assert var['HOST'] == 'localhost'
		assert var['DBNAME'] == 'soroban'
		assert os.environ.get('HOST') == 'localhost'	
		assert os.environ.get('DBNAME') == 'soroban'

	def test_correct_vars_in_prod(self):
		os.environ['ENV_MODE'] = 'production'
		var = config.get_env()
		assert os.environ.get('ENV_MODE') == 'production'
		assert var['ENV_MODE'] == 'production'