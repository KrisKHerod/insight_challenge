'''
This function will find all of the resources that have status 404, which hosts tried to access them, and how many times they tried to access it
'''

from collections import Counter, defaultdict

def get_badsites(log_file, badsites_path):

	if not log_file.load: return False

	status_file = log_file.status

	
	# create a "defaultdict"
	badsites_grouped = defaultdict(list)


	for resource in zip(log_file.status, log_file.resource, log_file.host):
		if (resource[0] == 404):
			badsites_grouped[resource[1]].append(resource[2])

	badsites = []

	for resource, hosts in badsites_grouped.items():
		c = Counter(hosts).most_common()
		# print (hosts[1])
		# print (c)
		for host in c:
			badsites.append((resource, host[0], host[1]))


	with open(badsites_path, 'w') as badsites_logfile:
		for badsite in badsites:
			badsites_logfile.write('%s\n' %','.join([str(x) for x in badsite]))





