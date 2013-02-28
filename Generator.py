#-------------------------------------------------------------------------------
# Name:     Lending Club Generator Module
# Purpose:  Used to iterate through combinations of loan filters.
#              - The generator class subclasses Thread.
# Author:   Zachariah Kendall
# Log:      01/--/2013 - Created
#           02/20/2013 - Made to run in seperate thread
#-------------------------------------------------------------------------------

from itertools import combinations
import threading #from threading import Thread
import time

# Filter options #
useFilter = {"employmentLength": False, "homeOwnership": False, "loanLength": False, \
                 "inquiriesSixMonths": False, "creditGrade": False, "ficoRange": False, \
                 }  #"status": True
employmentLength = {"'1'": False, "'2'": False, "'3'": True, "'4'": True, "'5'": False}
homeOwnership = {"'MORTGAGE'": True, "'OTHER'" : False, "'OWN'" : True, "'RENT'": True}
loanLength = {"'36 months'": True, "'60 months'": False}
inquiriesSixMonths = {"'1'": False, "'2'": False, "'3'": True, "'4'": True, "'5'": False}
creditGrade = {"'A'": False, "'B'": False, "'C'": True, "'D'": True,\
                "'E'": False, "'F'": False, "'G'": False}
ficoRange = {"'640-675'": False, "'676-700'": False, "'701-725'": True,\
                 "'726-750'": True, "'751-775'": False,\
                 "'776-800'": False, "'801-825'": False, "'826-850'": False}
##ficoRangeMin = 640   # low is 640
##ficoRangeMax = 850   # High is 850
status = {"'In Review'": False, "'Issued'": False, "'Current'": False, \
        "'Fully Paid'": True, "'In Grace Period'": False, "'Late (16-30 days)'": False, \
        "'Late (31-120 days)'": False, "'Performing Payment Plan'": False, \
        "'Charged Off'": True, "'Default'": True}
        # How will I handle status?! That is why the roi is so low.
        #  There are lots of loans in review, in progress, etc... That produce an
        #  unreliable ROI.

# Other Options #
doPrint = True      # Print selections and queries
numFilters = 4      # How many filters to select at once
valueCount = 4      # How many values to select at once
minNoteCount = 300  # The minimum number of notes to make it into 'highest'

# Other Storage #
highestROI = 0
highestCount = 0
highestQuery = ""
queryCount = 0

# Other Other #
#abortEvent = threading.Event()


def getFilter(f):
    dic = eval(f)
    ret = "%s in (" % (f) + ", ".join([key for key in dic.keys() if dic[key] == True]) + ")"
    return ret


def buildQuery():
    criteria = ['']
    for f in useFilter.keys():
        if useFilter[f] == True:
            criteria.append(getFilter(f))

    criteria.append(getFilter("status"))  # Always, use this? -> Handles all else being false...

    final = [x for x in criteria if x]
    query = "SELECT AVG(roi), COUNT(roi) FROM loan WHERE %s" % (" AND ".join(final))
    if doPrint:
        print "SQl Query:\t\t\t", query
    return query


def runGenerator(db, abortEvent):
    if not db.dbLoaded:
        print "Databse is not loaded"
        return
    print "Generating. . ."
    global numFilters
    #global abortEvent
    global highestROI
    global highestCount
    global highestQuery
    global queryCount
    global valueCount
    global minNoteCount
    startTime = time.time()
    # Select filter set
    for f in combinations(useFilter.keys(), numFilters):
        if abortEvent.is_set():
            print "Aborting..."
            return False
            
        # Turn off all filters
        for k in useFilter.keys():
            useFilter[k] = False
        # Turn on selected set
        for k in f:
            useFilter[k] = True

        # Print selected
        if doPrint:
            print "Selected filters: \t", [a for a in useFilter.keys() if useFilter[a] == True]

        #Use filters....


        for f in useFilter.keys():
            if useFilter[f] == True:
                # Cycle filters properties!
                optionList = eval(f)
                # Select values in filter
                for selected in combinations(optionList.keys(), valueCount):
                    # if abortEvent.is_set():
                    #     print "Aborting..."
                    #     return False

                    # Turn off all options
                    for v in optionList.keys():
                        optionList[v] = False

                    # Turn on selected set
                    for v in selected:
                        optionList[v] = True

                    # Test values
                    query = buildQuery()
                    result = db.getROIandCount(query)
                    if result[0] > highestROI and result[1] > minNoteCount:
                        highestROI = result[0]
                        highestCount = result[1]
                        highestQuery = query
                    queryCount = queryCount + 1

    # Print Results #
    print "===================================================================="
    print "Highest ROI:\t", highestROI
    print "Highest Query:\t", highestQuery
    print "Highest Count:\t", highestCount
    print "\nNumber of Queries:\t", queryCount
    print "Elapsed Time: ", time.time() - startTime

    # Finished
    return True  


class MyThread(threading.Thread):
    """Use class to easily thread"""
    # Should be daemon thread?

    def __init__(self, db):
        # Db must be passed as arg
        self._abortEvent = threading.Event()
        self._abortEvent.clear()
        super(MyThread, self).__init__(target=runGenerator, name="MyThread", args=(db, self._abortEvent))
        

    def stop(self):
        self._abortEvent.set()

    def stopped(self):
        return self._abortEvent.isSet()
