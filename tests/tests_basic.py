import src
from src.features import hosts
from src.features import resources
from src.features import hours
from src.features import blocked
from src.features import load

import tests.test_cases.log_input as LOG

'''
LOG
- log_input_simple_good.txt
- log_input_bad_simple_1.txt
- log_input_bad_simple_2.txt

in order to run all tests type:
"python -m unittest tests.test_basic.py"
in terminal

'''

import unittest


class TestFeatures(unittest.TestCase):


	# test the load.py basic and edge cases
	def test_load_simple (self):

		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/log_input_simple_good.txt')

		self.assertEqual(log_file.host, ['199.72.81.55'])
		self.assertEqual(log_file.dates, [804571201])
		self.assertEqual(log_file.timezone, ['-0400'])
		self.assertEqual(log_file.resource, ['GET /history/apollo/ HTTP/1.0'])
		self.assertEqual(log_file.status, [200])
		self.assertEqual(log_file.bytes, [6245])
		self.assertEqual(log_file.lines, ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'])

	# test the edge case 1
	def test_load_edge_1 (self):

		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/log_input_simple_bad_1.txt')

		self.assertEqual(log_file.host, ['intospa.aball.de'])
		self.assertEqual(log_file.dates, [805618482])
		self.assertEqual(log_file.timezone, ['-0400'])
		self.assertEqual(log_file.resource, ['GET /shuttle/missions/sts-69/mission-sts-69.htmlhttp://hamburg.bda.de:800/bda/index_germany.html HTTP/1.0'])
		self.assertEqual(log_file.status, [404])
		self.assertEqual(log_file.bytes, [0])
		self.assertEqual(log_file.lines, ['intospa.aball.de - - [13/Jul/1995:02:54:42 -0400] "GET /shuttle/missions/sts-69/mission-sts-69.htmlhttp://hamburg.bda.de:800/bda/index_germany.html HTTP/1.0" 404 -'])




	# test the _parse.py basic and edge cases
	def test_parse_simple (self):
		
		log_file = load.Data()
		data_input = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245']
		log_file._parse(data_input)

		self.assertEqual(log_file.host, ['199.72.81.55'])
		self.assertEqual(log_file.dates, [804571201])
		self.assertEqual(log_file.timezone, ['-0400'])
		self.assertEqual(log_file.resource, ['GET /history/apollo/ HTTP/1.0'])
		self.assertEqual(log_file.status, [200])
		self.assertEqual(log_file.bytes, [6245])
		self.assertEqual(log_file.lines, ['199.72.81.55 - - [01/Jul/1995:00:00:01 -0400] "GET /history/apollo/ HTTP/1.0" 200 6245'])

	# test the edge case 1
	def test_parse_no_data (self):
		
		log_file = load.Data()
		data_input = ['199.72.81.55 - - [01/Jul/1995:00:00:01 -040sdafasdf sad fsadfsaf sad fsf 0] "GET /history/apollo/ HTTP/1.0" 200 6245']
		log_file._parse(data_input)

		self.assertEqual(log_file.host, [])
		self.assertEqual(log_file.dates, [])
		self.assertEqual(log_file.timezone, [])
		self.assertEqual(log_file.resource, [])
		self.assertEqual(log_file.status, [])
		self.assertEqual(log_file.bytes, [])
		self.assertEqual(log_file.lines, [])



	# test _check methods

	# test check host
	def test_check_host (self):
		log_file = load.Data()
		response = log_file._check_host('sfadf')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.host_tmp, 'sfadf')



	# test check timezone
	def test_check_timezone (self):
		log_file = load.Data()
		response = log_file._check_timezone('sfadf')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.timezone_tmp, 'sfadf')



	# test chcek date good
	def test_check_date_good (self):
		log_file = load.Data()
		response = log_file._check_date('01/Jul/1995:00:00:01')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.dates_tmp, 804571201)

	# test check data bad
	def test_check_date_bad (self):
		log_file = load.Data()
		response = log_file._check_date('01/Jul/199sdfs5:00:00:01')

		self.assertEqual(response, 0)
		self.assertEqual(log_file.dates_tmp, "")	



	# test chcek resource good
	def test_check_resource_good (self):
		log_file = load.Data()
		response = log_file._check_resources('GET /history/apollo/ HTTP/1.0')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.resource_tmp, 'GET /history/apollo/ HTTP/1.0')

	# test check resource bad
	def test_check_resource_bad (self):
		log_file = load.Data()
		response = log_file._check_resources('dddddd')

		self.assertEqual(response, 0)
		self.assertEqual(log_file.resource_tmp, "")



	# test chcek status good
	def test_check_status_good (self):
		log_file = load.Data()
		response = log_file._check_status('200')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.status_tmp, 200)

	# test check status bad
	def test_check_status_bad (self):
		log_file = load.Data()
		response = log_file._check_status('dddddd')

		self.assertEqual(response, 0)
		self.assertEqual(log_file.status_tmp, "")



	# test chcek bytes good
	def test_check_bytes_good (self):
		log_file = load.Data()
		response = log_file._check_bytes('0')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.bytes_tmp, 0)

	# test check bytes bad
	def test_check_bytes_bad (self):
		log_file = load.Data()
		response = log_file._check_bytes('-')

		self.assertEqual(response, 1)
		self.assertEqual(log_file.bytes_tmp, 0)



	# test the hosts files
	def test_hosts_good (self):
		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/host_test_1.txt')

		hosts.get_hosts(log_file, './tests/test_cases/log_output/host_output_test.txt')

		with open('./tests/test_cases/log_output/host_output_test.txt') as test: test = test.read()
		with open('./tests/test_cases/log_output/host_output_1.txt') as real: real = real.read()


		self.assertEqual(test, real)



	# test the resources files
	def test_resources_good (self):
		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/host_test_1.txt')

		resources.get_resources(log_file, './tests/test_cases/log_output/resource_output_test.txt')

		with open('./tests/test_cases/log_output/resource_output_test.txt') as test: test = test.read()
		with open('./tests/test_cases/log_output/resource_output_1.txt') as real: real = real.read()

		self.assertEqual(test, real)



	# test the hours files
	def test_hours_good (self):
		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/host_test_1.txt')

		hours.get_hours(log_file, './tests/test_cases/log_output/hours_output_test.txt')

		with open('./tests/test_cases/log_output/hours_output_test.txt') as test: test = test.read()
		with open('./tests/test_cases/log_output/hours_output_1.txt') as real: real = real.read()

		self.assertEqual(test, real)



	# test the blccked files
	def test_hours_good (self):
		log_file = load.Data()
		log_file.load('./tests/test_cases/log_input/blocked_test_1.txt')

		blocked.get_blocked(log_file, './tests/test_cases/log_output/blocked_output_test.txt')

		with open('./tests/test_cases/log_output/blocked_output_test.txt') as test: test = test.read()
		with open('./tests/test_cases/log_output/blocked_output_1.txt') as real: real = real.read()

		self.assertEqual(test, real)






if __name__=='__main__':
	unittest.main()