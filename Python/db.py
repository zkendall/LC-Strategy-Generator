#-------------------------------------------------------------------------------
# Name:     Lending Club Database Module
# Purpose:  Manage SQLite db for generator
# Author:   Zachariah Kendall
# Created:  01/--/2013
# Modified: 04/06/2013
#-------------------------------------------------------------------------------

import sqlite3, csv
import os.path


class Db(object):
    def __init__(self):
        self.dbLoaded = False

    def close(self):
        if hasattr(self, 'conn'):
            self.conn.close()
            print "Db connection closed"

    def connectToDb(self, dbFilename='loans.db'):
        print "Connecting to database"
        # Is 'check_same_thread=False' safe?
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
        self._createTable()
        with open(csvFileAddress, 'r') as csvfile:
            csvfile.next()  # skip header
            reader = csv.reader(csvfile, delimiter=',')
            for line in reader:
                self._insertCSVLine(line)
            self.conn.commit()
            print "\nFinished loading CSV"
        self.dbLoaded = True

        # The last 3% of the csv are
        #  "Loans that do not meet the current credit policy"
        #  Include or not?
        #   ^ May be fixed in new source files. They seperated those out?

    # Parse CSV line and insert into db #
    def _insertCSVLine(self, line):
        command = "INSERT INTO loan VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
          + "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, " \
          + "?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)"
        print line
        values = (  line[1],  # id
                    line[2],  # loan_amnt
                    line[3],  # funded_amnt
                    line[4],  # funded_amnt_inv
                    line[5],  # loanLength
                    line[6],  # apr
                    line[7],  # int_rate
                    line[8],  # installment
                    line[9],  # grade
                    line[12],  # emp_length
                    line[13],  # home_ownership
                    line[14],  # annual_inc
                    line[15],  # is_inc_v
                    line[16],  # accept_d
                    line[17],  # exp_d
                    line[18],  # list_d
                    line[19],  # issue_d
                    line[20],  # loan_status
                    line[24],  # purpose
                    line[27],  # addr_state
                    line[28],  # acc_now_delinq
                    line[29],  # acc_open_past_24mths
                    line[33],  # dti                    ???
                    line[34],  # delinq_2yrs
                    line[35],  # delinq_amnt
                    line[36],  # earliest_cr_line
                    line[37],  # fico_range_low
                    line[38],  # fico_range_high
                    line[39],  # inq_last_6mths
                    line[40],  # mths_since_last_delinq
                    line[41],  # mths_since_last_record
                    line[47],  # open_acc
                    line[49],  # pub_rec
                    line[51],  # revol_bal
                    line[52],  # revol_util
                    line[54],  # total_acc
                    line[58],  # total_pymnt
                    line[59],  # total_pymnt_inv
                    line[60],  # total_rec_prncp
                    line[61],  # total_rec_int
                    line[62],  # total_rec_late_fee
                    line[63],  # last_pymnt_d
                    line[64],  # last_pymnt_amnt
                    line[66],  # last_credit_pull_d
                    line[67],  # last_fico_range_high
                    line[68],  # last_fico_range_low
                )
        self.cursor.execute(command, values)

    def _createTable(self):  #Add ROI
        createTableQuery = """CREATE TABLE loan (
            id INTEGER NOT NULL PRIMARY KEY,
            loan_amnt TEXT,
            funded_amnt TEXT,
            funded_amnt_inv TEXT,
            loanLength TEXT,
            apr TEXT,
            int_rate TEXT,
            installment TEXT,
            grade TEXT,
            emp_length TEXT,
            home_ownership TEXT,
            annual_inc TEXT,
            is_inc_v TEXT,
            accept_d TEXT,
            exp_d TEXT,
            list_d TEXT,
            issue_d TEXT,
            loan_status TEXT,
            purpose TEXT,
            addr_state TEXT,
            acc_now_delinq TEXT,
            acc_open_past_24mths TEXT,
            dti TEXT,
            delinq_2yrs TEXT,
            delinq_amnt TEXT,
            earliest_cr_line TEXT,
            fico_range_low TEXT,
            fico_range_high TEXT,
            inq_last_6mths TEXT,
            mths_since_last_delinq TEXT,
            mths_since_last_record TEXT,
            open_acc TEXT,
            pub_rec TEXT,
            revol_bal TEXT,
            revol_util TEXT,
            total_acc TEXT,
            total_pymnt TEXT,
            total_pymnt_inv TEXT,
            total_rec_prncp TEXT,
            total_rec_int TEXT,
            total_rec_late_fee TEXT,
            last_pymnt_d TEXT,
            last_pymnt_amnt TEXT,
            last_credit_pull_d TEXT,
            last_fico_range_high TEXT,
            last_fico_range_low TEXT
            )"""
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
def _calculateROI(loanAmount, paidAmount):
    """I'm not sure how accurate this is..."""
    amount = float(loanAmount)
    ret = (float(paidAmount) - amount) / amount
    return round(ret * 100, 1)  # Percentageize


def _assignFicoRange(f):
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


def _employmentInteger(length):
    if length[0] == '<':
        return 0
    else:
        return length[0]
