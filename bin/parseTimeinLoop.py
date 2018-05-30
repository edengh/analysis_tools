#!/usr/local/bin/python3
#parseTimeinLoop.py

#Calculates months since start of loop date.
#invoke in command line with
#./parseTimeinLoop.py filename.xlsx

import sys
import os
import xlrd
import datetime

def file_open(filename):
    excel = xlrd.open_workbook(filename)
    sheet = excel.sheet_by_index(0)

    for rowindex in range(2,sheet.nrows):
        if (sheet.cell_type(rowindex, 1) == 3):
           data = sheet.row_values(rowindex)
           start_date = xlrd.xldate.xldate_as_datetime(data[1:2][0],0).date()
           today = datetime.date.today()
           time_in_loop = (today - start_date).days
           months = time_in_loop / 30
           print (str(data[0:1][0]) + " " + str(months))

def main():
    argvs = sys.argv[1:]

    if len(argvs) == 0:
        print ("needs at least 1 argument")
        sys.exit(1)
        return

    filename = sys.argv[1]
    file_open(filename)
    
if __name__ == "__main__":
    main()
