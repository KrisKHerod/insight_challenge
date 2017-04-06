'''
this function loads the logfile into readable python format

Loading takes longer so that the other features can be executed faster and are more scalableg

'''



import os
from datetime import datetime
import time
import io



class Data:

	def __init__(self):

		self.data = False
		self.file_len = 0

		# store lists of all of the values
		self.host, self.host_index = [], 0
		self.dates, self.dates_index = [], 3
		self.timezone, self.timezone_index = [], 4
		self.resource = []
		self.status, self.status_index = [], 5
		self.bytes, self.bytes_index = [], 6
		self.lines = []

		# temporary storage of value before they get committed
		self.host_tmp = ""
		self.dates_tmp = ""
		self.timezone_tmp = ""
		self.method_tmp = ""
		self.resource_tmp = ""
		self.status_tmp = ""
		self.bytes_tmp = ""

		self.month_abbreviations = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4,
		                       'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8,
		                       'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}


	# helper function to conver the string to unix timestamp
	def _strtodate(self, date):

		# get the values of the different parts of the date
		year = int(date[7:11])
		month = self.month_abbreviations[date[3:6]]
		day = int(date[0:2])
		hour = int(date[12:14])
		minute = int(date[15:17])
		second = int(date[18:20])
		# convert date string into unix timestamp
		return int(datetime(year, month, day, hour, minute, second).timestamp())

	# function to check if the data is properly formatted
	def _check_date(self, data):
		try:
			self.dates_tmp = Data._strtodate(self, data)
			return 1
		except:
			return 0

	# function to check the host
	def _check_host(self, data):
		self.host_tmp = data
		return 1

	# function to check the timezone
	def _check_timezone(self, data):
		self.timezone_tmp = data
		return 1

	# function to check the resource
	def _check_resources(self, data):

		if '/' in data:
			self.resource_tmp = data
			return 1
		else:
			# print (i)
			# self.resource_tmp = data
			return 0

	# function to check the status
	def _check_status(self, data):
		if data.isdigit():
			self.status_tmp = int(data)
			return 1
		else:
			# self.status_tmp = int(data)
			return 0

	# function to check the bytes
	def _check_bytes(self, data):

		if data.isdigit():
			self.bytes_tmp = int(data)
			return 1
		else:
			# self.bytes.append(0)
			self.bytes_tmp = 0
			return 1

	def _commit(self):

		self.host.append(self.host_tmp)
		self.dates.append(self.dates_tmp)
		self.timezone.append(self.timezone_tmp)
		self.resource.append(self.resource_tmp)
		self.status.append(self.status_tmp)
		self.bytes.append(self.bytes_tmp)

		return 1


	# function to parse the file lines
	# this function takes longer since it  parses every line in the log file which makes the getting the features easier and more scalable
	def _parse(self, data):

		for i, line in enumerate(data):

			# check if there is a quotation in the line, if not then the program wont work
			if '"' not in line: continue

			# get the index of the first and last quote where the method is stored
			i1, i2 = line.index('"'), line.rindex('"')

			# split the string into method and everything else
			resource, rest = line[i1+1:i2], line[:i1]+line[i2+2:]

			# split the rest into a list delimited by a space
			line_frmt = rest.strip('\n').split(' ')

			# check all of the columns
			if not Data._check_date(self, line_frmt[self.dates_index].strip('["')): continue
			if not Data._check_host(self, line_frmt[self.host_index]): continue
			if not Data._check_timezone(self, line_frmt[self.timezone_index].strip('"]')): continue
			if not Data._check_resources(self, resource): continue
			if not Data._check_status(self, line_frmt[self.status_index]): continue
			if not Data._check_bytes(self, line_frmt[self.bytes_index]): continue			

			# if the columns are good then commit them
			Data._commit(self)
			self.lines.append(line)

		return True


	# function to load the logfile
	def load(self, path):

		with io.open(path, 'r', encoding='ascii', errors='ignore') as f:
			# iterate through all lines and split them by new line
			log_file = f.readlines()

		self.file_len = len(log_file)
		self.data = Data._parse(self, log_file)


