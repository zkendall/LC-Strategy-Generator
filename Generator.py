#-------------------------------------------------------------------------------
# Name:     Lending Club Generator Module
# Purpose:  Used to iterate through combinations of loan filters.
#              - The generator class subclasses Thread.
# Author:   Zachariah Kendall
#-------------------------------------------------------------------------------

from itertools import combinations
from scipy.misc import comb
import threading  #from threading import Thread
import time




# Filter options #
filters = {"employmentLength": False, "homeOwnership": False, "loanLength": False,
            "inquiriesSixMonths": False, "creditGrade": False,
            "ficoRange": False}  #"status": True
employmentLength = {"'1'": False, "'2'": False, "'3'": False, "'4'": False,
                    "'5'": False}
homeOwnership = {"'OWN'" : False, "'MORTGAGE'": False, "'RENT'": False,
                 "'OTHER'" : False,}
loanLength = {"'36 months'": False, "'60 months'": False}
inquiriesSixMonths = {"'1'": False, "'2'": False, "'3'": False, "'4'": False,
                    "'5'": False}
creditGrade = {"'A'": False, "'B'": False, "'C'": False, "'D'": False,
                "'E'": False, "'F'": False, "'G'": False}
ficoRange = {"'640-675'": False, "'676-700'": False, "'701-725'": False,
                 "'726-750'": False, "'751-775'": False,
                 "'776-800'": False, "'801-825'": False, "'826-850'": False}
status = {"'In Review'": False, "'Issued'": False, "'Current'": False, 
            "'Fully Paid'": False, "'In Grace Period'": False,
            "'Late (16-30 days)'": False, "'Late (31-120 days)'": False,
            "'Performing Payment Plan'": False, "'Charged Off'": False,
            "'Default'": False}
        # How will I handle status?! That is why the roi is so low.
        #  There are lots of loans in review, in progress, etc... That produce
        #  an unreliable ROI.

def toggleFilter(cat, key, value):
    category = eval(cat)
    category[key] = value
    print category, key, value


# Filter option buckets for generator
use_filters = []
use_employmentLength = []
use_homeOwnership = []
use_loanLength = []
use_inquiriesSixMonths = []
use_creditGrade = []
use_ficoRange = []
use_status = ["'Fully Paid'", "'Charged Off'", "'Default'"]


# Other Options #
doPrint = True      # Print selections and queries
numFilters = 4      # How many filters to select at once
numValues = 3       # How many values to select at once
minNoteCount = 300  # The minimum number of notes to make it into 'highest'

# Other Storage #
highestROI = 0
highestCount = 0
highestQuery = ""
queryCount = 0
totalCombinations = 0
progress = 1

# Other Other #
#abortEvent = threading.Event()

def getCombinationCount():
    """Approximate the number of filter combinations for progress bar"""
    total = 0
    # need to loop from 1 through numFilters. # TO DO #
    for f in filters.keys():
            if filters[f] is True:
                total += 1

    combinations = 0
    for n in xrange(1, numFilters):
        combinations += comb(total, n)

    return combinations


def getFilter(f):
    """Returns and SQL segment for the incoming filter"""
    optionsBucket = eval("use_"+f)
    ret = ""
    if optionsBucket:
        ret = "%s in (" % (f) + ", ".join([o for o in optionsBucket]) + ")"
    return ret


def buildQuery():
    """Returns an SQL string made from enabled filters and options"""
    criteria = ['']
    for f in filters.keys():
        if filters[f] is True:
            criteria.append(getFilter(f))

    # Always, use this? -> Handles all else being false...
    criteria.append(getFilter("status"))

    final = [x for x in criteria if x]
    query = "SELECT AVG(roi), COUNT(roi) FROM loan WHERE %s" % (" AND ".join(final))
    if doPrint:
        print "SQl Query:\t\t\t", query
    return query


def runGenerator(db, abortEvent):
    if not db.dbLoaded:
        print "Database is not loaded"
        return
    print "Generating. . ."
    global numFilters, use_filters, filters
    global highestROI, highestCount, highestQuery
    global queryCount, numValues, minNoteCount
    global totalCombinations, progress
    startTime = time.time()

    totalCombinations = getCombinationCount()
    print "Total Combinations:", totalCombinations

    # Select combinations
    for fcount in xrange(1, numFilters):  # Select from 1 to numFilters.
        for fs in combinations([k for k in filters if filters[k] is True], fcount):

            # Update progress bar
            progress += 1
            print "Progress: ", (progress / totalCombinations)

            # Put selection in use-bucket
            del use_filters[:]
            for i in fs:
                use_filters.append(i)  # Take individual items out of tupple

            # Print selected
            if doPrint:
                print "Selected filters: ", use_filters

            #Use filters; cycle filters' properties
            for f in use_filters:
                optionList = eval(f)
                optionBucket = eval("use_"+f)

                # Select values in filter, out of enabled options
                for vcount in xrange(1, numValues):
                    for selectedValues in combinations([v for v in optionList
                                            if optionList[v] is True], vcount):
                        if abortEvent.is_set():
                            print "Aborting..."
                            return False

                        # Put values in filter's use-bucket
                        del optionBucket[:]
                        for i in selectedValues:
                            optionBucket.append(i)

                        # Test values
                        query = buildQuery()
                        result = db.getROIandCount(query)

                        # Save highest
                        if result[0] > highestROI and result[1] > minNoteCount:
                            highestROI = result[0]
                            highestCount = result[1]
                            highestQuery = query

                        queryCount += 1


    # Print Results #
    print "==================================================================="
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
        super(MyThread, self).__init__(target=runGenerator, name="MyThread",
                                       args=(db, self._abortEvent))


    def stop(self):
        self._abortEvent.set()

    def stopped(self):
        return self._abortEvent.isSet()
        # ^This needs to be an event that returns UI to normal. TODO
