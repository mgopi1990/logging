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
	end_date  = datetime.datetime(yr+1, 1, 1) if (today.year != yr) else today
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
	log_stat['summary'][yr] = {}
	for status in LogStatus:
		log_stat['summary'][yr].setdefault(status.value, 0)

	#print (log_stat['summary'])

	## Update days count
	log_stat['summary'][yr].setdefault('days', 0)
	log_stat['summary'][yr]['days'] += len(year_data['date'])

	#print (year_data)

	## count summary
	for date in list(year_data['date'].keys()):
		status = year_data['date'][date]
		log_stat['summary'][yr][status] += 1

		## remove complete from list
		if (status == LogStatus.COMPLETE):
			del(year_data['date'][date])

	## update summary total
	log_stat['summary'].setdefault('Total', {})
	for k in log_stat['summary'][yr].keys():
		log_stat['summary']['Total'].setdefault(k, 0)
		log_stat['summary']['Total'][k] += log_stat['summary'][yr][k]

	## store brief info for the year
	log_stat['brief'][yr] = year_data


def print_buf(buf):
	for line in buf:
		print (' ' + ''.join(line))
	print ('')


def prep_buf_header (date):

	## prepare buffer to print 
	buf = ['', [], [], [], []]
	buf[0] = '      Mo Tu We Th Fr Sa Su Mo Tu We Th Fr Sa Su Mo Tu We Th Fr Sa Su'

	## prepare buffer header
	str_yr = str(date.year)
	str_mon = date.strftime('%b').upper() 
	buf[1].append(str_yr[0] + ' ' + ' '		   + ' ' + 'H')
	buf[2].append(str_yr[1] + ' ' + str_mon[0] + ' ' + 'H')
	buf[3].append(str_yr[2] + ' ' + str_mon[1] + ' ' + 'M')
	buf[4].append(str_yr[3] + ' ' + str_mon[2] + ' ' + 'M')

	## reset all date entries
	for i in range(0, 22):
		buf[1].append('   ')
		buf[2].append('   ')
		buf[3].append('   ')
		buf[4].append('   ')

	return buf

			
def update_buf (buf, date, result):
	day_diff =  datetime.datetime(date.year, date.month, 1).weekday()
	row = (date.day + day_diff) // 22
	col = ((date.day + day_diff) % 22) + row

	if (result == LogStatus.MISSING):
		buf[3 + row][col] = '{:3}'.format(date.day)	
	elif (result == LogStatus.HALFDONE):
		buf[1 + row][col] = '{:3}'.format(date.day)	


def print_missing_cal (log_stat):
	for yr in log_stat['brief'].keys():
		month = 1
		buf = prep_buf_header (datetime.datetime(yr, month, 1))
		for str_date,result in log_stat['brief'][yr]['date'].items():
			date = datetime.datetime.strptime(str_date, '%d%b%Y')
			if (month != date.month):
				print_buf (buf) 
				buf = prep_buf_header (date)
				month = date.month
			update_buf (buf, date, result)
	print_buf (buf)


def print_stat_summary (log_stat):
	print (' Stats:')

	## we want the total to be in the end
	## idiot, mixed int (year) with str 'Total'
	temp_summary_list = list (log_stat['summary'].keys())
	temp_summary_list.remove('Total')
	temp_summary_list.sort()
	temp_summary_list.append('Total')

	for yr in temp_summary_list:
		print (f' {yr}:')
		print ('  Missing Count   : {}'.format(
					log_stat['summary'][yr][LogStatus.MISSING.value]))
		print ('  Incomplete Count: {}'.format(
					log_stat['summary'][yr][LogStatus.HALFDONE.value]))
		print ('  Total days to do: {}/{}'.format(
            (log_stat['summary'][yr][LogStatus.MISSING.value] + 
			 log_stat['summary'][yr][LogStatus.HALFDONE.value]), 
            str(log_stat['summary'][yr]['days'])))
		print ('')


def print_stat(log_stat):
	print_missing_cal (log_stat)
	print_stat_summary (log_stat)


if __name__ == '__main__':
	log_stat = build_log_stats()
	print_stat(log_stat)

