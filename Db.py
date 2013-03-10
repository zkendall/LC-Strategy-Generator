#-------------------------------------------------------------------------------
# Name:     Lending Club Database Module
# Purpose:  Manage SQLite db for generator
# Author:   Zachariah Kendall
# Created:  01/~~/2013
# Modified: 02/23/2013
#-------------------------------------------------------------------------------

import sqlite3, csv
import os.path


class Db(object):
    def __init__(self):
        self.dbLoaded = False
##        print "Db class initialized"

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            print "Db connection closed"

    def connectToDb(self, dbFilename='loans.db'):
        print "Connecting to database"
        # Is not 'check_same_thread' safe?
        self.conn = sqlite3.connect(dbFilename, check_same_thread = False)
                                                                            
        self.cursor = self.conn.cursor()
        self.dbLoaded = True
        print "Connected to database"

    def buildDb(self, csvFileAddress='LoanStats.csv', dbFilename='loansNew.db'):
        print "Building database from", csvFileAddress
        # If db exists ask to replace.
        if os.path.isfile(dbFilename):
            # TODO: The prompt needs changed to windowed.
            replace = raw_input("Database Exists. Remove and replace? (y/n)")  
            if replace == 'y':
                try: os.remove(dbFilename)
                except:
                    print "Could not remove", dbFilename
                    return
            else: return

        # Connect
        self.conn = sqlite3.connect(dbFilename)
        self.cursor = self.conn.cursor()
        self.createTable()
        with open(csvFileAddress, 'r') as csvfile:
            csvfile.next()  # skip header
            reader = csv.reader(csvfile, delimiter=',')
            for i, line in enumerate(reader):
                ##try:
                self.insertCSVLine(line)
                ##except Exception:
                ##  print "Error on line", i , line
                ##  print Exception
            self.conn.commit()
            print "\nFinished loading CSV"
        self.dbLoaded = True

        # The last 3% of the csv are
        #  "Loans that do not meet the current credit policy"
        #  Include or not?

    # Parse CSV line and insert into db #
    def insertCSVLine(self, line):
        command = "INSERT INTO loan VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?," \
           + "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?," \
           + " ?, ?, ?, ?, ?, ?)"
        values = (  line[0], # loanID
                    line[1], # amountRequested
                    line[2], # amountFunded
                    line[3][0:1], # interestRate
                    line[4], # loanLength
                    calculateROI(line[1], line[19]), # Calculated ROI
                    line[5], # applicationDate
                    line[6], # applicationExpiration
                    line[7], # issueDate
                    line[8][0], # creditGrade (Take letter only)
                    line[10], # loanPurpose
                    line[12], # monthlyPayment
                    line[13], # status
                    line[14], # totalAmountFunded
                    line[15][0:-1], # debtToIncomeRatio
                    line[16], # remainingPrincipalFunded
                    line[17], # paymentsToDateFunded
                    line[18], # remainingPrincipal
                    line[19], # paymentsToDate
                    line[22], # state
                    line[23], # homeOwnership
                    line[24], # montlyIncome
                    assignFicoRange(line[25]), # ficoRange
                    line[26], # earliestCreditLine
                    line[27], # openCreditLines
                    line[28], # totalCreditLines
                    line[29], # revolvingCreditBalance
                    line[30][0:-1], # revolvingLineUtilization
                    line[31], # inquiriesSixMonths
                    line[32], # accountsNowDelinquent
                    line[33], # delinquentAmount
                    line[34], # delinquenciesTwoYears
                    line[35], # monthsLastDelinquency
                    line[36], # publicRecordsonFile
                    employmentInteger(line[39]), # employmentLength
                    line[41]  # initialListingStatus
                )
        self.cursor.execute(command, values)

    def createTable(self):  #Add ROI
        createTableQuery = """CREATE TABLE loan (
            id INTEGER NOT NULL PRIMARY KEY,
            amountRequested REAL,
            amountFunded REAL,
            interestRate REAL,
            loanLength TEXT,
            roi REAL,
            applicationDate TEXT,
            applicationExpiration TEXT,
            issueDate TEXT,
            creditGrade TEXT,
            loanPurpose TEXT,
            monthlyPayment REAL,
            status TEXT,
            totalAmountFunded REAL,
            debtToIncomeRatio REAL,
            remainingPrincipalFunded REAL,
            paymentsToDateFunded REAL,
            remainingPrincipal REAL,
            paymentsToDate REAL,
            state TEXT,
            homeOwnership TEXT,
            montlyIncome REAL,
            ficoRange TEXT,
            earliestCreditLine TEXT,
            openCreditLines INTEGER,
            totalCreditLines INTEGER,
            revolvingCreditBalance INTEGER,
            revolvingLineUtilization REAL,
            inquiriesSixMonths INTEGER,
            accountsNowDelinquent INTEGER,
            delinquentAmount INTEGER,
            delinquenciesTwoYears INTEGER,
            monthsLastDelinquency INTEGER,
            publicRecordsonFile INTEGER,
            employmentLength TEXT,
            initialListingStatus TEXT
            )""" # Took out: loanTitle TEXT, loanDescription TEXT,  
                 # city TEXT,  monthsLastRecord INTEGER, monthsLastRecord INTEGER,  
                 # education TEXT,  code TEXT, screenName TEXT,
        self.cursor.execute(createTableQuery)

################################################################################

    def executeCommand(self, cmd):
        for row in self.cursor.execute(cmd):
            print row

##  def makeSelect(self, input):
##      return self.cursor.execute("SELECT %s FROM load") % (input)

    def printAll(self):
        print "\nHere's a listing of all the records in the table:\n"
        for row in self.cursor.execute("SELECT id, roi, FROM loan"):
            print row

    def getROIandCount(self, q):
        #print "\nSelected Notes Average ROI:"
        for row in self.cursor.execute(q):
            return (row[0], row[1])  #Return ROI


################################################################################
#######################  Helper Methods for building Db  #######################
################################################################################
def calculateROI(loanAmount, paidAmount):
    """I'm not sure how accurate this is..."""
    amount = float(loanAmount)
    ret = (float(paidAmount) - amount) / amount
    return round(ret * 100, 1)  # Percentageize


def assignFicoRange(f):
    # Fico range is currently listed in ranges of 5.
    # This makes 42 options. I'm 'expanding' the
    # bucket range to a 25pt spread for convenience.
    if len(f) < 3:
        return
    fico = int(f[:3])
    if 640 <= fico <= 675:
        return '640-675'
    if 676 <= fico <= 700:
        return '676-700'
    if 701 <= fico <= 725:
        return '701-725'
    if 726 <= fico <= 750:
        return '726-750'
    if 751 <= fico <= 775:
        return '751-775'
    if 776 <= fico <= 800:
        return '776-800'
    if 801 <= fico <= 825:
        return '801-825'
    if 826 <= fico <= 850:
        return '826-850'


def employmentInteger(length):
    if length[0] == '<':
        return 0
    else:
        return length[0]
