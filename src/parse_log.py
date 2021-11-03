#!/usr/bin/env python3

import datetime
import os
import sys

HOME_DIR = '/home/pi/gopi/gopi_updates/logging/'
START_DATE = '21Mar2020'

LOG_DIR = HOME_DIR + 'logs/'

MISSING  = 0
HALFDONE = 1
COMPLETE = 2

today = datetime.datetime.now()

def build_log_stats():
  
    if not os.path.exists(HOME_DIR):
        print (' ERROR: Home Dir ({}) missing'.format(HOME_DIR)) 
        sys.exit()

    ## Prepare file list 
    log_file_names = []
    for root, dirs, files in os.walk(LOG_DIR):
        log_file_names.extend(files)    

    #print (log_file_names)

    temp_date = datetime.datetime.strptime(START_DATE,'%d%b%Y')
    log_stat = {}
    log_stat['count'] = {}
    log_stat['dates'] = []
    log_stat['count']['halfdone'] = 0
    log_stat['count']['missing'] = 0
    log_stat['count']['complete'] = 0
    log_stat['count']['days'] = 0
    while (temp_date <= today):
        log_done_name = '{}.txt'.format(temp_date.strftime('%d%b%Y'))
        log_half_name = '{}_.txt'.format(temp_date.strftime('%d%b%Y'))
        if (log_done_name in log_file_names): 
            ## Completed logs
            log_stat['count']['complete'] += 1
        elif (log_half_name in log_file_names):
            log_stat['dates'].append ((log_done_name, HALFDONE))
            log_stat['count']['halfdone'] += 1 
        else:
            log_stat['dates'].append ((log_done_name, MISSING))
            log_stat['count']['missing'] += 1 

        temp_date += datetime.timedelta(days=1)
        log_stat['count']['days'] += 1

    return log_stat

def print_stat(log_stat):
    print (' Stats: \n')
    for (log,result) in log_stat['dates']:
        if result == MISSING:
            print ('M  {}  {}'.format(log, 
                datetime.datetime.strptime(log[0:9],'%d%b%Y').strftime('%a')))
        elif result == HALFDONE:
            print ('H     {}  {}'.format(log, 
                datetime.datetime.strptime(log[0:9],'%d%b%Y').strftime('%a')))
    
    print ('\n Missing Count   : {}'.format(log_stat['count']['missing']))
    print (' Incomplete Count: {}'.format(log_stat['count']['halfdone']))
    print (' Total days to do: {}/{}'.format(
            (log_stat['count']['missing'] + log_stat['count']['halfdone']), 
            str(log_stat['count']['days'])))


if __name__ == '__main__':
    log_stat = build_log_stats()
    print_stat(log_stat)

