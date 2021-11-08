#!/usr/bin/env python3

import os
import xlrd
import re
import datetime
import csv

## Global variables
HomeDir = os.path.join('/', 'home', 'pi', 'gopi', 'gopi_updates', 'logging', 'scripts', 'src')
OutputHtmlFile = 'report.html'
OutputCsvFile = 'reportDb.csv'
ExcelReadDir = os.path.join('/', 'home', 'pi', 'gopi', 'gopi_updates', 'logging', 'logs', 'xls')
InputFileTemplate = 'Logging_YYYY.xlsx'
StartDateStr = '01Jan2014'
ExcelKnownStatus = ['IDIOT', 'SHIT' , 'HEROIC']

# The cell where the string 'DATE' is present.
DateCell = 'B3'
# Fix: later fix this.
DateCell = [2,1]

## Global constants
ExcelEpochDate = datetime.datetime(1899, 12, 30)

EndDate = datetime.datetime.now()

## global functions
def DaysInYear(y):
    YearDays = 365
    if y % 400 == 0:
        return (YearDays+1)
    if y % 100 == 0:
        return (YearDays)
    if y % 4 == 0:
        return (YearDays+1) 
    else:
        return (YearDays)

def print_fail_row (heading, FailCount):
    print ('{:6} :{:4}  | FILL_FIRST:{:4}, FILL_LATER:{:4}, FILL_LAST:{:4}, UNKNOWN:{:4}'
           .format(heading,
            FailCount['total'],
            FailCount['fill_first'],
            FailCount['fill_later'],
            FailCount['fill_last'],
            FailCount['others']))

def ExcelGetUnfilledCount(yr):
    FileName = os.path.join(ExcelReadDir, re.sub('YYYY',str(yr),InputFileTemplate))
    wb = xlrd.open_workbook(FileName)
    sheet = wb.sheet_by_index(0)

    Row,Col = DateCell[0],DateCell[1]
    Buff = sheet.cell_value(Row, Col)

    ## confirm we are reading correctly
    if (Buff != 'DATE'):
        return -1

    ## next row can start with date or might be empty
    Row += 1
    Buff = sheet.cell_value(Row, Col)
    if (Buff == ''):
        Row += 1
        ## read the next row
        Buff = sheet.cell_value(Row, Col)
        
    DateXLDay1 = int(Buff)
    ## Confirm we are starting from 1-Jan-YYYY
    TempDate = ExcelEpochDate + datetime.timedelta(days=DateXLDay1)
    if ((TempDate.day != 1) or 
        (TempDate.month != 1) or 
        (TempDate.year != yr)):
        return -1

    FailCount = {
         'total':0,
         'fill_first':0,
         'fill_later':0,
         'fill_last':0,
         'others':0
      }
    for i in range(0, DaysInYear(yr)):
        ExcelFloatDate = sheet.cell_value(Row+i, Col)
        Result = sheet.cell_value(Row+i, Col+3).strip()

        if (int(ExcelFloatDate) != (DateXLDay1 + i)):
            return -1

        if (Result not in ExcelKnownStatus): 
            FailCount['total'] += 1
            if (Result == 'FILL_FIRST'):
                FailCount['fill_first'] += 1
            elif (Result == 'FILL_LATER'):
                FailCount['fill_later'] += 1
            elif (Result == 'FILL_LAST'):
                FailCount['fill_last'] += 1
            elif (Result != ''):
                print ('HERE ' + Result);
                FailCount['others'] += 1

    ## running year; cant write logs for future :P 
    if (yr == EndDate.year):
        FailCount['total'] -= (DaysInYear(EndDate.year) - int(EndDate.strftime('%j')))

    return FailCount


## Script Begins

StartDate = datetime.datetime.strptime(StartDateStr, '%d%b%Y')

count = {}
TotalFailCount = {
         'total':0,
         'fill_first':0,
         'fill_later':0,
         'fill_last':0,
         'others':0
}
for yr in range(StartDate.year, EndDate.year+1):
    count = ExcelGetUnfilledCount(yr)
    for key in TotalFailCount.keys():
        TotalFailCount[key] += count[key]
    print_fail_row(yr, count)

print_fail_row('Total', TotalFailCount)

