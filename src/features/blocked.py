
# dependencies
from datetime import datetime, timedelta


def get_blocked(log_file, blocked_path):

	if not log_file.load: return False

	temp_usr_attempt = {}
	temp_usr_time = {}
	temp_usr_blocked = {}

	with open(blocked_path, 'w') as blocked_logfile:

		for status, time, ip, log in zip(log_file.status, log_file.dates, log_file.host, log_file.lines):


			# check if the ip is already blocked
			if ip in temp_usr_blocked:

				# check if their time is up
				if time > temp_usr_blocked[ip] + 5*60:
					# their 5 minute period is up so now they can attempt to login again
					del temp_usr_blocked[ip]
				else:
					# log the line to the logfile
					blocked_logfile.write('%s' %log)

					continue

			else: pass


			# check if the login succeeded
			if int(status) == 401:

				# check if the user exists in the hash table to determine whether a record should be added
				if ip in temp_usr_attempt:
					temp_usr_attempt[ip] += 1
				else:
					temp_usr_attempt[ip] = 1
					temp_usr_time[ip] = time

				if temp_usr_attempt[ip] > 3:

					if time < temp_usr_time[ip] + 20:
						temp_usr_blocked[ip] = time

						# log line to the log file
						blocked_logfile.write('%s' %log)

						# delete their record from 'temp_usr_time' and 'temp_usr_attemp' hash tables since they will be pardoned after 5 min
						del temp_usr_time[ip]
						del temp_usr_attempt[ip]

					else: 
						# delete their record from 'temp_usr_time' and 'temp_usr_attemp' hash tables since they did not exceed 3 attempts in under 20 seconds
						del temp_usr_time[ip]
						del temp_usr_attempt[ip]

			else:
				if ip in temp_usr_attempt:
					# if they failed a login attempt then it is now pardoned
					del temp_usr_time[ip]
					del temp_usr_attempt[ip]
				else: pass


	return True

