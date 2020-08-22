#!/usr/bin/env python3

import datetime
import os
import sys

HOME_DIR = '/home/pi/gopi/gopi_updates/logging/'
START_DATE = '21Mar2020'

LOG_DIR = HOME_DIR + 'logs/'

today = datetime.datetime.now()

def find_missing():
  
    if not os.path.exists(HOME_DIR):
        print (' ERROR: Home Dir ({}) missing'.format(HOME_DIR)) 
        sys.exit()

    ## Prepare file list 
    log_file_names = []
    for root, dirs, files in os.walk(LOG_DIR):
        log_file_names.extend(files)    

    print (log_file_names)

    temp_date = datetime.datetime.strptime(START_DATE,'%d%b%Y')
    missing_logs = []
    while (temp_date <= today):
        log_done_name = '{}.txt'.format(temp_date.strftime('%d%b%Y'))
        log_half_name = '{}_.txt'.format(temp_date.strftime('%d%b%Y'))
        if ((log_done_name not in log_file_names) and 
            (log_half_name not in log_file_names)):
           missing_logs.append(log_done_name) 
        temp_date += datetime.timedelta(days=1)
    return missing_logs

missing_logs = find_missing()
print (' Missing: \n' + '\n  '.join(missing_logs) + '\n')
print (' Count  : ' + str(len(missing_logs)))

