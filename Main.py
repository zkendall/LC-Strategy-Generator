#--------------------------------------------------------------------------------------------
# Name:         Lending Club Strategy Generator
# Purpose:      To generate strategies to choose notes on LendingClub.com
# Author:       Zachariah Kendall
# Created:      04/01/2013
#--------------------------------------------------------------------------------------------

# Global imports
import os
import wx
import wx.lib.agw.customtreectrl as CT
#import wx.lib.delayedresult as delayedresult

# Local imports
import generator
from generator import doLog
import db

# Initialize Db #
db = db.Db()

# TODO: Remove this
# Just so I don't have to manually load the db:
db.connectToDb()

# IDs #
APP_EXIT = 1
APP_OPEN_CSV = 2
APP_OPEN_DB = 3
#APP_GENERATE = 4


class MyWindow(wx.Frame):
    """This is the GUI class"""
    global db
    def __init__(self, *args, **kwargs):
        super(MyWindow, self).__init__(*args, **kwargs)
        self.SetSize((640, 480))
        # Initialize User Interface #
        self.InitUI()

    def InitUI(self):
        """Build and place UI componants"""
        self.currentDirectory = os.getcwd()

        # Split Panels #
        splitter = wx.SplitterWindow(self, -1)
        splitter.SetMinimumPaneSize(30)
        splitter.SetSashGravity(0.2)


        # Left Panel
        panLeft = wx.Panel(splitter, -1)
        self.custom_tree = CT.CustomTreeCtrl(panLeft, -1)

        # Add Tree Items
        root = self.custom_tree.AddRoot("Filters", data="employmentLength")
        root.Expand()
        employment = self.custom_tree.AppendItem(root, "Employment Length ", ct_type=1,
                                                    data="employmentLength")
        self.custom_tree.AppendItem(employment, "1 Year ", ct_type=1, data="'1'")
        self.custom_tree.AppendItem(employment, "2 Year ", ct_type=1, data="'2'")
        self.custom_tree.AppendItem(employment, "3 Year ", ct_type=1, data="'3'")
        self.custom_tree.AppendItem(employment, "4 Year ", ct_type=1, data="'4'")
        self.custom_tree.AppendItem(employment, "5 Year ", ct_type=1, data="'5'")

        homeShip = self.custom_tree.AppendItem(root, "Home Ownership ", ct_type=1,
                                                data="homeOwnership")
        self.custom_tree.AppendItem(homeShip, "Own", ct_type=1, data="'OWN'")
        self.custom_tree.AppendItem(homeShip, "Mortgage", ct_type=1, data="'MORTGAGE'")
        self.custom_tree.AppendItem(homeShip, "Rent", ct_type=1, data="'RENT'")
        self.custom_tree.AppendItem(homeShip, "Other", ct_type=1, data="'OTHER'")

        loanLength = self.custom_tree.AppendItem(root,  "Loan Length", ct_type=1,
                                                    data="loanLength")
        self.custom_tree.AppendItem(loanLength,"36 Months", ct_type=1, data="'36 months'")
        self.custom_tree.AppendItem(loanLength,"60 Months", ct_type=1, data="'60 months'")

        inquiries = self.custom_tree.AppendItem(root,  "Inquiries in Six Months", ct_type=1,
                                                data="inquiriesSixMonths")
        self.custom_tree.AppendItem(inquiries, "1", ct_type=1, data="'1'")
        self.custom_tree.AppendItem(inquiries, "2", ct_type=1, data="'2'")
        self.custom_tree.AppendItem(inquiries, "3", ct_type=1, data="'3'")
        self.custom_tree.AppendItem(inquiries, "4", ct_type=1, data="'4'")
        self.custom_tree.AppendItem(inquiries, "5", ct_type=1, data="'5'")

        credit = self.custom_tree.AppendItem(root,  "Credit Grade", ct_type=1,
                                                data="creditGrade")
        self.custom_tree.AppendItem(credit, "A", ct_type=1, data="'A'")
        self.custom_tree.AppendItem(credit, "B", ct_type=1, data="'B'")
        self.custom_tree.AppendItem(credit, "C", ct_type=1, data="'C'")
        self.custom_tree.AppendItem(credit, "D", ct_type=1, data="'D'")
        self.custom_tree.AppendItem(credit, "E", ct_type=1, data="'E'")
        self.custom_tree.AppendItem(credit, "F", ct_type=1, data="'F'")
        self.custom_tree.AppendItem(credit, "G", ct_type=1, data="'G'")

        fico = self.custom_tree.AppendItem(root,  "FICO Range", ct_type=1,
                                            data="ficoRange")
        self.custom_tree.AppendItem(fico, "640-675", ct_type=1, data="'640-675'")
        self.custom_tree.AppendItem(fico, "676-700", ct_type=1, data="'676-700'")
        self.custom_tree.AppendItem(fico, "701-725", ct_type=1, data="'701-725'")
        self.custom_tree.AppendItem(fico, "726-750", ct_type=1, data="'726-750'")
        self.custom_tree.AppendItem(fico, "751-775", ct_type=1, data="'751-775'")
        self.custom_tree.AppendItem(fico, "776-800", ct_type=1, data="'776-800'")
        self.custom_tree.AppendItem(fico, "801-825", ct_type=1, data="'801-825'")
        self.custom_tree.AppendItem(fico, "826-850", ct_type=1, data="'826-850'")


        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.itemChecked)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.custom_tree, -1, wx.EXPAND)
        panLeft.SetSizerAndFit(sizer)
        sizer.Layout()



        self.loadPreferences()

        # Right Panels
        panRight = wx.Panel(splitter, -1)
        vbox = wx.BoxSizer(wx.VERTICAL)
        panTop = wx.Panel(panRight)
        panTop.SetBackgroundColour('#eeeeee')
        panBottom = wx.Panel(panRight)
        panBottom.SetBackgroundColour('#555555')
        vbox.Add(panTop, 1, wx.EXPAND | wx.ALL, 10)
        vbox.Add(panBottom, 1, wx.EXPAND | wx. ALL, 10)
        panRight.SetSizer(vbox)

        splitter.SplitVertically(panLeft, panRight)
        splitter.SetSashPosition(200)

        # Top Button Set
        self.btnGenerate = wx.Button(panTop, -1, "Generate")
        self.btnGenerate.Bind(wx.EVT_BUTTON, self.onGenerate)
        self.btnAbort = wx.Button(panTop, -1, "Abort")
        self.btnAbort.Bind(wx.EVT_BUTTON, self.onAbort)

        hsizer = wx.BoxSizer(wx.HORIZONTAL)
        hsizer.Add(self.btnGenerate, 0, wx.ALL, 5)
        hsizer.Add(self.btnAbort, 0, wx.ALL, 5)
        panTop.SetSizer(hsizer)

        # File Menu #
        fileMenu = wx.Menu()
        quit_mi = wx.MenuItem(fileMenu, APP_EXIT, '&Quit\tCtrl+Q')
        open_csv_mi = wx.MenuItem(fileMenu, APP_OPEN_CSV, '&Open CSV')
        open_db_mi = wx.MenuItem(fileMenu, APP_OPEN_DB, '&Open DB')

        fileMenu.AppendItem(open_csv_mi)
        fileMenu.AppendItem(open_db_mi)
        fileMenu.AppendItem(quit_mi)

        self.Bind(wx.EVT_MENU, self.onQuit, quit_mi)
        self.Bind(wx.EVT_MENU, self.onOpenCSV, open_csv_mi)
        self.Bind(wx.EVT_MENU, self.onOpenDb, open_db_mi)

        # Menu Bar #
        menubar = wx.MenuBar()
        menubar.Append(fileMenu, '&File')
        self.SetMenuBar(menubar)

        # Status Bar #
        self.statusbar = self.CreateStatusBar()
        self.statusbar.SetStatusText('Ready')
        self.statusbar.Show()


    def itemChecked(self, event):
        """Enable corresponding filter in the generator"""
        item = event.GetItem()
        isChecked = self.custom_tree.IsItemChecked(item)
        log("Toggled \"%s\" %s" % (self.custom_tree.GetItemText(item), isChecked))
        parent = self.custom_tree.GetItemParent(item)
        data = self.custom_tree.GetItemPyData(item)

        generator.toggleFilter(self.custom_tree.GetItemPyData(parent), data, isChecked)

        event.Skip()

    def loadPreferences(self):
        """Get filter options from generator and enable corresponding UI"""
        cur, cookie = self.custom_tree.GetFirstChild(self.custom_tree.GetRootItem())
        f = generator.filters
        while cur:
            data = self.custom_tree.GetItemPyData(cur)
            if f[data]:
                self.custom_tree.CheckItem(cur)
                cur.Expand()

            child, cookie = self.custom_tree.GetFirstChild(cur)
            options = generator.getFilterDict(data)
            while child:
                data = self.custom_tree.GetItemPyData(child)
                if options[data]:
                    self.custom_tree.CheckItem(child)
                child = self.custom_tree.GetNextSibling(child)

            cur = self.custom_tree.GetNextSibling(cur)


    def onQuit(self, e):
        """Close the application"""
        log("Quitting.")
        db.close()
        self.Close()

    def onOpenCSV(self, e):
        """Create and show the Open FileDialog"""
        dlg = wx.FileDialog(
            self, message="Choose a Lending Club CSV file",
            defaultDir=self.currentDirectory,
            defaultFile="",
            wildcard="CSV file (*.csv)|*.csv|All files (*.*)|*.*",
            style=wx.OPEN | wx.MULTIPLE | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            db.buildDb(path);
        dlg.Destroy()

    def onOpenDb(self, e):
        """Create and show the Open FileDialog"""
        dlg = wx.FileDialog(
            self, message="Choose a Db file containing Lending Club loans",
            defaultDir = self.currentDirectory,
            defaultFile = "",
            wildcard = "CSV file (*.db)|*.db|All files (*.*)|*.*",
            style = wx.OPEN | wx.CHANGE_DIR
        )
        if dlg.ShowModal() == wx.ID_OK:
            path = dlg.GetPath()
            db.connectToDb(path)
        dlg.Destroy()


    def onGenerate(self, e):
        """Run Generator"""
        if not db.dbLoaded:
            log("Database is not loaded")
            return
        self.btnGenerate.Enable(False)
        self.btnAbort.Enable(True)
        self.generator_thread = generator.MyThread(db)  # Pass in database
        self.generator_thread.start()

        # TODO: Disable sidepanel options!



    def onAbort(self, e):
        log("Aborting generator...")
        self.generator_thread.stop()
        self.btnAbort.SetLabel("Aborting")
        self.generator_thread.join()
        self.btnGenerate.Enable(True)
        self.btnAbort.Enable(False)
        self.btnAbort.SetLabel("Abort")


def log(text):
    if doLog:
        print "Main:", text

##########################################################

class MyApp(wx.App):
    def __init__(self, redirect=False, filename=None):
        wx.App.__init__(self, redirect, filename)
        self.frame = MyWindow(None)
        self.frame.Show()
        self.frame.Centre()
        self.frame.SetTitle('LendingClub Strategy Generator')

if __name__ == '__main__':
    app = MyApp()
    app.MainLoop()
