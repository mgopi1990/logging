#!/usr/bin/env python3

import datetime
import os
import sys
from enum import IntEnum

HOME_DIR = '/home/pi/gopi/gopi_updates/logging/'
START_DATE = '21Mar2020'

LOG_DIR = HOME_DIR + 'logs/'

class LogStatus(IntEnum):
	MISSING = 0
	HALFDONE = 1
	COMPLETE = 2
			
Months = [	'Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun',
			'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

today = datetime.datetime.now()


def build_year_data_from_text(yr, year_data):

	## collect file list
	log_file_names = []
	for root, dirs, files in os.walk(LOG_DIR + str(yr)):
		log_file_names.extend(files)

	temp_date = datetime.datetime(yr, 1, 1) 
	end_date  = datetime.datetime(yr+1, 1, 1)
	while (temp_date < end_date):
		temp_date_str = temp_date.strftime('%d%b%Y')
		log_done_name = temp_date_str + '.txt'
		log_half_name = temp_date_str + '_.txt'

		#print (f'FILE: {log_done_name} {log_half_name}')

		if (log_done_name in log_file_names): 
			year_data['date'][temp_date_str] = LogStatus.COMPLETE.value
			log_file_names.remove(log_done_name)
		elif (log_half_name in log_file_names):
			year_data['date'][temp_date_str] = LogStatus.HALFDONE.value
			log_file_names.remove(log_half_name)
		else:
			year_data['date'][temp_date_str] = LogStatus.MISSING.value

		temp_date += datetime.timedelta(days=1)

	## we removed known files from the list already 
	year_data['unknown_files'] = log_file_names


def build_year_data(yr):
	year_data = {}
	year_data['date'] = {}
	build_year_data_from_text(yr, year_data)
	return year_data


def build_log_stats():

	if not os.path.exists(HOME_DIR):
		print (' ERROR: Home Dir ({}) missing'.format(HOME_DIR)) 
		sys.exit()

	log_stat = {}
	log_stat['summary'] = {}
	log_stat['brief'] = {}

	## walkthrough the whole years and collect data
	start_date = datetime.datetime.strptime(START_DATE,'%d%b%Y')
	for yr in range(start_date.year, today.year +1):
		year_data = build_year_data(yr)
		update_log_stat(log_stat, yr, year_data)

	return log_stat


def update_log_stat(log_stat, yr, year_data):

	## defaults
	for status in LogStatus:
		log_stat['summary'].setdefault(status.value, 0)

	#print (log_stat['summary'])

	## Update days count
	log_stat['summary'].setdefault('days', 0)
	log_stat['summary']['days'] += len(year_data['date'])

	#print (year_data)

	## count summary
	for date in list(year_data['date'].keys()):
		status = year_data['date'][date]
		log_stat['summary'][status] += 1

		## remove complete from list
		if (status == LogStatus.COMPLETE):
			del(year_data['date'][date])

	log_stat['brief'][yr] = year_data


def print_stat(log_stat):
	print (' Stats: \n')
	for yr in log_stat['brief'].keys():
		for date,result in log_stat['brief'][yr]['date'].items():
			if result == LogStatus.MISSING:
					print ('M  {}  {}'.format(date, 
                datetime.datetime.strptime(date,'%d%b%Y').strftime('%a')))
			elif result == LogStatus.HALFDONE:
					print ('H     {}  {}'.format(date, 
                datetime.datetime.strptime(date,'%d%b%Y').strftime('%a')))

	print ('\n Missing Count   : {}'.format(
				log_stat['summary'][LogStatus.MISSING.value]))
	print (' Incomplete Count: {}'.format(
				log_stat['summary'][LogStatus.HALFDONE.value]))
	print (' Total days to do: {}/{}'.format(
            (log_stat['summary'][LogStatus.MISSING.value] + 
			 log_stat['summary'][LogStatus.HALFDONE.value]), 
            str(log_stat['summary']['days'])))


if __name__ == '__main__':
	log_stat = build_log_stats()
	print_stat(log_stat)

