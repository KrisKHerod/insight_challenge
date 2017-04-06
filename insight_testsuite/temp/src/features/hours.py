'''
this function finds the top 10 busiest hours
'''

# dependencies
from datetime import datetime
import bisect


def get_hours (log_file, hours_path):

	if not log_file.load: return False

	dates_file = log_file.dates
	timezone = log_file.timezone

	busiest_hours = []

	# iterate through all possible times between the ranges
	for i, timestamp in enumerate(range(dates_file[0], dates_file[-1])):

		# get the value of the next hour
		next_hour = timestamp + 3600

		# use the bisect method to get the index of the list which contains a timestamp greater than the next hour
		# subtract 1 so that you get the value greater than or equal to the first value
		i1 = bisect.bisect(dates_file, timestamp-1)
		i2 = bisect.bisect(dates_file, next_hour)

		# create a tuple with the timestamp of the start of the busiest hour, the index, and the difference
		busiest_hours.append((timestamp, i1, i2-i1))

	# log the data to the hours file
	with open(hours_path, 'w') as hours_logfile:

		# sort the data
		busiest_hours = sorted(busiest_hours, key=lambda x: (-x[2], x[0]))[:10]
		for hour in busiest_hours:
			hours_logfile.write('%s %s,%d\n' %(str(datetime.fromtimestamp(hour[0]).strftime('%d/%b/%Y:%H:%M:%S')), timezone[hour[1]] ,hour[2]))


	return True