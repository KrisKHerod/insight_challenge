'''
this function finds the top 10 most active hosts
'''


# dependencies
from collections import Counter



def get_hosts(log_file, hosts_path):

	if not log_file.load: return False

	# using Counter, count the top 10 most active hosts
	c = Counter(log_file.host).most_common(10)

	# write the file to the log file
	with open(hosts_path, 'w') as hosts:

		# sort the list of tuple in alphanumeric order
		c = sorted(c, key=lambda x: (-x[1], x[0]))
		for tup in c:
			hosts.write('%s\n' %','.join([str(t).strip("'") for t in tup]))

	return True


