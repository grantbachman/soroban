import unittest
import config
import os

class TestEnvVars(unittest.TestCase):

	def setUp(self):
		pass

	def tearDown(self):
		print os.environ['ENV_MODE']
		del os.environ['ENV_MODE'] 

	def test_correct_vars_in_dev(self):
		os.environ['ENV_MODE'] = 'development'
		vars = config.get_env()
		print vars['ENV_MODE']
		assert vars['HOST'] == 'localhost'
		assert vars['DBNAME'] == 'soroban'

	def test_correct_vars_in_prod(self):
		os.environ['ENV_MODE'] = 'production'
		vars = config.get_env()
		print vars['ENV_MODE']
		assert vars['DBNAME']
		assert vars['USER']
		assert vars['PASSWORD']

	def test_correct_vars_no_env(self):
		vars = config.get_env()
		print vars['ENV_MODE']
		assert vars['HOST'] == 'localhost'
		assert vars['DBNAME'] == 'soroban'
