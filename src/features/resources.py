'''
this function finds the top 10 most resouces with the highest bandwidth
'''


# dependencies
from collections import defaultdict


def get_resources (log_file, resources_path):

	if not log_file.load: return False

	# create a "defaultdict"
	grouped_resouces = defaultdict(list)

	# group all of the unique resources together with the bytes from each resource

	for resource in zip(log_file.resource, log_file.bytes):
		grouped_resouces[resource[0]].append(resource[1])

	# create a new tuple with the resource and the average bytes
	resource_bandwidth = []
	for key, val in dict(grouped_resouces).items():
		resource_bandwidth.append((key, sum(val)*len(val)))

	# select the top 10 resouces and write them to the log file
	with open(resources_path, 'w') as resource_logfile:

		# sort the resource_bandwidth
		resource_bandwidth = sorted(resource_bandwidth, key = lambda x: (-x[1], x[0]))[:10]

		for resource in resource_bandwidth:

			resource_frmt = resource[0]
			# format the output by removing the method tag
			rm = ['POST ', 'GET ', 'HEAD ']
			for substring in rm:
				if substring in resource[0]:
					resource_frmt = resource[0].replace(substring, '')

			resource_frmt = resource_frmt.replace(' HTTP/1.0', '')

			resource_logfile.write('%s\n' %str(resource_frmt))

	return True





