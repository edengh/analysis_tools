#!/usr/local/bin/python3
#timeSpent.py

# ./timeSpent.py 'data_directory'

import sys, os, csv, xlrd, datetime

#generates dictionary of id to start dates
def loopDate(startDateFile):
    excel = xlrd.open_workbook(startDateFile)
    sheet = excel.sheet_by_index(0)
    startDates = {}

    for rowindex in range(2,sheet.nrows):
        if (sheet.cell_type(rowindex, 1) == 3):
            data = sheet.row_values(rowindex)
            start_date = xlrd.xldate.xldate_as_datetime(data[1:2][0],0).date()
            startDates[str(int(data[0]))] = start_date

    return startDates

def calculateTime(numberOfReadings, totalNumberofReadings, range):
    percentTimeInRange = (numberOfReadings/totalNumberofReadings) * 100
    timeInRange = numberOfReadings * 5
    print ("Percent time " + range +  ": " + str(percentTimeInRange))
    print ("Time " + range +  " (mins): " + str(timeInRange))

def parseTimeInRanges(filename, lowerRange, upperRange, id, startDateFile):
    startDates = loopDate(startDateFile)
    with open (filename, 'r', newline='') as file:
        csvreader = csv.reader(file,quotechar='|')
        lowcount = 0
        rangecount = 0
        highcount = 0
        totalcount = 0
        lowcountafterloop = 0
        rangecountafterloop = 0
        highcountafterloop = 0
        totalcountafterloop = 0
        
        lowerRange = int(lowerRange)
        upperRange = int(upperRange)
        id = id.split("_")
        id = id[0]
        
        if not id in startDates:
            for row in csvreader:
                bloodSugar = row[1].strip()
                if bloodSugar.isdigit():
                    bloodSugar = int(bloodSugar)
                    if bloodSugar < lowerRange:
                        lowcount += 1
                    elif lowerRange < bloodSugar < upperRange:
                        rangecount += 1
                    elif bloodSugar > upperRange:
                        highcount += 1
                    totalcount += 1
            calculateTime(lowcount, totalcount, "low")
            calculateTime(rangecount, totalcount, "range")
            calculateTime(highcount, totalcount, "high")
        if id in startDates:
            startDate = startDates[id]
            for row in csvreader:
                bloodSugar = row[1].strip()
                #find a way to do a "try this format, then that format, then exception"
                try:
                    try:
                        rowDate = row[0].split("T")[0]
                        rowDate = datetime.datetime.strptime(rowDate, '%Y-%m-%d').date()
                    except ValueError:
                        try:
                            rowDate = row[0].split(" ")[0]
                            rowDate = datetime.datetime.strptime(rowDate, '%m/%d/%Y').date()
                        except ValueError:
                            try:
                                rowDate = row[0].split(" ")[0]
                                rowDate = datetime.datetime.strptime(rowDate, '%Y-%m-%d').date()
                            except ValueError:
                                try:
                                    try:
                                        rowDateList = row[0].split(" ")
                                        rowDate = rowDateList[0] + "-" + rowDateList[1] + "-" + rowDateList[2] + "-" + rowDateList[5]
                                        rowDate = datetime.datetime.strptime(rowDate, '%a-%b-%d-%Y').date()
                                    except IndexError:
                                        pass
                                except ValueError:
                                    pass
                    if rowDate < startDate:
                        if bloodSugar.isdigit():
                            bloodSugar = int(bloodSugar)
                            if bloodSugar < lowerRange:
                                lowcount += 1
                            elif lowerRange < bloodSugar < upperRange:
                                rangecount += 1
                            elif bloodSugar > upperRange:
                                highcount += 1
                        totalcount += 1
                    else:
                        if bloodSugar.isdigit():
                            bloodSugar = int(bloodSugar)
                            if bloodSugar < lowerRange:
                                lowcountafterloop += 1
                            elif lowerRange < bloodSugar < upperRange:
                                rangecountafterloop += 1
                            elif bloodSugar > upperRange:
                                highcountafterloop += 1
                        totalcountafterloop += 1
                except TypeError:
                    totalcount += 1
            calculateTime(lowcount, totalcount, "low before loop")
            calculateTime(rangecount, totalcount, "range before loop")
            calculateTime(highcount, totalcount, "high before loop")
            calculateTime(lowcountafterloop, totalcountafterloop, "low during loop")
            calculateTime(rangecountafterloop, totalcountafterloop, "range during loop")
            calculateTime(highcountafterloop, totalcountafterloop, "high during loop")


def parseTimeInRangesNoFile(filename, lowerRange, upperRange, id):
    with open (filename, 'r', newline='') as file:
        csvreader = csv.reader(file,quotechar='|')
        lowcount = 0
        rangecount = 0
        highcount = 0
        totalcount = 0
        lowerRange = int(lowerRange)
        upperRange = int(upperRange)
        id = id.split("_")
        id = id[0]
        for row in csvreader:
            bloodSugar = row[1].strip()
            if bloodSugar.isdigit():
                bloodSugar = int(bloodSugar)
                if bloodSugar < lowerRange:
                    lowcount += 1
                elif lowerRange < bloodSugar < upperRange:
                    rangecount += 1
                elif bloodSugar > upperRange:
                    highcount += 1
                totalcount += 1
        calculateTime(lowcount, totalcount, "low")
        calculateTime(rangecount, totalcount, "range")
        calculateTime(highcount, totalcount, "high")

#run script on all entries files in folder
def flipThroughPath(path, lowerRange, upperRange, startDateFile = "none"):
    for subdirectory, directory, filenames in os.walk(path):
        for file in filenames:
            filepath = subdirectory + os.sep + file
            if filepath.endswith(".csv") and "entries" in filepath:
                print (file)
                if os.path.isfile(startDateFile):
                    parseTimeInRanges(filepath, lowerRange, upperRange, file, startDateFile)
                else:
                    parseTimeInRangesNoFile(filepath, lowerRange, upperRange, file)

#convert from mmol to mgdl if needed
def mmol(number):
    return (number * 18)

def main():
    argvs = sys.argv[1:]

    if len(argvs) < 3:
        print ("needs at least 3 arguments")
        sys.exit(1)
        return
    
    pathDirectory = sys.argv[1]
    lowerRange = int(sys.argv[2])
    upperRange = int(sys.argv[3])
    if upperRange < 25:
        lowerRange = mmol(lowerRange)
        upperRange = mmol(upperRange)

    if len(argvs) == 3:
        flipThroughPath(pathDirectory, lowerRange, upperRange)
    elif len(argvs) > 3:
        startDateFile = sys.argv[4]
        flipThroughPath(pathDirectory, lowerRange, upperRange, startDateFile)
    
if __name__ == "__main__":
    main()
