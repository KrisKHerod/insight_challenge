import sys
import os
import time

import features.load as load
import features.hosts as hosts
import features.resources as resources
import features.hours as hours
import features.blocked as blocked
import features.badsites as badsites

# load all of the paths from run.sh
log_path = sys.argv[1]
hosts_path = sys.argv[2]
hours_path = sys.argv[3]
resources_path = sys.argv[4]
blocked_path = sys.argv[5]
badsites_path = './log_output/badsites.txt'


def check_logfile(log_path):

	if not os.path.exists(log_path):
		with open(log_path, 'w') as log_file:
			return log_path
	else: return log_path



if __name__=="__main__":

	# check python version

	#if (sys.version_info > (3,0)):
	# print (sys.version_info)
	
	# first check if the log file input path exists
	
	# if not os.path.exists(log_path):
	# 	raise ValueError("Log file does not exist")

	# # check if the log file output paths exists, if not create them
	# check_logfile(hosts_path)
	# check_logfile(hours_path)
	# check_logfile(resources_path)
	# check_logfile(blocked_path)
	check_logfile(badsites_path)


	# t0 = time.time()
	log_file = load.Data()
	log_file.load(log_path)
	# print ("loading data took: \t\t", time.time() - t0)

	# print (log_file.file_len, len(log_file.host), len(log_file.resource), len(log_file.dates))

	#get the hosts
	# t0 = time.time()
	hosts.get_hosts(log_file, hosts_path)
	# print ("Getting hosts took: \t\t", time.time() - t0)


	#get the resources
	# t0 = time.time()
	resources.get_resources(log_file, resources_path)
	# print ("Getting resources took: \t", time.time() - t0)


	# get the hours
	# t0 = time.time()
	hours.get_hours(log_file, hours_path)
	# print ("Getting busiest hours took: \t", time.time() - t0)
	

	# get the the blocked users
	# t0 = time.time()
	blocked.get_blocked(log_file, blocked_path)
	# print ("Getting blocked users took: \t", time.time() - t0)


	# get badsites
	# t0 = time.time()
	badsites.get_badsites(log_file, badsites_path)
	# print ("Getting bad resources took:\t", time.time() - t0)




