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
import db

# Initialize Db #
db = db.Db()

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
        self.SetSize((250, 300))
        # Initialize User Interface #
        self.InitUI()

    def InitUI(self):
        self.currentDirectory = os.getcwd()

        # Split Panels #
        splitter = wx.SplitterWindow(self, -1)
        splitter.SetMinimumPaneSize(50)

        # Left Panel
        panLeft = wx.Panel(splitter, -1)
        self.custom_tree = CT.CustomTreeCtrl(panLeft, -1)

        # Add Tree Items
        root = self.custom_tree.AddRoot("The Root Item")
        root.Expand()
        last = self.custom_tree.AppendItem(root, "item 1")
        item = self.custom_tree.AppendItem(last,  "item 2", ct_type=1)
        self.Bind(CT.EVT_TREE_ITEM_CHECKED, self.ItemChecked)
        sizer = wx.BoxSizer(wx.VERTICAL)
        sizer.Add(self.custom_tree, -1, wx.EXPAND)
        panLeft.SetSizerAndFit(sizer)
        sizer.Layout()

        
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

        self.Bind(wx.EVT_MENU, self.OnQuit, quit_mi)
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


    def ItemChecked(self, event):
        print("Somebody checked something")
        print(event.GetSelections())


    def OnQuit(self, e):
        print "Quitting!"
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
        self.btnGenerate.Enable(False)
        self.btnAbort.Enable(True)
        self.generator_thread = generator.MyThread(db)  # Pass in database
        self.generator_thread.start()

        # Other options I experimented with #
        # thread.start_new_thread(Generator.runGenerator,(db))
        # delayedresult.startWorker(self.resultConsumer, # Send finished result
        #                           Generator.runGenerator(db))


    # def resultConsumer(self, delayedresult):
    #     # reinable disabled interface.
    #     self.btnGenerate.Enable(True)
    #     self.btnAbort.Enable(False)


    def onAbort(self, e):
        print "Aborting generator..."
        self.generator_thread.stop()
        self.btnAbort.SetLabel("Aborting")
        self.generator_thread.join()
        self.btnGenerate.Enable(True)
        self.btnAbort.Enable(False)
        self.btnAbort.SetLabel("Abort")





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
